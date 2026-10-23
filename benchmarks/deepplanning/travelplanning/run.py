"""
TravelBench Integrated Runner

This script integrates three steps into a single pipeline:
1. Agent inference (generate trajectories)
2. Plan parsing/conversion
3. Evaluation

Usage:
    python run.py --model qwen-plus --language zh --workers 40
"""

import argparse
import os
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent.call_llm import load_model_config
from evaluation.convert_report import DEFAULT_CONVERSION_MODEL, convert_reports
from evaluation.eval_converted import evaluate_plans
from agent.tools_fn_agent import run_agent_inference

# Project-root languages registry.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from languages import resolve_language, UnknownLanguage, all_languages  # noqa: E402
from task_selection import (  # noqa: E402
    FULL_TASK_SUBSET,
    effective_task_subset_name,
    load_dataset_ids,
    parse_task_selector,
    resolve_task_subset,
    validate_dataset_selection,
)


def detect_missing_ids(
    directory: Path,
    file_pattern: str,
    total_ids: int = 120,
    expected_ids=None,
) -> list:
    """
    Detect missing IDs in a directory
    
    Args:
        directory: Directory to check
        file_pattern: Pattern to match files (e.g., 'id_*.txt', 'id_*_converted.json')
        total_ids: Total number of expected IDs (default: 120, i.e., id_0 to id_119)
        
    Returns:
        List of missing IDs (sorted)
    """
    expected = set(expected_ids) if expected_ids is not None else set(range(total_ids))
    if not directory.exists():
        return sorted(expected)
    
    # Get all existing IDs
    import re
    existing_ids = set()
    
    for file in directory.glob(file_pattern):
        match = re.search(r'id_(\d+)', file.name)
        if match:
            existing_ids.add(int(match.group(1)))
    
    # Find missing IDs
    missing_ids = sorted(expected - existing_ids)
    
    return missing_ids


def parse_id_list(id_str: str) -> list:
    """
    Parse ID list from string format
    
    Supports formats:
    - Single ID: "5"
    - Multiple IDs: "1,5,10"
    - Ranges: "0-10" or "0-10,15,20-25"
    
    Args:
        id_str: String containing IDs
        
    Returns:
        List of integer IDs
    """
    if id_str is None:
        return None
    return [int(task_id) for task_id in parse_task_selector(id_str, allow_ranges=True)]


def validate_rerun_ids(id_str: str, dataset_path: Path) -> list[int]:
    """Parse a selector and require every ID in the resolved language dataset."""
    selected = parse_task_selector(id_str, allow_ranges=True)
    validate_dataset_selection(selected, dataset_path)
    return [int(task_id) for task_id in selected]


def get_agent_inference_function(model: str):
    """
    Dynamically select the appropriate agent based on model type
    
    Args:
        model: Model configuration name
    
    Returns:
        run_agent_inference function for the appropriate agent type
    """
        
    return run_agent_inference



def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Run TravelBench agent inference, conversion, and evaluation'
    )
    
    # Model configuration
    parser.add_argument('--model', type=str, required=True,
                       help='Model configuration name from models_config.json')
    parser.add_argument(
        '--conversion-model',
        default=DEFAULT_CONVERSION_MODEL,
        help=(
            'Model configuration name for report conversion '
            f'(default: {DEFAULT_CONVERSION_MODEL})'
        ),
    )
    
    # Language and dataset
    parser.add_argument('--language', type=str, default=None,
                       help='Language switch_key (e.g. "english", "japanese", "eastern_panjabi") '
                            'or short code (e.g. "ja", "fr"). '
                            'Default: run both zh and en (the baseline languages).')
    
    # Execution configuration
    parser.add_argument('--workers', type=int, default=10,
                       help='Number of concurrent workers (default: 10)')
    parser.add_argument('--max-llm-calls', type=int, default=150,
                       help='Maximum LLM calls per sample (default: 150)')
    
    # Output configuration
    parser.add_argument('--output-dir', type=str, default=None,
                       help='Output directory for results (default: results/{model}_{timestamp})')
    parser.add_argument('--save-intermediate', action='store_true',
                       help='Save intermediate results after each step')
    
    # Pipeline control
    parser.add_argument('--start-from', type=str, default='inference',
                       choices=['inference', 'conversion', 'evaluation'],
                       help='Which step to start from (default: inference = run all steps)')
    
    # Rerun specific IDs
    parser.add_argument('--rerun-ids', type=str, default=None,
                       help='Comma-separated list of IDs to rerun (e.g., "0,5,10" or "0-10,15,20-25")')

    # Named frozen case subset (shared across all languages)
    parser.add_argument('--task-subset', type=str, default=None,
                       help="Named pre-sampled case subset under task_subsets/ "
                            "(default: $BENCHMARK_TASK_SUBSET or 'standard' — a fixed "
                            "60-of-120 list identical across all languages). "
                            "Pass 'full' to run the complete task set. "
                            "Ignored when --rerun-ids is given.")
    
    # Advanced options
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    
    args = parser.parse_args()
    return args


