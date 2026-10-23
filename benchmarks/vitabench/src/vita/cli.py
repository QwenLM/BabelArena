import argparse
from typing import get_args

from vita.config import (
    DEFAULT_AGENT_IMPLEMENTATION,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_CONCURRENCY,
    DEFAULT_MAX_ERRORS,
    DEFAULT_MAX_STEPS,
    DEFAULT_NUM_TRIALS,
    DEFAULT_SEED,
    DEFAULT_USER_IMPLEMENTATION,
    DEFAULT_EVALUATION_TYPE,
    DEFAULT_LANGUAGE,
    DEFAULT_LLM_AGENT,
    DEFAULT_LLM_USER,
    DEFAULT_LLM_EVALUATOR,
    models,
)
from vita.data_model.simulation import RunConfig, EvaluationType
from vita.run import get_options, run_domain
from vita.utils.utils import DATA_DIR

DEFAULT_TASK_SUBSET = "standard"


def add_run_args(parser):
    """Add run arguments to a parser."""
    parser.add_argument(
        "--domain",
        "-d",
        type=str,
        default="delivery,instore,ota",
        help="The domain to run the simulation on",
    )
    parser.add_argument(
        "--num-trials",
        type=int,
        default=DEFAULT_NUM_TRIALS,
        help="The number of times each task is run. Default is 1.",
    )
    parser.add_argument(
        "--agent",
        type=str,
        default=DEFAULT_AGENT_IMPLEMENTATION,
        choices=get_options().agents,
        help=f"The agent implementation to use. Default is {DEFAULT_AGENT_IMPLEMENTATION}.",
    )
    parser.add_argument(
        "--agent-llm",
        type=str,
        default=DEFAULT_LLM_AGENT,
        help=f"The LLM to use for the agent. Default is {DEFAULT_LLM_AGENT}.",
    )
    parser.add_argument(
        "--agent-llm-args",
        type=dict,
        default={},
        help=f"The arguments to pass to the LLM for the agent.",
    )
    parser.add_argument(
        "--user",
        type=str,
        choices=get_options().users,
        default=DEFAULT_USER_IMPLEMENTATION,
        help=f"The user implementation to use. Default is {DEFAULT_USER_IMPLEMENTATION}.",
    )
    parser.add_argument(
        "--user-llm",
        type=str,
        default=DEFAULT_LLM_USER,
        help=f"The LLM to use for the user. Default is {DEFAULT_LLM_USER}.",
    )
    parser.add_argument(
        "--user-llm-args",
        type=dict,
        default={},
        help=f"The arguments to pass to the LLM for the user.",
    )
    parser.add_argument(
        "--task-set-name",
        type=str,
        default=None,
        choices=get_options().task_sets,
        help="The task set to run the simulation on. If not provided, will load default task set for the domain.",
    )
    parser.add_argument(
        "--task-ids",
        type=str,
        nargs="+",
        help="(Optional) run only the tasks with the given IDs. If not provided, will run num_tasks tasks.",
    )
    parser.add_argument(
        "--task-ids-file",
        type=str,
        default=None,
        help="(Optional) path to a file with one task ID per line (blank lines/# comments ignored). "
             "Runs only those tasks — used for pre-sampled cross-language-parallel subsets. "
             "Overridden by --task-ids if both are given.",
    )
    parser.add_argument(
        "--task-subset",
        type=str,
        default=None,
        help="(Optional) named pre-sampled subset. Defaults to 'standard' — a fixed "
             "50-of-100 tasks per domain, identical across all languages (parallel). "
             "Pass 'full' to run the complete task set. Auto-resolves to "
             "data/task_subsets/<name>/<domain>.txt for the current --domain (cross domains -> cross.txt). "
             "Precedence: --task-ids > --task-ids-file > --task-subset.",
    )
    parser.add_argument(
        "--num-tasks",
        type=int,
        default=None,
        help="The number of tasks to run.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=DEFAULT_MAX_STEPS,
        help=f"The maximum number of steps to run the simulation. Default is {DEFAULT_MAX_STEPS}.",
    )
    parser.add_argument(
        "--evaluation-type",
        type=str,
        default=DEFAULT_EVALUATION_TYPE,
        choices=get_args(EvaluationType),
        help=f"The type of evaluation to use. Choices: trajectory, trajectory_full_traj_rubric, trajectory_sliding_wo_rubric, trajectory_full_traj_wo_rubric.",
    )
    parser.add_argument(
        "--evaluator-llm",
        type=str,
        default=DEFAULT_LLM_EVALUATOR,
        help=f"The LLM to use for evaluation. Default is {DEFAULT_LLM_EVALUATOR}.",
    )
    parser.add_argument(
        "--evaluator-llm-args",
        type=dict,
        default={},
        help=f"The arguments to pass to the LLM for evaluation",
    )
    parser.add_argument(
        "--max-errors",
        type=int,
        default=DEFAULT_MAX_ERRORS,
        help=f"The maximum number of tool errors allowed in a row in the simulation. Default is {DEFAULT_MAX_ERRORS}.",
    )
    parser.add_argument(
        "--save-to",
        type=str,
        required=False,
        help="The path to save the simulation results. Will be saved to data/simulations/<save_to>.json. If not provided, will save to <domain>_<agent>_<user>_<llm_agent>_<llm_user>_<timestamp>.json. If the file already exists, it will try to resume the run.",
    )
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=DEFAULT_MAX_CONCURRENCY,
        help=f"The maximum number of concurrent simulations to run. Default is {DEFAULT_MAX_CONCURRENCY}.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"The seed to use for the simulation. Default is {DEFAULT_SEED}.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=DEFAULT_LOG_LEVEL,
        help=f"The log level to use for the simulation. Default is {DEFAULT_LOG_LEVEL}.",
    )
    parser.add_argument(
        "--re-evaluate-file",
        type=str,
        help="Path to simulation file for re-evaluation mode. If provided, will re-evaluate the simulations from this file instead of running new ones.",
    )
    parser.add_argument(
        "--csv-output",
        type=str,
        help="Path to CSV file to append results. If provided, will append all simulation results to this CSV file after completion.",
    )
    parser.add_argument(
        "--enable-think",
        action="store_true",
        help="Enable think mode for the agent. Default is False.",
    )
    parser.add_argument(
        "--language",
        type=str,
        choices=["chinese", "english", "japanese", "french", "russian", "arabic", "hindi", "thai", "spanish",
                 "korean", "indonesian", "hebrew", "turkish", "vietnamese", "malay", "belarusian", "punjabi",
                 "kazakh", "khmer", "burmese", "lao", "tamil", "telugu"],
        default=DEFAULT_LANGUAGE,
        help="The language to use for prompts and tasks. Choices: chinese, english, japanese, french, russian, arabic, hindi, thai, spanish. Default is chinese.",
    )
    parser.add_argument(
        "--re-run",
        action="store_true",
        help="Re-run tasks specified by --task-ids. If used with --re-evaluate-file, will re-run specified tasks and then re-evaluate all tasks together.",
    )
    


