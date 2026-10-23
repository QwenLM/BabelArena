from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from shoppingplanning.prepare_database import stage_database
from task_selection import (
    parse_task_selector,
    validate_case_directories,
    validate_dataset_selection,
)


ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ModelConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = (
            load_module(ROOT / "travelplanning/agent/call_llm.py", "travel_call_llm_test"),
            load_module(ROOT / "shoppingplanning/agent/call_llm.py", "shopping_call_llm_test"),
        )

    def test_explicit_config_takes_precedence_in_both_domains(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "models.json"
            expected = {"model_name": "external-model", "api_key_env": "TEST_KEY"}
            config_path.write_text(
                json.dumps({"models": {"external": expected}}), encoding="utf-8"
            )
            with mock.patch.dict(
                os.environ, {"DEEPPLANNING_MODELS_CONFIG": str(config_path)}
            ):
                for module in self.modules:
                    with self.subTest(module=module.__name__):
                        self.assertEqual(module.load_model_config("external"), expected)

    def test_bad_explicit_config_never_falls_back(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing.json"
            invalid = Path(temp_dir) / "invalid.json"
            invalid.write_text("{not-json", encoding="utf-8")
            for config_path, error in (
                (missing, FileNotFoundError),
                (invalid, ValueError),
            ):
                with mock.patch.dict(
                    os.environ, {"DEEPPLANNING_MODELS_CONFIG": str(config_path)}
                ):
                    for module in self.modules:
                        with self.subTest(module=module.__name__, path=config_path.name):
                            with self.assertRaises(error):
                                module.load_model_config("qwen-plus")

    def test_explicit_config_requires_models_object(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "models.json"
            config_path.write_text(json.dumps({"models": []}), encoding="utf-8")
            with mock.patch.dict(
                os.environ, {"DEEPPLANNING_MODELS_CONFIG": str(config_path)}
            ):
                for module in self.modules:
                    with self.subTest(module=module.__name__):
                        with self.assertRaises(ValueError):
                            module.load_model_config("anything")

    def test_unset_explicit_config_keeps_repository_fallback(self):
        expected = json.loads((ROOT / "models_config.json").read_text(encoding="utf-8"))[
            "models"
        ]["qwen-plus"]
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("DEEPPLANNING_MODELS_CONFIG", None)
            for module in self.modules:
                with self.subTest(module=module.__name__):
                    self.assertEqual(module.load_model_config("qwen-plus"), expected)


class SelectorTests(unittest.TestCase):
    def test_strict_selector_rejects_empty_duplicate_and_malformed_values(self):
        for selector in ("", "  ", "1,,7", "1,1", "../1", "-1", "1;echo bad"):
            with self.subTest(selector=selector):
                with self.assertRaises(ValueError):
                    parse_task_selector(selector)

    def test_travel_ranges_are_strict_and_preserve_request_order(self):
        self.assertEqual(
            parse_task_selector("4,1-3", allow_ranges=True), ("4", "1", "2", "3")
        )
        for selector in ("3-1", "1-3,2", "1-2-3"):
            with self.subTest(selector=selector):
                with self.assertRaises(ValueError):
                    parse_task_selector(selector, allow_ranges=True)

    def test_unknown_dataset_id_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Path(temp_dir) / "tasks.json"
            dataset.write_text(json.dumps([{"id": "1"}, {"id": "7"}]), encoding="utf-8")
            self.assertEqual(
                validate_dataset_selection(("1", "7"), dataset), ("1", "7")
            )
            with self.assertRaises(ValueError):
                validate_dataset_selection(("1", "8"), dataset)

    def test_shopping_selection_requires_every_staged_case(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database = Path(temp_dir)
            (database / "case_1").mkdir()
            self.assertEqual(validate_case_directories(("1",), database), ("1",))
            with self.assertRaises(ValueError):
                validate_case_directories(("1", "7"), database)


class DatabaseStagingTests(unittest.TestCase):
    def make_source(self, root: Path) -> Path:
        source = root / "source"
        for task_id in ("1", "2", "7"):
            case = source / f"case_{task_id}"
            case.mkdir(parents=True)
            (case / "payload.json").write_text(task_id, encoding="utf-8")
        (source / "README.txt").write_text("ignored", encoding="utf-8")
        return source

    def test_stages_only_exact_selected_cases(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = self.make_source(root)
            destination = root / "runtime/database_run"
            staged = stage_database(source, destination, ("1", "7"))
            self.assertEqual(staged, ("case_1", "case_7"))
            self.assertEqual(
                sorted(path.name for path in destination.iterdir()),
                ["case_1", "case_7"],
            )

    def test_all_cases_remains_the_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = self.make_source(root)
            staged = stage_database(source, root / "destination", None)
            self.assertEqual(staged, ("case_1", "case_2", "case_7"))

    def test_bad_selections_and_destinations_fail(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = self.make_source(root)
            for task_ids in ((), ("8",), ("1", "1"), ("../1",)):
                with self.subTest(task_ids=task_ids):
                    with self.assertRaises(ValueError):
                        stage_database(source, root / f"destination-{len(task_ids)}", task_ids)

            nonempty = root / "nonempty"
            nonempty.mkdir()
            (nonempty / "keep").write_text("owned", encoding="utf-8")
            with self.assertRaises(ValueError):
                stage_database(source, nonempty, ("1",))
            self.assertEqual((nonempty / "keep").read_text(encoding="utf-8"), "owned")

    def test_malformed_source_case_entry_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = self.make_source(root)
            (source / "case_bad").write_text("not a case directory", encoding="utf-8")
            with self.assertRaises(ValueError):
                stage_database(source, root / "destination", None)

    def test_separate_runtime_roots_do_not_interfere(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = self.make_source(root)
            first = root / "run-a/database_run"
            second = root / "run-b/database_run"
            stage_database(source, first, ("1",))
            stage_database(source, second, ("7",))
            self.assertTrue((first / "case_1").is_dir())
            self.assertFalse((first / "case_7").exists())
            self.assertTrue((second / "case_7").is_dir())
            self.assertFalse((second / "case_1").exists())


class EvaluationOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = load_module(
            ROOT / "shoppingplanning/evaluation/evaluation_pipeline.py",
            "shopping_evaluation_pipeline_test",
        )

    def test_absolute_output_is_used_exactly(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            absolute = Path(temp_dir) / "reports"
            resolved = self.pipeline.resolve_output_dir(
                Path("/source/shoppingplanning"), "database_name", str(absolute), "v3"
            )
            self.assertEqual(resolved, absolute)

    def test_relative_and_default_outputs_keep_legacy_layout(self):
        script_dir = Path("/source/shoppingplanning")
        self.assertEqual(
            self.pipeline.resolve_output_dir(script_dir, "database_name", "custom", "v3"),
            script_dir / "result_report/v3/custom",
        )
        self.assertEqual(
            self.pipeline.resolve_output_dir(script_dir, "database_name", None, "v3"),
            script_dir / "result_report/v3/database_name",
        )

    def test_statistics_accepts_deterministic_isolated_folder_names(self):
        statistics = load_module(
            ROOT / "shoppingplanning/evaluation/score_statistics.py",
            "shopping_score_statistics_test",
        )
        self.assertEqual(
            statistics.parse_folder_name("database_test-model_english_level1"),
            ("test-model", 1, "0", "english"),
        )


class ShoppingRunSelectionTests(unittest.TestCase):
    """shoppingplanning/run.py resolve_selected_task_ids — exercised in a
    subprocess because importing run.py caches its 'agent' package, which
    would collide with travelplanning's 'agent' in this process."""

    HARNESS = """
import argparse
import importlib.util
import json
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
scenario = sys.argv[2]
shopping = repo_root / "shoppingplanning"
sys.path.insert(0, str(shopping))
spec = importlib.util.spec_from_file_location("shopping_run_probe", shopping / "run.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

fixture = Path(sys.argv[3])
dataset = fixture / "tasks.json"
dataset.write_text(json.dumps([{"id": "1"}, {"id": "7"}]), encoding="utf-8")
database = fixture / "db"
for task_id in ("1", "7"):
    (database / f"case_{task_id}").mkdir(parents=True)

module.resolve_task_subset = lambda name, key: (
    None if name.lower() == "full" else ("1", "7") if key == "shopping_level1" else None
)
args = argparse.Namespace(
    rerun_ids=None, task_subset="standard", level=1,
    test_data=dataset, database_dir=database,
)
if scenario == "subset":
    pass
elif scenario == "full":
    args.task_subset = "full"
elif scenario == "precedence":
    args.rerun_ids = "7"
elif scenario == "invalid":
    module.resolve_task_subset = lambda name, key: ("9",)
elif scenario == "preflight":
    # Regression: the tokenizer preflight must bootstrap the tools dir onto
    # sys.path itself (the flat `from base_shopping_tool import ...` inside
    # the tool modules fails otherwise).
    module.run_tokenizer_preflight("english")
    print("OK:preflight")
    raise SystemExit(0)

try:
    selected, display = module.resolve_selected_task_ids(args)
except ValueError as exc:
    print(f"ERROR:{exc}")
else:
    print(f"OK:{selected}|{display}")
"""

    def run_scenario(self, scenario: str) -> str:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-c", self.HARNESS, str(ROOT), scenario, temp_dir],
                capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip().splitlines()[-1]

    def test_subset_resolves_and_validates(self):
        self.assertEqual(
            self.run_scenario("subset"),
            "OK:['1', '7']|standard (2 level-1 cases)",
        )

    def test_full_disables_selection(self):
        self.assertEqual(self.run_scenario("full"), "OK:None|full (all cases)")

    def test_rerun_ids_take_precedence(self):
        self.assertEqual(
            self.run_scenario("precedence"),
            "OK:['7']|(ignored — explicit --rerun-ids)",
        )

    def test_subset_id_outside_dataset_fails(self):
        self.assertTrue(
            self.run_scenario("invalid").startswith("ERROR:Invalid --task-subset:")
        )

    def test_tokenizer_preflight_bootstraps_tools_path(self):
        self.assertEqual(self.run_scenario("preflight"), "OK:preflight")


class ShellRunnerTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> tuple[Path, Path]:
        project = root / "project"
        shopping = project / "shoppingplanning"
        shopping.mkdir(parents=True)
        shutil.copy2(ROOT / "shoppingplanning/run.sh", shopping / "run.sh")
        shutil.copy2(
            ROOT / "shoppingplanning/prepare_database.py", shopping / "prepare_database.py"
        )
        shutil.copy2(ROOT / "task_selection.py", project / "task_selection.py")
        scripts = project / "scripts"
        scripts.mkdir()
        shutil.copy2(
            ROOT / "scripts/resolve_task_subset.py", scripts / "resolve_task_subset.py"
        )
        subset_dir = project / "task_subsets" / "standard"
        subset_dir.mkdir(parents=True)
        (subset_dir / "shopping_level1.txt").write_text("1\n", encoding="utf-8")
        for task_id in ("1", "7"):
            case = shopping / "database_level1" / f"case_{task_id}"
            case.mkdir(parents=True)
            (case / "payload.json").write_text(task_id, encoding="utf-8")

        fake_bin = root / "bin"
        fake_bin.mkdir()
        fake_python = fake_bin / "python"
        fake_python.write_text(
            """#!/bin/bash
printf '%q ' "$@" >> "$CALL_LOG"
printf '\\n' >> "$CALL_LOG"
if [ "$1" = "-c" ]; then
    echo en
    exit 0
fi
if [ "$1" = "scripts/resolve_task_subset.py" ]; then
    exec "$REAL_PYTHON" "$@"
fi
if [ "$1" = "prepare_database.py" ]; then
    exec "$REAL_PYTHON" "$@"
fi
if [ "$1" = "run.py" ]; then
    exit 0
fi
if [ "$1" = "evaluation/evaluation_pipeline.py" ]; then
    shift
    database=""
    output=""
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --database_dir) database="$2"; shift 2 ;;
            --output_dir) output="$2"; shift 2 ;;
            --case_filter) shift; while [ "$#" -gt 0 ] && [[ "$1" != --* ]]; do shift; done ;;
            *) shift ;;
        esac
    done
    if [ -z "$output" ]; then
        output="result_report/${BENCHMARK_VERSION}/$(basename "$database")"
    fi
    mkdir -p "$output"
    printf '{}' > "$output/summary_report.json"
    exit 0
fi
if [ "$1" = "evaluation/score_statistics.py" ]; then
    exit 0
fi
exit 99
""",
            encoding="utf-8",
        )
        fake_python.chmod(0o755)
        return shopping, fake_bin

    def runner_env(self, root: Path, fake_bin: Path) -> dict[str, str]:
        env = os.environ.copy()
        env.pop("BENCHMARK_TASK_SUBSET", None)
        env.pop("DEEPPLANNING_TASK_IDS", None)
        env.pop("DEEPPLANNING_RUN_DIR", None)
        env.update(
            {
                "PATH": f"{fake_bin}{os.pathsep}{env['PATH']}",
                "REAL_PYTHON": sys.executable,
                "CALL_LOG": str(root / "calls.log"),
                "PYTHONDONTWRITEBYTECODE": "1",
                "BENCHMARK_MODEL": "test-model",
                "BENCHMARK_LANGUAGE": "english",
                "BENCHMARK_LEVELS": "1",
                "BENCHMARK_WORKERS": "1",
                "BENCHMARK_VERSION": "smoke",
            }
        )
        return env

    def test_external_selected_run_only_mutates_runtime_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shopping, fake_bin = self.make_fixture(root)
            runtime = root / "runtime"
            before = sorted(
                path.relative_to(shopping) for path in shopping.rglob("*")
            )
            env = self.runner_env(root, fake_bin)
            env.update(
                {
                    "DEEPPLANNING_RUN_DIR": str(runtime),
                    "DEEPPLANNING_TASK_IDS": "1",
                }
            )
            subprocess.run(
                ["bash", "run.sh"], cwd=shopping, env=env, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            )
            after = sorted(path.relative_to(shopping) for path in shopping.rglob("*"))
            self.assertEqual(after, before)

            output_name = "database_test-model_english_level1"
            inferred = runtime / "database_infered" / output_name
            report = runtime / "result_report/smoke" / output_name
            self.assertEqual(
                sorted(path.name for path in inferred.iterdir()), ["case_1"]
            )
            self.assertTrue((report / "summary_report.json").is_file())

            calls = (root / "calls.log").read_text(encoding="utf-8")
            self.assertIn("--rerun-ids 1", calls)
            self.assertIn("--case_filter case_1", calls)
            self.assertIn(f"--output_dir {report}", calls)
            self.assertIn(
                f"--result_report_dir {runtime / 'result_report/smoke'}", calls
            )

    def test_unset_runtime_variables_keep_legacy_command_shape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shopping, fake_bin = self.make_fixture(root)
            env = self.runner_env(root, fake_bin)
            # 'full' is the opt-out: no selector must be injected anywhere.
            env["BENCHMARK_TASK_SUBSET"] = "full"
            subprocess.run(
                ["bash", "run.sh"], cwd=shopping, env=env, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            )
            calls = (root / "calls.log").read_text(encoding="utf-8")
            run_call = next(line for line in calls.splitlines() if line.startswith("run.py "))
            prepare_call = next(
                line for line in calls.splitlines()
                if line.startswith("prepare_database.py ")
            )
            eval_call = next(
                line for line in calls.splitlines()
                if line.startswith("evaluation/evaluation_pipeline.py ")
            )
            stats_call = next(
                line for line in calls.splitlines()
                if line.startswith("evaluation/score_statistics.py ")
            )
            self.assertNotIn("--rerun-ids", run_call)
            self.assertNotIn("--task-subset", run_call)
            self.assertNotIn("--task-ids", prepare_call)
            self.assertNotIn("--output_dir", eval_call)
            self.assertNotIn("--case_filter", eval_call)
            self.assertNotIn("--result_report_dir", stats_call)
            self.assertTrue((shopping / "database_infered").is_dir())

    def test_default_task_subset_drives_staging_inference_and_evaluation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shopping, fake_bin = self.make_fixture(root)
            runtime = root / "runtime"
            env = self.runner_env(root, fake_bin)
            env["DEEPPLANNING_RUN_DIR"] = str(runtime)
            # No DEEPPLANNING_TASK_IDS and no BENCHMARK_TASK_SUBSET: the
            # fixture's standard subset (case 1) must drive the whole run.
            subprocess.run(
                ["bash", "run.sh"], cwd=shopping, env=env, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            )
            inferred = runtime / "database_infered/database_test-model_english_level1"
            self.assertEqual(
                sorted(path.name for path in inferred.iterdir()), ["case_1"]
            )
            calls = (root / "calls.log").read_text(encoding="utf-8")
            self.assertIn("--task-ids 1", calls)
            self.assertIn("--rerun-ids 1", calls)
            self.assertIn("--task-subset full", calls)
            self.assertIn("--case_filter case_1", calls)

    def test_unknown_task_subset_fails_before_staging(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shopping, fake_bin = self.make_fixture(root)
            env = self.runner_env(root, fake_bin)
            env["BENCHMARK_TASK_SUBSET"] = "nonexistent"
            result = subprocess.run(
                ["bash", "run.sh"], cwd=shopping, env=env, check=False,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("task subset", result.stdout.lower())
            self.assertFalse((shopping / "database_infered").exists())
            calls_file = root / "calls.log"
            if calls_file.exists():
                self.assertNotIn(
                    "prepare_database.py", calls_file.read_text(encoding="utf-8")
                )


if __name__ == "__main__":
    unittest.main()
