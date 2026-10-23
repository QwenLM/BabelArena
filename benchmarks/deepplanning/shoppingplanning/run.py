"""
ShoppingBench Integrated Runner

This script runs shopping agent inference for different levels.

Usage:
    python run.py --model qwen-plus --level 1 --workers 40
"""

import argparse
import os
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

from agent.shopping_agent import run_agent_inference
from agent.prompts import get_system_prompt

sys.path.insert(0, str(Path(__file__).parent))

# Project-root language registry.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from languages import resolve_language, UnknownLanguage  # noqa: E402
from task_selection import (  # noqa: E402
    FULL_TASK_SUBSET,
    effective_task_subset_name,
    parse_task_selector,
    resolve_task_subset,
    validate_case_directories,
    validate_dataset_selection,
)


def validate_rerun_ids(selector: str, dataset_path: Path, database_dir: Path) -> list[str]:
    """Validate exact IDs against both the query data and staged case folders."""
    selected = parse_task_selector(selector)
    validate_dataset_selection(selected, dataset_path)
    validate_case_directories(selected, database_dir)
    return list(selected)


def resolve_selected_task_ids(args) -> tuple:
    """Case selection: explicit --rerun-ids wins, else the named task subset.

    Returns (selected_task_ids or None, human-readable subset display).
    Raises ValueError (message already prefixed with the offending flag).
    """
    subset_name = effective_task_subset_name(getattr(args, 'task_subset', None))
    if args.rerun_ids is not None:
        try:
            selected = validate_rerun_ids(
                args.rerun_ids, args.test_data, args.database_dir
            )
        except ValueError as exc:
            raise ValueError(f"Invalid --rerun-ids: {exc}") from exc
        if subset_name.lower() != FULL_TASK_SUBSET:
            print(f"📎 Explicit --rerun-ids given: ignoring task subset '{subset_name}'")
        return selected, "(ignored — explicit --rerun-ids)"

    try:
        subset_ids = resolve_task_subset(subset_name, f"shopping_level{args.level}")
        if subset_ids is not None:
            validate_dataset_selection(subset_ids, args.test_data)
            validate_case_directories(subset_ids, args.database_dir)
    except ValueError as exc:
        raise ValueError(f"Invalid --task-subset: {exc}") from exc
    if subset_ids is None:
        return None, f"{FULL_TASK_SUBSET} (all cases)"
    print(
        f"📎 Task subset '{subset_name}': running {len(subset_ids)} "
        f"level-{args.level} cases "
        f"(pass --task-subset {FULL_TASK_SUBSET} for the complete set)"
    )
    return list(subset_ids), f"{subset_name} ({len(subset_ids)} level-{args.level} cases)"


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Run ShoppingBench agent inference'
    )

    # Model configuration
    parser.add_argument('--model', type=str, default=None,
                       help='Model name (default: from SHOPPING_AGENT_MODEL env or qwen-plus)')

    # Level configuration
    parser.add_argument('--level', type=int, default=1, choices=[1, 2, 3],
                       help='Task level, determines input file and system prompt (default: 1)')

    # Language configuration. English is the baseline (the existing un-suffixed
    # files). Other languages live under data/level_{N}_query_meta_<code>.json
    # and tools/shopping_tool_schema_<code>.json.
    parser.add_argument('--language', type=str, default=None,
                       help='Language switch_key (e.g. "english", "japanese", "eastern_panjabi") '
                            'or short code (e.g. "ja", "fr"). '
                            'Default: english (the baseline).')
    
    # Execution configuration
    parser.add_argument('--workers', type=int, default=5,
                       help='Number of concurrent workers (default: 5)')
    parser.add_argument('--max-llm-calls', type=int, default=400,
                       help='Maximum LLM calls per sample (default: 400). NOTE: the agent '
                            'additionally hard-caps the effective budget at '
                            'BENCHMARK_SHOPPING_HARD_CALL_CAP (default 60), so the '
                            'per-case ceiling is min(this, that cap).')
    
    # Database configuration (for concurrent run isolation)
    parser.add_argument('--database-dir', type=str, default=None,
                       help='Path to database directory (default: database/). Use unique paths to allow concurrent runs.')
    
    # Advanced options
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    parser.add_argument('--rerun-ids', type=str, default=None,
                       help='Comma-separated case IDs to re-run only (e.g. "41" or "7,12,41"). '
                            'Other cases are skipped; existing artifacts in --database-dir are preserved.')
    parser.add_argument('--task-subset', type=str, default=None,
                       help="Named pre-sampled case subset under ../task_subsets/ "
                            "(default: $BENCHMARK_TASK_SUBSET or 'standard' — a fixed "
                            "per-level list identical across all languages: 25/25/10 "
                            "cases for levels 1/2/3). Pass 'full' to run every case. "
                            "Ignored when --rerun-ids is given.")

    args = parser.parse_args()
    return args
