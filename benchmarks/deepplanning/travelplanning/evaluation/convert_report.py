"""
Convert agent reports to structured JSON format for evaluation

This module uses an LLM to parse the agent's natural language travel plans
and convert them into structured JSON format required by the evaluation module.
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, Optional, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

import openai

# Add parent directory to path to import prompts and call_llm utilities
sys.path.insert(0, str(Path(__file__).parent.parent / 'agent'))
from prompts import get_format_convert_prompt
from call_llm import load_model_config, create_client

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from task_selection import normalize_task_ids  # noqa: E402


DEFAULT_CONVERSION_MODEL = 'conversion-model'


# Load environment variables from .env file
def _load_env_from_dotenv() -> None:
    """
    Load environment variables from .env file if exists
    
    Searches for .env in the following order:
    1. Domain directory (travelplanning/)
    2. Project root (parent of domain)
    """
    try:
        # Try domain directory first
        domain_root = Path(__file__).parent.parent
        domain_dotenv = domain_root / '.env'
        
        # Try project root
        project_root = domain_root.parent
        project_dotenv = project_root / '.env'
        
        # Use project root .env if it exists, otherwise domain .env
        dotenv_path = project_dotenv if project_dotenv.exists() else domain_dotenv
        
        if not dotenv_path.exists():
            return
        
        for line in dotenv_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and value and key not in os.environ:
                    os.environ[key] = value
    except Exception as e:
        pass  # Silently ignore if .env loading fails

# Load .env at module import time
_load_env_from_dotenv()


def extract_json_from_response(text: str) -> Optional[str]:
    """Extract JSON content from model output (looks for <JSON>...</JSON> tags)"""
    if not text:
        return None

    # Try to extract from <JSON> tags
    match = re.search(r"<JSON>([\s\S]*?)</JSON>", text)
    if match:
        return match.group(1).strip()

    # If no tags, return as-is and let caller try to parse
    return text


def extract_entity_names(parsed: Dict) -> list:
    """Extract every entity name from a converted plan that the evaluator will check.

    Mirrors the same fields/normalization used by
    `travelplanning/evaluation/utils.py::iter_meal_acts`,
    `iter_attraction_acts`, `iter_hotel_acts`, and `iter_accommodation_entries`:
        - day.activities[i].details.name  (type ∈ {meal, attraction, hotel})
        - day.accommodation.name
    All names are `.strip()`'d on the plan side, matching the evaluator.
    """
    names: list = []
    daily_plans = parsed.get("plans") or parsed.get("daily_plans") or []
    if not isinstance(daily_plans, list):
        return names
    for day in daily_plans:
        if not isinstance(day, dict):
            continue
        for act in day.get("activities") or []:
            if not isinstance(act, dict):
                continue
            if act.get("type") not in ("meal", "attraction", "hotel"):
                continue
            details = act.get("details") or {}
            name = (details.get("name") or "").strip()
            if name:
                names.append(name)
        accom = day.get("accommodation")
        if isinstance(accom, dict):
            name = (accom.get("name") or "").strip()
            if name:
                names.append(name)
    return names


def check_name_fidelity(names: list, report_text: str) -> list:
    """Return list of names NOT present as substrings in report_text.

    Uses strict substring match with no normalization, matching the evaluator's
    direct `==`/`in` comparison against DB keys. The only normalization is
    `.strip()` on plan-side names, which mirrors the evaluator exactly.
    """
    missing = []
    for name in names:
        if name and name not in report_text:
            missing.append(name)
    return missing


class NameFidelityError(ValueError):
    """Raised when converted plan contains entity names not present in original report."""

    def __init__(self, missing_names: list, total_names: int):
        self.missing_names = missing_names
        self.total_names = total_names
        super().__init__(
            f"name-fidelity check failed: {len(missing_names)}/{total_names} names "
            f"absent from report.txt; first few: {missing_names[:5]}"
        )


# A bare intercity transport number: optional carrier prefix of letters (MU,
# KTX) or digit+letter (9C, 3U) followed by digits, e.g. G7554, MU5137,
# 9C8888, 1462. Anything already matching this is left verbatim.
_BARE_TRANSPORT_NUMBER_RE = re.compile(r'^(?:[A-Za-z]{1,3}|\d[A-Za-z])?\d{1,5}[A-Za-z]?$')
_TOKEN_TRIM_CHARS = '()[]{}«»„"\'‘’“”.,;:!?'


def normalize_transport_numbers(parsed: Dict) -> int:
    """Strip carrier words the conversion LLM glues onto `details.number`.

    On fr/ru runs the converter emits e.g. "Vol MU5137" / "поезд G7554" while
    the evaluator exact-matches the bare number against the flight/train DB
    index, force-failing the transport checks for those languages. When the
    field is not already a bare number and exactly one whitespace-separated
    token qualifies as one, keep only that token. Ambiguous or unrecognized
    values are left verbatim. Returns the number of fields rewritten.
    """
    changed = 0
    daily_plans = parsed.get("plans") or parsed.get("daily_plans") or []
    if not isinstance(daily_plans, list):
        return 0
    for day in daily_plans:
        if not isinstance(day, dict):
            continue
        for act in day.get("activities") or []:
            if not isinstance(act, dict) or act.get("type") != "travel_intercity_public":
                continue
            details = act.get("details")
            if not isinstance(details, dict):
                continue
            number = details.get("number")
            if not isinstance(number, str):
                continue
            stripped = number.strip()
            if not stripped or _BARE_TRANSPORT_NUMBER_RE.match(stripped):
                continue
            candidates = {
                token.strip(_TOKEN_TRIM_CHARS)
                for token in stripped.split()
                if _BARE_TRANSPORT_NUMBER_RE.match(token.strip(_TOKEN_TRIM_CHARS))
            }
            candidates.discard('')
            if len(candidates) == 1:
                details["number"] = candidates.pop()
                changed += 1
    return changed


def process_single_report(
    report_file: Path,
    output_dir: Path,
    model_name: str,
    client: openai.OpenAI,
    format_prompt: str,
    print_lock: Lock,
    max_retries: int = 30,
    temperature: Optional[float] = None,
) -> Dict:
    """
    Process a single report file and convert to JSON
    
    Args:
        report_file: Input report file path
        output_dir: Output directory for converted JSON
        model_name: Model name for API call
        client: OpenAI client instance
        format_prompt: Format conversion prompt
        print_lock: Thread-safe print lock
        max_retries: Maximum number of retries for JSON parsing errors
        
    Returns:
        Processing result dictionary
    """
    sample_id = None
    
    # Extract sample_id from filename (format: id_X.txt)
    filename = report_file.name
    match = re.match(r'id_(\d+)\.txt', filename)
    if match:
        sample_id = match.group(1)
    else:
        # Try without id_ prefix
        match = re.match(r'(\d+)_final_answer\.txt', filename)
        if match:
            sample_id = match.group(1)
        else:
            sample_id = report_file.stem.replace('_final_answer', '')
    
    # Retry loop for JSON parsing errors
    for attempt in range(max_retries + 1):
        try:
            if attempt == 0:
                with print_lock:
                    print(f"\n{'='*80}")
                    print(f"🚀 [Thread Started] Processing Sample ID: {sample_id}")
                    print(f"   Input File: {report_file.name}")
                    print(f"{'='*80}")
            else:
                with print_lock:
                    print(f"🔄 Sample {sample_id} JSON parsing failed, retry attempt {attempt}...")
            
            # Read raw text
            raw_text = report_file.read_text(encoding='utf-8')
            
            # Construct messages
            messages = [
                {"role": "system", "content": format_prompt},
                {"role": "user", "content": raw_text},
            ]
            
            # Call LLM for conversion. max_tokens=32768 because Hebrew/Hindi/etc.
            # tokenize denser than English/Chinese; 10240 truncated mid-output for
            # 7-day plans, leaving an unterminated <JSON> tag and forcing 30 retries.
            # timeout is REQUIRED. Without it the SDK inherits httpx's default of
            # no read deadline, so a proxy that accepts the connection and then
            # never answers parks the worker thread in ssl.read() forever. That
            # wedged conversion runs in practice (threads idle on
            # ssl.py:1165, CPU ~0, no progress) until the watchdog killed them,
            # stranding finished inference. 600s is well past the p99 for a
            # 32k-token max-effort completion, so it only fires on a real hang.
            create_kwargs = {
                "model": model_name,
                "messages": messages,
                "max_tokens": 32768,
                "timeout": 600,
            }
            if temperature is not None:
                create_kwargs["temperature"] = temperature
            resp = client.chat.completions.create(**create_kwargs)
            
            content = resp.choices[0].message.content or ""
            
            # Extract JSON
            json_payload = extract_json_from_response(content)
            if not json_payload:
                # If no tags and can't parse directly, fail this attempt
                try:
                    json.loads(content)
                    json_payload = content
                except Exception as e:
                    raise ValueError(f"LLM did not return content with <JSON> tags, and direct parsing failed: {e}")
            
            # Validate JSON (this is the key step for retry)
            parsed = json.loads(json_payload)

            # Strip glued carrier words from intercity transport numbers so
            # the evaluator's exact number match sees the bare number.
            normalize_transport_numbers(parsed)

            # Name-fidelity check: every entity name in the converted plan must
            # appear as a literal substring in the original report. This guards
            # against the conversion LLM rewriting names (he construct-state,
            # ko Chinese→Korean transliteration, etc.). Strict — no normalize,
            # mirroring the evaluator's exact-match comparison.
            names = extract_entity_names(parsed)
            missing = check_name_fidelity(names, raw_text)
            if missing:
                raise NameFidelityError(missing, len(names))

            # If successful, save and exit loop
            output_file = output_dir / f'id_{sample_id}_converted.json'
            output_file.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding='utf-8')

            with print_lock:
                print(f"✅ Sample {sample_id} conversion completed (attempt {attempt + 1})")
                print(f"   Output File: {output_file.name}\n")

            return {
                'success': True,
                'sample_id': sample_id,
                'input_file': str(report_file),
                'output_file': str(output_file)
            }

        except (json.JSONDecodeError, ValueError) as e:
            # Catch JSON parsing errors, fidelity errors, and our ValueError
            # If last attempt, write INVALID marker so the evaluator can exclude
            # the case from case_acc denominator instead of scoring it 0.
            if attempt >= max_retries:
                with print_lock:
                    print(f"❌ Sample {sample_id} failed after {max_retries + 1} attempts: {e}\n")

                # Write a convert_failed marker JSON so eval_converted.py can
                # treat this case as INVALID (excluded from denominator) rather
                # than as a 0-score conversion.
                missing_names = getattr(e, 'missing_names', None)
                marker = {
                    "convert_failed": True,
                    "reason": "name-fidelity check failed" if isinstance(e, NameFidelityError)
                              else f"json parsing failed: {type(e).__name__}",
                    "error": str(e),
                    "missing_names": missing_names if missing_names is not None else [],
                }
                output_file = output_dir / f'id_{sample_id}_converted.json'
                output_file.write_text(json.dumps(marker, ensure_ascii=False, indent=2), encoding='utf-8')

                return {
                    'success': False,
                    'sample_id': sample_id,
                    'input_file': str(report_file),
                    'error': str(e)
                }
            # If not last attempt, continue to next retry
            time.sleep(1)  # Brief delay to avoid rapid requests
            
        except Exception as e:
            # Catch other unexpected errors (e.g., network issues)
            if attempt >= max_retries:
                with print_lock:
                    print(f"❌ Sample {sample_id} encountered unexpected error: {e}\n")
                
                return {
                    'success': False,
                    'sample_id': sample_id,
                    'input_file': str(report_file),
                    'error': str(e)
                }
            time.sleep(1)


def convert_reports(
    result_dir: Path,
    language: str = 'zh',
    workers: int = 10,
    skip_existing: bool = False,
    verbose: bool = False,
    conversion_model: str = DEFAULT_CONVERSION_MODEL,
    selected_ids: Optional[Sequence[object]] = None,
    require_artifacts: bool = True,
) -> Dict:
    """
    Convert multiple report files to JSON format

    Args:
        result_dir: Result directory containing 'reports' subdirectory
        language: Language for prompts ('zh' or 'en')
        workers: Number of concurrent workers
        skip_existing: Skip files that already have output
        verbose: Enable verbose output
        conversion_model: Model configuration name used for report conversion
        selected_ids: Exact task IDs to convert, or None for every report
        require_artifacts: With selected_ids, True (explicit-rerun contract)
            fails hard when a selected report or converted plan is missing;
            False (task-subset mode) mirrors the full-run protocol — absent
            artifacts are skipped here and score 0 at evaluation

    Returns:
        dict: {'total': int, 'converted': int, 'skipped': int, 'results': list}
    """
    reports_dir = result_dir / 'reports'
    output_dir = result_dir / 'converted_plans'
    output_dir.mkdir(parents=True, exist_ok=True)

    requested_ids = normalize_task_ids(selected_ids) if selected_ids is not None else None
    candidates = sorted(reports_dir.glob('id_*.txt'))
    if requested_ids is None:
        report_files = candidates
    else:
        reports_by_id = {}
        for report_file in candidates:
            match = re.fullmatch(r'id_([0-9]+)\.txt', report_file.name)
            if match is None or str(int(match.group(1))) != match.group(1):
                raise ValueError(f"Malformed report filename: {report_file.name}")
            sample_id = match.group(1)
            if sample_id in reports_by_id:
                raise ValueError(f"Duplicate report for task ID {sample_id}")
            reports_by_id[sample_id] = report_file
        missing = [task_id for task_id in requested_ids if task_id not in reports_by_id]
        if missing:
            if require_artifacts:
                raise FileNotFoundError(
                    f"Selected reports are missing from {reports_dir}: {', '.join(missing)}"
                )
            # Task-subset mode mirrors the full-run protocol: a case whose
            # inference produced no report is skipped here and scores 0 at
            # evaluation (the denominator stays the selected-set size).
            print(
                f"⚠️  {len(missing)} selected reports are absent and will score 0: "
                + ", ".join(missing)
            )
        report_files = [
            reports_by_id[task_id]
            for task_id in requested_ids
            if task_id in reports_by_id
        ]

    if not report_files:
        print(f"⚠️  No report files found in {reports_dir}")
        return {'total': 0, 'converted': 0, 'skipped': 0, 'success': 0, 'failed': 0, 'results': []}

    # Artifact validation happens before client creation so a missing selected
    # report fails without opening a model connection.
    model_config = load_model_config(conversion_model)
    client = create_client(conversion_model, model_config)
    actual_model_name = model_config.get('model_name', conversion_model)
    conversion_temperature = model_config.get('temperature')
    format_prompt = get_format_convert_prompt(language)

    # Track original count and filtered files
    original_count = len(report_files)
    skipped_count = 0
    
    # Filter out existing files if skip_existing is True
    if skip_existing:
        filtered_files = []
        for report_file in report_files:
            # Extract sample_id
            match = re.match(r'id_(\d+)\.txt', report_file.name)
            if match:
                sample_id = match.group(1)
            else:
                sample_id = report_file.stem.replace('_final_answer', '')
            
            # Check if output file already exists
            output_file = output_dir / f'id_{sample_id}_converted.json'
            if not output_file.exists():
                filtered_files.append(report_file)
        
        skipped_count = original_count - len(filtered_files)
        report_files = filtered_files
        
        if skipped_count > 0:
            print(f"⏭️  Skipped {skipped_count} existing files")
        
        if not report_files:
            print(f"✅ All files already converted, nothing to process")
            results = []
            if requested_ids is not None and require_artifacts:
                missing_outputs = [
                    task_id for task_id in requested_ids
                    if not (output_dir / f'id_{task_id}_converted.json').is_file()
                ]
                if missing_outputs:
                    raise RuntimeError(
                        "Selected converted plans are missing after conversion: "
                        + ", ".join(missing_outputs)
                    )
            return {'total': original_count, 'converted': 0, 'skipped': skipped_count, 'success': 0, 'failed': 0, 'results': results}
    
    print(f"\n{'='*80}")
    print(f"📊 Found {len(report_files)} report files to convert")
    print(f"🚀 Using {workers} concurrent workers")
    print(f"📂 Input Directory: {reports_dir}")
    print(f"📂 Output Directory: {output_dir}")
    print(f"🌐 Language: {language}")
    print(f"🤖 Conversion Model: {actual_model_name}")
    print(f"{'='*80}\n")
    
    # Create print lock
    print_lock = Lock()
    
    # Record start time
    start_time = time.time()
    
    # Use thread pool for parallel processing
    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit all tasks
        future_to_file = {}
        for report_file in report_files:
            future = executor.submit(
                process_single_report,
                report_file,
                output_dir,
                actual_model_name,
                client,
                format_prompt,
                print_lock,
                30,
                conversion_temperature,
            )
            future_to_file[future] = report_file
        
        # Collect results (in completion order)
        for future in as_completed(future_to_file):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                report_file = future_to_file[future]
                with print_lock:
                    print(f"❌ File {report_file.name} encountered uncaught exception: {e}\n")
                results.append({
                    'success': False,
                    'sample_id': report_file.name,
                    'error': str(e)
                })
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Statistics
    success_count = sum(1 for r in results if r['success'])
    failed_count = len(results) - success_count

    if requested_ids is not None:
        if require_artifacts:
            missing_outputs = [
                task_id for task_id in requested_ids
                if not (output_dir / f'id_{task_id}_converted.json').is_file()
            ]
            if missing_outputs:
                raise RuntimeError(
                    "Selected converted plans are missing after conversion: "
                    + ", ".join(missing_outputs)
                )
        result_order = {task_id: index for index, task_id in enumerate(requested_ids)}
        results.sort(key=lambda result: result_order[str(result.get('sample_id'))])
    
    print(f"\n{'='*80}")
    print(f"✅ All report conversions completed!")
    print(f"{'='*80}")
    print(f"📊 Statistics:")
    print(f"   - Total Files: {len(report_files)}")
    print(f"   - Success: {success_count}")
    print(f"   - Failed: {failed_count}")
    print(f"   - Total Time: {elapsed_time:.2f} seconds")
    print(f"   - Average Time: {elapsed_time/len(report_files):.2f} seconds/file")
    print(f"   - Output Directory: {output_dir}")
    print(f"{'='*80}\n")
    
    return {
        'total': original_count,
        'converted': success_count,
        'skipped': skipped_count,
        'success': success_count,
        'failed': failed_count,
        'results': results,
        'elapsed_time': elapsed_time,
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert report files to JSON format'
    )
    parser.add_argument('--result-dir', type=Path, required=True,
                       help='Result directory containing reports/ subdirectory')
    parser.add_argument('--language', type=str, default='zh', choices=['zh', 'en'],
                       help='Language for prompts (zh or en)')
    parser.add_argument('--workers', type=int, default=10,
                       help='Number of concurrent workers')
    parser.add_argument('--skip-existing', action='store_true',
                       help='Skip files that already have output')
    parser.add_argument('--conversion-model', default=DEFAULT_CONVERSION_MODEL,
                       help='Model configuration name for conversion')
    parser.add_argument('--task-ids', default=None,
                       help='Comma-separated exact IDs to convert')
    
    args = parser.parse_args()
    
    result = convert_reports(
        result_dir=args.result_dir,
        language=args.language,
        workers=args.workers,
        skip_existing=args.skip_existing,
        conversion_model=args.conversion_model,
        selected_ids=args.task_ids.split(',') if args.task_ids is not None else None,
    )
    
    print(f"Conversion completed: {result['success']}/{result['total']} succeeded")