def setup_paths(args):
    """Setup paths for input/output directories.

    args.language at this point is the LanguageSpec.code (e.g. 'zh','en','ja').
    For baseline languages (zh, en) we use database_<code>/. For non-baseline
    languages we use database_<canonical_db_code>/ (database_en by default —
    the English-canonical layer).
    """
    base_dir = Path(__file__).parent

    # Resolve the LanguageSpec for routing decisions.
    spec = resolve_language(args.language)
    if spec is None:
        raise ValueError(
            f"Internal error: setup_paths called with unresolved language {args.language!r}"
        )
    lang_code = spec.code

    # Test data path — per-language query file.
    args.test_data = base_dir / 'data' / f'travelplanning_query_{lang_code}.json'

    if not args.test_data.exists():
        raise FileNotFoundError(
            f"Test data file not found: {args.test_data}\n"
            f"Language {spec.display} is not yet translated. Run:\n"
            f"  (data for {spec.switch_key} is missing -- re-check the data download)"
        )

    # Output directory
    user_output_dir = getattr(args, '_user_output_dir', None)
    dir_name = f"{args.model}_{lang_code}"
    benchmark_version = os.environ.get('BENCHMARK_VERSION', 'v8')

    if user_output_dir is None:
        args.output_dir = base_dir / 'results' / benchmark_version / dir_name
    else:
        args.output_dir = Path(user_output_dir) / dir_name

    # Create output directories
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'trajectories').mkdir(exist_ok=True)
    (args.output_dir / 'reports').mkdir(exist_ok=True)
    (args.output_dir / 'converted_plans').mkdir(exist_ok=True)
    (args.output_dir / 'evaluation').mkdir(exist_ok=True)

    # Database path — for non-baseline languages, reuse the canonical DB.
    from data_paths import travel_database_dir  # noqa: E402
    args.database_dir = travel_database_dir(spec.canonical_db_code)

    # Tool schema path — per-language file.
    args.tool_schema_path = base_dir / 'tools' / f'tool_schema_{lang_code}.json'
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
    print("TravelBench Integrated Runner")
    print("=" * 80)
    print(f"Model:              {args.model}")
    print(f"Conversion model:   {args.conversion_model}")
    print(f"Language:           {args.language}")
    if getattr(args, '_task_subset_display', None):
        print(f"Task subset:        {args._task_subset_display}")
    print(f"Workers:            {args.workers}")
    print(f"Max LLM calls:      {args.max_llm_calls}")
    print(f"Test data:          {args.test_data}")
    print(f"Output directory:   {args.output_dir}")
    print(f"Database directory: {args.database_dir}")
    print(f"Tool schema:        {args.tool_schema_path}")
    
    # Pipeline steps
    steps = []
    if args.start_from == 'inference':
        steps = ["1. Inference", "2. Conversion", "3. Evaluation"]
    elif args.start_from == 'conversion':
        steps = ["2. Conversion", "3. Evaluation"]
    elif args.start_from == 'evaluation':
        steps = ["3. Evaluation"]
    
    print(f"Pipeline steps:     {' → '.join(steps)}")
    print(f"Start from:         {args.start_from.capitalize()}")
    print("=" * 80)
    print()