def _read_ids_file(path):
    with open(path) as f:
        ids = [ln.strip() for ln in f if ln.strip() and not ln.lstrip().startswith("#")]
    if not ids:
        raise ValueError(f"task-ids file {path} is empty or contains only comments")
    return ids


def _resolve_task_ids(args):
    """Precedence: --task-ids > --task-ids-file > --task-subset.
    --task-subset <name> resolves to data/task_subsets/<name>/<domain>.txt for the
    current --domain (comma-separated cross-domain -> cross.txt). Defaults to the
    'standard' subset when none of the three flags is given; pass 'full' to run
    the complete task set."""
    if getattr(args, "task_ids", None):
        return args.task_ids
    path = getattr(args, "task_ids_file", None)
    if path:
        return _read_ids_file(path)
    subset = getattr(args, "task_subset", None)
    if subset is None:
        # Re-evaluation loads its tasks from the simulation file; injecting the
        # default subset here would make --re-run silently re-run 50 tasks.
        if getattr(args, "re_evaluate_file", None):
            return None
        subset = DEFAULT_TASK_SUBSET
    if subset.lower() == "full":
        return None
    dom = getattr(args, "domain", "") or ""
    key = "cross" if "," in dom else dom
    # Resolve against the repo's data dir (like task loading does), not the cwd.
    path = DATA_DIR / "task_subsets" / subset / f"{key}.txt"
    if not path.exists():
        raise ValueError(f"--task-subset {subset}: {path} not found (domain={dom})")
    return _read_ids_file(path)


def main():
    parser = argparse.ArgumentParser(description="vita command line interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a benchmark")
    add_run_args(run_parser)
    run_parser.set_defaults(
        func=lambda args: run_domain(
            RunConfig(
                domain=args.domain,
                task_set_name=args.task_set_name,
                task_ids=_resolve_task_ids(args),
                num_tasks=args.num_tasks,
                agent=args.agent,
                llm_agent=args.agent_llm,
                llm_args_agent=args.agent_llm_args if args.agent_llm_args else models.get(args.agent_llm, {}),
                user=args.user,
                llm_user=args.user_llm,
                llm_args_user=args.user_llm_args if args.user_llm_args else models.get(args.user_llm, {}),
                num_trials=args.num_trials,
                max_steps=args.max_steps,
                evaluation_type=args.evaluation_type,
                llm_evaluator=args.evaluator_llm,
                llm_args_evaluator=args.evaluator_llm_args if args.evaluator_llm_args else models.get(args.evaluator_llm, {}),
                max_errors=args.max_errors,
                save_to=args.save_to,
                max_concurrency=args.max_concurrency,
                seed=args.seed,
                log_level=args.log_level,
                re_evaluate_file=getattr(args, 're_evaluate_file', None),
                csv_output_file=getattr(args, 'csv_output', None),
                enable_think=args.enable_think,
                language=args.language,
                re_run=getattr(args, 're_run', False)
            )
        )
    )

    # View command
    view_parser = subparsers.add_parser("view", help="View simulation results")
    view_parser.add_argument(
        "--file",
        type=str,
        help="Path to the simulation results file to view",
    )
    view_parser.add_argument(
        "--only-show-failed",
        action="store_true",
        help="Only show failed tasks.",
    )
    view_parser.add_argument(
        "--only-show-all-failed",
        action="store_true",
        help="Only show tasks that failed in all trials.",
    )
    view_parser.set_defaults(func=lambda args: run_view_simulations(args))

    # Domain command
    domain_parser = subparsers.add_parser("domain", help="Show domain documentation")
    domain_parser.add_argument(
        "domain",
        type=str,
        help="Name of the domain to show documentation for (e.g., 'ota', 'delivery', 'instore')",
    )

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


def run_view_simulations(args):
    from vita.scripts.view_simulations import main as view_main

    view_main(
        sim_file=args.file,
        only_show_failed=args.only_show_failed,
        only_show_all_failed=args.only_show_all_failed,
    )

if __name__ == "__main__":
    main()