def setup_paths(args):
    """Setup paths for input/output directories.

    `args.language_spec` is set from --language (or environment, or default
    English). Baseline English uses the un-suffixed legacy filenames so old
    runs keep working. Other languages use suffixed siblings.
    """
    base_dir = Path(__file__).parent
    spec = args.language_spec  # set in main() before this is called

    # Test data path — un-suffixed for English baseline, suffixed otherwise.
    if spec.code == 'en':
        args.test_data = base_dir / 'data' / f'level_{args.level}_query_meta.json'
    else:
        args.test_data = base_dir / 'data' / f'level_{args.level}_query_meta_{spec.code}.json'

    if not args.test_data.exists():
        raise FileNotFoundError(
            f"Test data file not found: {args.test_data}\n"
            f"Language {spec.display} is not yet translated. Run:\n"
            f"  (data for {spec.switch_key} is missing -- re-check the data download)"
        )

    # Database path — per-language localized when shopping_canonical_db_code != "en".
    if args.database_dir:
        db_path = Path(args.database_dir)
        if not db_path.is_absolute():
            db_path = base_dir / db_path
        args.database_dir = db_path
    else:
        # Default tool path (un-prefixed legacy) — used only when run.sh has not
        # already pointed --database-dir at a per-run copy. We resolve to the
        # language-specific seed directory and let run.sh do the per-run copy.
        from data_paths import shopping_seed_dir  # noqa: E402
        args.database_dir = shopping_seed_dir(args.level, spec.shopping_canonical_db_code)

    if not args.database_dir.exists():
        raise FileNotFoundError(
            f"Shopping DB for language {spec.display} ({spec.shopping_canonical_db_code}) "
            f"not found at {args.database_dir}.\n"
            f"Check the data download (DEEPPLANNING_DATA_DIR={__import__('os').getenv('DEEPPLANNING_DATA_DIR', '<unset>')})."
        )

    # Tool schema path — un-suffixed for English, suffixed otherwise.
    if spec.code == 'en':
        args.tool_schema_path = base_dir / 'tools' / 'shopping_tool_schema.json'
    else:
        args.tool_schema_path = base_dir / 'tools' / f'shopping_tool_schema_{spec.code}.json'

    if not args.tool_schema_path.exists():
        raise FileNotFoundError(
            f"Tool schema file not found: {args.tool_schema_path}\n"
            f"Language {spec.display} is not yet translated. Run:\n"
            f"  (data for {spec.switch_key} is missing -- re-check the data download)"
        )

    return args
def print_config(args):
    """Print configuration summary"""
    print("=" * 80)
    print("ShoppingBench Integrated Runner")
    print("=" * 80)
    print(f"Model:              {args.model}")
    print(f"Level:              {args.level}")
    print(f"Language:           {args.language_spec.display} ({args.language_spec.code})")
    if getattr(args, '_task_subset_display', None):
        print(f"Task subset:        {args._task_subset_display}")
    print(f"Workers:            {args.workers}")
    print(f"Max LLM calls:      {args.max_llm_calls}")
    print(f"Test data:          {args.test_data}")
    print(f"Database directory: {args.database_dir}")
    print(f"Tool schema:        {args.tool_schema_path}")
    print("=" * 80)
    print()