def run_step_inference(args):
    """Step 1: Run agent inference to generate trajectories"""
    print("\n" + "=" * 80)
    print("STEP 1: Agent Inference")
    print("=" * 80)
    
    # Auto-detect missing reports if not explicitly specifying rerun_ids
    rerun_ids = None
    if args.rerun_ids is not None:
        # User explicitly specified IDs to rerun
        rerun_ids = args.selected_task_ids
        print(f"  🔄 User-specified IDs to rerun: {rerun_ids}")
        print(f"  📝 Total IDs: {len(rerun_ids)}")
    else:
        # Auto-detect missing reports
        reports_dir = args.output_dir / 'reports'
        missing_ids = detect_missing_ids(
            reports_dir, 'id_*.txt', expected_ids=args.dataset_task_ids
        )
        
        if missing_ids:
            rerun_ids = missing_ids
            print(f"  🔍 Auto-detected missing reports")
            print(f"  📝 Missing IDs ({len(missing_ids)}): {missing_ids[:10]}{'...' if len(missing_ids) > 10 else ''}")
            print(f"  🔄 Will regenerate reports for these IDs")
        else:
            print(f"  ✅ All {len(args.dataset_task_ids)} reports already exist")
            print(f"  ⏭️  Skipping inference step")
            total = len(args.dataset_task_ids)
            return True, {'total': total, 'success': total, 'failed': 0, 'cached': total, 'processed': 0}
    
    start_time = time.time()
    
    try:
        # Dynamically select the appropriate agent
        run_agent_inference = get_agent_inference_function(args.model)
        
        results = run_agent_inference(
            model=args.model,
            language=args.language,
            test_data_path=args.test_data,
            database_dir=args.database_dir,
            tool_schema_path=args.tool_schema_path,
            output_dir=args.output_dir,
            workers=args.workers,
            max_llm_calls=args.max_llm_calls,
            rerun_ids=rerun_ids,  # Pass rerun_ids parameter
        )
        if rerun_ids is not None and results.get('total') != len(rerun_ids):
            raise RuntimeError(
                f"Inference processed {results.get('total')} tasks, "
                f"but {len(rerun_ids)} were requested"
            )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Inference completed in {elapsed:.2f}s")
        print(f"   Total samples: {results['total']}")
        print(f"   Success: {results['success']}")
        print(f"   Failed: {results['failed']}")
        if 'cached' in results and results.get('cached', 0) > 0:
            print(f"   Cached: {results['cached']}")
            print(f"   Newly processed: {results.get('processed', 0)}")
        
        return True, results
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Inference failed after {elapsed:.2f}s: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return False, None


def run_step_conversion(args):
    """Step 2: Convert reports to standardized plan format"""
    print("\n" + "=" * 80)
    print("STEP 2: Plan Conversion")
    print("=" * 80)
    
    converted_plans_dir = args.output_dir / 'converted_plans'
    expected_ids = (
        args.selected_task_ids
        if args.selected_task_ids is not None
        else args.dataset_task_ids
    )
    missing_ids = detect_missing_ids(
        converted_plans_dir,
        'id_*_converted.json',
        expected_ids=expected_ids,
    )

    if args.selected_task_ids is not None:
        if missing_ids:
            print(f"  🔍 Selected converted plans missing: {missing_ids}")
        else:
            print(f"  ✅ All {len(expected_ids)} selected plans already converted")
        # Still enter convert_reports so it can validate that the exact source
        # reports exist before accepting cached converted plans.
    elif missing_ids:
        print(f"  🔍 Auto-detected missing converted plans")
        print(f"  📝 Missing IDs ({len(missing_ids)}): {missing_ids[:10]}{'...' if len(missing_ids) > 10 else ''}")
        print(f"  🔄 Will convert reports for these IDs")
    else:
        print(f"  ✅ All {len(expected_ids)} plans already converted")
        print(f"  ⏭️  Skipping conversion step")
        total = len(expected_ids)
        return True, {'total': total, 'converted': 0, 'skipped': total}
    
    start_time = time.time()
    
    try:
        # Always use skip_existing=True to only convert missing files
        results = convert_reports(
            result_dir=args.output_dir,
            language=args.language,
            workers=args.workers,
            skip_existing=True,
            verbose=args.verbose,
            conversion_model=args.conversion_model,
            selected_ids=args.selected_task_ids,
            # Explicit --rerun-ids keeps the strict artifact contract; the
            # task-subset default mirrors the full-run protocol (absent
            # reports score 0 downstream instead of aborting the language).
            require_artifacts=args.rerun_ids is not None,
        )
        if (
            args.rerun_ids is not None
            and args.selected_task_ids is not None
            and results.get('total') != len(args.selected_task_ids)
        ):
            raise RuntimeError(
                f"Conversion covered {results.get('total')} tasks, "
                f"but {len(args.selected_task_ids)} were requested"
            )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Conversion completed in {elapsed:.2f}s")
        print(f"   Total files: {results['total']}")
        print(f"   Converted: {results['converted']}")
        print(f"   Skipped: {results['skipped']}")
        
        return True, results
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Conversion failed after {elapsed:.2f}s: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return False, None


def run_step_evaluation(args):
    """Step 3: Evaluate converted plans"""
    print("\n" + "=" * 80)
    print("STEP 3: Plan Evaluation")
    print("=" * 80)
    print(f"  Language: {args.language}")
    print(f"  Database directory: {args.database_dir}")
    print(f"  Test data: {args.test_data}")
    if args.selected_task_ids is None:
        print(f"  📊 Will evaluate the complete {len(args.dataset_task_ids)}-task dataset")
    else:
        print(f"  📊 Will evaluate selected task IDs: {args.selected_task_ids}")
    print()
    
    start_time = time.time()
    
    try:
        results = evaluate_plans(
            result_dir=args.output_dir,
            test_data_path=args.test_data,
            database_dir=args.database_dir,
            verbose=args.verbose,
            selected_ids=args.selected_task_ids,
            require_artifacts=args.rerun_ids is not None,
        )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Evaluation completed in {elapsed:.2f}s")
        print(f"   Total plans: {results['total']}")
        print(f"   Average score: {results['average_score']:.2f}")
        print(f"   Pass rate: {results['pass_rate']:.1f}%")
        
        return True, results
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Evaluation failed after {elapsed:.2f}s: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return False, None


def print_final_summary(args, inference_results, conversion_results, eval_results):
    """Print final summary of all steps"""
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    
    if inference_results:
        print(f"Inference:  {inference_results['success']}/{inference_results['total']} succeeded")
    
    if conversion_results:
        print(f"Conversion: {conversion_results['converted']}/{conversion_results['total']} converted")
    
    if eval_results:
        print(f"Evaluation: Average score = {eval_results['average_score']:.2f}")
        print(f"            Pass rate = {eval_results['pass_rate']:.1f}%")
    
    print(f"\nResults saved to: {args.output_dir}")
    print("=" * 80)