def run_step_inference(args):
    """Run agent inference to generate trajectories"""
    # Get language-aware system prompt via strict resolver.
    try:
        system_prompt = get_system_prompt(args.level, args.language_spec.switch_key)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return False, None

    start_time = time.time()
    
    try:
        rerun_ids = args.selected_task_ids
        if rerun_ids is not None:
            print(f"🔁 Rerun mode: only processing case IDs {rerun_ids}")

        result = run_agent_inference(
            model=args.model,
            test_data_path=args.test_data,
            database_dir=args.database_dir,
            tool_schema_path=args.tool_schema_path,
            system_prompt=system_prompt,
            workers=args.workers,
            max_llm_calls=args.max_llm_calls,
            language=args.language_spec.code,
            rerun_ids=rerun_ids,
        )
        if rerun_ids is not None and result.get('total') != len(rerun_ids):
            raise RuntimeError(
                f"Inference processed {result.get('total')} tasks, "
                f"but {len(rerun_ids)} were requested"
            )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Inference completed in {elapsed:.2f}s")
        print(f"   Total samples: {result['total']}")
        print(f"   Success: {result['success']}")
        print(f"   Failed: {result['failed']}")
        
        return True, {
            'total': result['total'],
            'success': result['success'],
            'failed': result['failed']
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Inference failed after {elapsed:.2f}s: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return False, None


def run_tokenizer_preflight(language_switch_key: str) -> None:
    """Import the search tool's tokenizer and tokenize once, failing fast.

    The tool modules use flat imports (``from base_shopping_tool import ...``)
    that only resolve once the tools directory itself is on sys.path — the
    same bootstrap run_agent_inference's pre-warm block performs later.
    Replicate it here, because this preflight runs first; without it the
    import dies with ModuleNotFoundError instead of reporting a real
    tokenizer problem.
    """
    base_dir = Path(__file__).resolve().parent
    for path in (base_dir / 'tools', base_dir):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    from tools.search_products_tool import _resolve_tokenize_fn

    _resolve_tokenize_fn(language_switch_key)("tokenizer preflight")


def main():
    """Main execution function"""
    args = parse_args()

    # Set default model if not provided
    if args.model is None:
        args.model = os.getenv('SHOPPING_AGENT_MODEL', 'qwen-plus')

    # Resolve language: CLI flag wins, then env vars, then English default.
    lang_input = args.language
    if lang_input is None:
        lang_input = (os.environ.get('DEEPPLANNING_LANGUAGE')
                      or os.environ.get('BENCHMARK_LANGUAGE')
                      or '').strip() or None
    try:
        spec = resolve_language(lang_input) if lang_input else resolve_language('english')
    except UnknownLanguage as e:
        print(f"❌ {e}")
        sys.exit(2)
    if spec is None:
        spec = resolve_language('english')
    args.language_spec = spec

    # Setup paths
    args = setup_paths(args)
    try:
        args.selected_task_ids, args._task_subset_display = (
            resolve_selected_task_ids(args)
        )
    except ValueError as exc:
        print(f"❌ {exc}")
        sys.exit(2)

    # Fail before inference (and therefore before any LLM request) when a
    # non-whitespace language needs a tokenizer that setup did not prepare.
    try:
        run_tokenizer_preflight(args.language_spec.switch_key)
    except Exception as exc:
        print(f"❌ Shopping tokenizer preflight failed: {exc}")
        sys.exit(2)

    # Print configuration
    print_config(args)
    
    overall_start_time = time.time()
    
    # Run inference
    success, inference_results = run_step_inference(args)
    
    if not success:
        print("\n❌ Inference failed")
        sys.exit(1)
    
    # Print final summary
    overall_elapsed = time.time() - overall_start_time
    print(f"\nTotal time: {overall_elapsed:.2f}s ({overall_elapsed/60:.1f} minutes)")
    
    print("\n✅ Pipeline completed successfully!")
if __name__ == '__main__':
    main()
    # HF tokenizers / thread-pool atexit teardown intermittently deadlocks
    # (all threads in futex_wait, 0 CPU) even with TOKENIZERS_PARALLELISM=false,
    # hanging the process forever AFTER every case's data is already written.
    # run_step_inference flushes all results synchronously above, and run.sh's
    # evaluation step is a separate process, so force an immediate clean exit to
    # skip the deadlocking interpreter teardown. Failures take the sys.exit(N)
    # paths inside main() and never reach here.
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