def run_single_language(args, language):
    """Run pipeline for a single language"""
    # Update args with specific language
    args.language = language
    args = setup_paths(args)
    args.dataset_task_ids = [int(task_id) for task_id in load_dataset_ids(args.test_data)]
    dataset_total = len(args.dataset_task_ids)
    subset_name = effective_task_subset_name(getattr(args, 'task_subset', None))
    if args.rerun_ids is not None:
        try:
            args.selected_task_ids = validate_rerun_ids(args.rerun_ids, args.test_data)
        except ValueError as exc:
            print(f"❌ Invalid --rerun-ids: {exc}")
            return False, None, None, None
        if subset_name.lower() != FULL_TASK_SUBSET:
            print(f"📎 Explicit --rerun-ids given: ignoring task subset '{subset_name}'")
        args._task_subset_display = "(ignored — explicit --rerun-ids)"
    else:
        try:
            subset_ids = resolve_task_subset(subset_name, "travel")
            if subset_ids is not None:
                validate_dataset_selection(subset_ids, args.test_data)
        except ValueError as exc:
            print(f"❌ Invalid --task-subset: {exc}")
            return False, None, None, None
        if subset_ids is None:
            args.selected_task_ids = None
            args._task_subset_display = f"{FULL_TASK_SUBSET} (all {dataset_total} cases)"
        else:
            # Narrow both the expected dataset (drives inference auto-resume)
            # and the selected set (drives conversion/evaluation scope and the
            # score denominators) to the frozen subset, in dataset order.
            subset_set = {int(task_id) for task_id in subset_ids}
            args.dataset_task_ids = [
                task_id for task_id in args.dataset_task_ids if task_id in subset_set
            ]
            args.selected_task_ids = list(args.dataset_task_ids)
            args._task_subset_display = (
                f"{subset_name} ({len(args.selected_task_ids)}/{dataset_total} cases)"
            )
            print(
                f"📎 Task subset '{subset_name}': running "
                f"{len(args.selected_task_ids)}/{dataset_total} cases "
                f"(pass --task-subset {FULL_TASK_SUBSET} for the complete set)"
            )

    # Resolve every model configuration needed by this invocation before the
    # first request. In a full run this validates conversion independently of
    # inference, while evaluation-only runs need no model configuration.
    try:
        if args.start_from == 'inference':
            load_model_config(args.model)
        if args.start_from in ('inference', 'conversion'):
            load_model_config(args.conversion_model)
    except (FileNotFoundError, ValueError) as exc:
        print(f"❌ Model configuration preflight failed: {exc}")
        return False, None, None, None
    
    print_config(args)
    
    lang_start_time = time.time()
    
    inference_results = None
    conversion_results = None
    eval_results = None
    
    # Step 1: Inference
    if args.start_from == 'inference':
        success, inference_results = run_step_inference(args)
        if not success:
            print("\n⚠️  Inference failed, skipping subsequent steps")
            return False, None, None, None
    
    # Step 2: Conversion
    if args.start_from in ['inference', 'conversion']:
        success, conversion_results = run_step_conversion(args)
        if not success:
            print("\n⚠️  Conversion failed, skipping evaluation")
            return False, inference_results, None, None
    
    # Step 3: Evaluation
    if args.start_from in ['inference', 'conversion', 'evaluation']:
        success, eval_results = run_step_evaluation(args)
        if not success:
            print("\n⚠️  Evaluation failed")
            return False, inference_results, conversion_results, None
    
    # Print summary for this language
    lang_elapsed = time.time() - lang_start_time
    print_final_summary(args, inference_results, conversion_results, eval_results)
    print(f"\n✅ Model '{args.model}' | Language '{language}' completed in {lang_elapsed:.2f}s ({lang_elapsed/60:.1f} minutes)")
    
    return True, inference_results, conversion_results, eval_results


def main():
    """Main execution function"""
    args = parse_args()
    
    # Save user-specified output_dir (if any) before it gets modified
    # This allows language-specific directories to be generated for multi-language runs
    args._user_output_dir = args.output_dir
    
    overall_start_time = time.time()
    
    # Determine which languages to run.
    # `args.language` is the raw CLI input. Resolve through the registry.
    if args.language is None:
        # Legacy default: run both baseline languages.
        languages = ['zh', 'en']
        print("=" * 80)
        print("Running for both baseline languages: zh and en")
        print("(Pass --language <name> to run a specific language.)")
        print("=" * 80)
        print()
    else:
        try:
            spec = resolve_language(args.language)
        except UnknownLanguage as e:
            print(f"❌ {e}")
            sys.exit(2)
        if spec is None:
            print("❌ --language was supplied but resolved to None (empty string?).")
            sys.exit(2)
        languages = [spec.code]
    
    # Run for each language
    all_success = True
    for idx, lang in enumerate(languages):
        if len(languages) > 1:
            print("\n" + "=" * 80)
            print(f"LANGUAGE {idx + 1}/{len(languages)}: {lang.upper()}")
            print("=" * 80)
            print()
        
        success, inf_res, conv_res, eval_res = run_single_language(args, lang)
        
        if not success:
            all_success = False
            print(f"\n❌ Pipeline failed for language '{lang}'")
            if len(languages) > 1 and idx < len(languages) - 1:
                print(f"Continuing with next language...\n")
                continue
            else:
                sys.exit(1)
    
    # Print overall summary
    overall_elapsed = time.time() - overall_start_time
    print("\n" + "=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)
    print(f"Languages run: {', '.join(languages)}")
    print(f"Total time: {overall_elapsed:.2f}s ({overall_elapsed/60:.1f} minutes)")
    print("=" * 80)
    
    if all_success:
        print("\n✅ All pipelines completed successfully!")
    else:
        print("\n⚠️  Some pipelines failed. Check logs above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
