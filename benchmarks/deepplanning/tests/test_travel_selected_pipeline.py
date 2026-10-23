from __future__ import annotations

import argparse
import contextlib
import importlib.util
import json
import os
import re
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
TRAVEL_DIR = ROOT / "travelplanning"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


travel_run = load_module(TRAVEL_DIR / "run.py", "travel_selected_run_test")
convert_report = sys.modules[travel_run.convert_reports.__module__]
eval_converted = sys.modules[travel_run.evaluate_plans.__module__]


class FakeConversionClient:
    def __init__(self):
        self.report_texts: list[str] = []
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(create=self._create),
        )

    def _create(self, **kwargs):
        self.report_texts.append(kwargs["messages"][1]["content"])
        message = SimpleNamespace(content='<JSON>{"plans": []}</JSON>')
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def successful_evaluation(
    plan_file: Path,
    test_samples,
    output_dir: Path,
    database_dir: Path,
    print_lock,
):
    match = re.fullmatch(r"id_([0-9]+)_converted\.json", plan_file.name)
    if match is None:
        raise AssertionError(f"Unexpected plan filename: {plan_file.name}")
    sample_id = match.group(1)
    result = {
        "success": True,
        "sample_id": sample_id,
        "scores": {
            "commonsense_weighted_score": 1.0,
            "personalized_score": 1.0,
            "composite_score": 1.0,
            "case_acc": 1.0,
        },
        "commonsense_dimension_details": {},
        "personalized_dimension_score": {"constraints": {}},
    }
    (output_dir / f"id_{sample_id}_score.json").write_text(
        json.dumps(result), encoding="utf-8"
    )
    return result


class TravelSelectedArtifactTests(unittest.TestCase):
    def make_data(self, root: Path) -> tuple[Path, Path]:
        dataset = root / "tasks.json"
        dataset.write_text(
            json.dumps(
                [
                    {"id": "0", "query": "query zero", "meta_info": {}},
                    {"id": "1", "query": "query one", "meta_info": {}},
                ]
            ),
            encoding="utf-8",
        )
        database = root / "database"
        (database / "id_0").mkdir(parents=True)
        (database / "id_1").mkdir()
        return dataset, database

    def test_conversion_uses_explicit_model_and_only_selected_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result_dir = Path(temp_dir) / "result"
            reports = result_dir / "reports"
            reports.mkdir(parents=True)
            (reports / "id_0.txt").write_text("selected report", encoding="utf-8")
            (reports / "id_1.txt").write_text("unrelated report", encoding="utf-8")
            client = FakeConversionClient()

            with (
                mock.patch.object(
                    convert_report,
                    "load_model_config",
                    return_value={"model_name": "actual-evaluator"},
                ) as load_config,
                mock.patch.object(convert_report, "create_client", return_value=client),
                mock.patch.object(convert_report, "get_format_convert_prompt", return_value="prompt"),
            ):
                result = convert_report.convert_reports(
                    result_dir,
                    language="en",
                    workers=1,
                    conversion_model="caller-evaluator",
                    selected_ids=[0],
                )

            load_config.assert_called_once_with("caller-evaluator")
            self.assertEqual(client.report_texts, ["selected report"])
            self.assertEqual(result["total"], 1)
            self.assertTrue((result_dir / "converted_plans/id_0_converted.json").is_file())
            self.assertFalse((result_dir / "converted_plans/id_1_converted.json").exists())

    def test_missing_selected_report_fails_before_client_creation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result_dir = Path(temp_dir)
            (result_dir / "reports").mkdir()
            with mock.patch.object(convert_report, "load_model_config") as load_config:
                with self.assertRaises(FileNotFoundError):
                    convert_report.convert_reports(result_dir, selected_ids=[0])
            load_config.assert_not_called()

    def test_missing_converted_output_fails_stage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result_dir = Path(temp_dir)
            reports = result_dir / "reports"
            reports.mkdir()
            (reports / "id_0.txt").write_text("report", encoding="utf-8")
            with (
                mock.patch.object(convert_report, "load_model_config", return_value={}),
                mock.patch.object(convert_report, "create_client", return_value=FakeConversionClient()),
                mock.patch.object(convert_report, "get_format_convert_prompt", return_value="prompt"),
                mock.patch.object(
                    convert_report,
                    "process_single_report",
                    return_value={"success": True, "sample_id": "0"},
                ),
            ):
                with self.assertRaises(RuntimeError):
                    convert_report.convert_reports(result_dir, selected_ids=[0])

    def test_evaluation_filters_dataset_and_unrelated_plan(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset, database = self.make_data(root)
            result_dir = root / "result"
            plans = result_dir / "converted_plans"
            plans.mkdir(parents=True)
            for task_id in ("0", "1"):
                (plans / f"id_{task_id}_converted.json").write_text("{}", encoding="utf-8")

            with mock.patch.object(
                eval_converted, "process_single_evaluation", side_effect=successful_evaluation
            ):
                result = eval_converted.evaluate_plans(
                    result_dir,
                    dataset,
                    database,
                    workers=1,
                    selected_ids=[0],
                )

            summary = json.loads(
                (result_dir / "evaluation/evaluation_summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(summary["total_test_samples"], 1)
            self.assertEqual(summary["total_evaluated"], 1)
            self.assertEqual(summary["plan_files_found"], 1)
            self.assertEqual([item["sample_id"] for item in summary["results"]], ["0"])
            self.assertEqual(result["total"], 1)
            self.assertFalse((result_dir / "evaluation/id_1_score.json").exists())

    def test_missing_selected_plan_fails_without_partial_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset, database = self.make_data(root)
            result_dir = root / "result"
            (result_dir / "converted_plans").mkdir(parents=True)
            with self.assertRaises(FileNotFoundError):
                eval_converted.evaluate_plans(
                    result_dir, dataset, database, selected_ids=[0]
                )
            self.assertFalse((result_dir / "evaluation/evaluation_summary.json").exists())

    def test_legacy_evaluation_still_scores_complete_dataset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dataset, database = self.make_data(root)
            result_dir = root / "result"
            plans = result_dir / "converted_plans"
            plans.mkdir(parents=True)
            for task_id in ("0", "1"):
                (plans / f"id_{task_id}_converted.json").write_text("{}", encoding="utf-8")
            with mock.patch.object(
                eval_converted, "process_single_evaluation", side_effect=successful_evaluation
            ):
                result = eval_converted.evaluate_plans(
                    result_dir, dataset, database, workers=2
                )
            self.assertEqual(result["total"], 2)
            self.assertEqual(result["total_evaluated"], 2)


class TravelIntegratedSelectedPipelineTests(unittest.TestCase):
    def make_fixture(
        self,
        root: Path,
        selector: str | None = "0",
        task_subset: str | None = None,
    ):
        root.mkdir(parents=True, exist_ok=True)
        dataset = root / "tasks.json"
        dataset.write_text(
            json.dumps(
                [
                    {"id": "0", "query": "zero", "meta_info": {}},
                    {"id": "1", "query": "one", "meta_info": {}},
                ]
            ),
            encoding="utf-8",
        )
        database = root / "database"
        (database / "id_0").mkdir(parents=True)
        (database / "id_1").mkdir()
        tool_schema = root / "tools.json"
        tool_schema.write_text("[]", encoding="utf-8")
        output_root = root / "output"
        args = argparse.Namespace(
            model="caller-agent",
            conversion_model="caller-evaluator",
            language="english",
            workers=1,
            max_llm_calls=2,
            output_dir=str(output_root),
            _user_output_dir=str(output_root),
            save_intermediate=False,
            start_from="inference",
            rerun_ids=selector,
            task_subset=task_subset,
            verbose=False,
            debug=False,
        )

        def setup_paths(pipeline_args):
            pipeline_args.test_data = dataset
            pipeline_args.database_dir = database
            pipeline_args.tool_schema_path = tool_schema
            pipeline_args.output_dir = output_root / f"{pipeline_args.model}_{pipeline_args.language}"
            for name in ("trajectories", "reports", "converted_plans", "evaluation"):
                (pipeline_args.output_dir / name).mkdir(parents=True, exist_ok=True)
            return pipeline_args

        args._test_setup_paths = setup_paths
        return args, setup_paths

    def test_selected_task_remains_selected_through_all_stages(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args, setup_paths = self.make_fixture(root)
            events: list[str] = []
            client = FakeConversionClient()

            def preflight(model_name):
                events.append(f"preflight:{model_name}")
                return {"model_name": model_name}

            def inference(**kwargs):
                events.append("inference")
                self.assertEqual(kwargs["rerun_ids"], [0])
                output_dir = kwargs["output_dir"]
                (output_dir / "reports/id_0.txt").write_text("report zero", encoding="utf-8")
                (output_dir / "trajectories/id_0.json").write_text("{}", encoding="utf-8")
                return {"total": 1, "success": 1, "failed": 0, "results": [{"id": "0"}]}

            with (
                mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths),
                mock.patch.object(travel_run, "load_model_config", side_effect=preflight),
                mock.patch.object(travel_run, "run_agent_inference", side_effect=inference),
                mock.patch.object(
                    convert_report,
                    "load_model_config",
                    return_value={"model_name": "actual-evaluator"},
                ),
                mock.patch.object(convert_report, "create_client", return_value=client),
                mock.patch.object(convert_report, "get_format_convert_prompt", return_value="prompt"),
                mock.patch.object(
                    eval_converted,
                    "process_single_evaluation",
                    side_effect=successful_evaluation,
                ),
            ):
                success, inference_result, conversion_result, evaluation_result = (
                    travel_run.run_single_language(args, "en")
                )

            self.assertTrue(success)
            self.assertEqual(
                events[:3],
                ["preflight:caller-agent", "preflight:caller-evaluator", "inference"],
            )
            self.assertEqual(inference_result["total"], 1)
            self.assertEqual(conversion_result["total"], 1)
            self.assertEqual(evaluation_result["total"], 1)
            output_dir = root / "output/caller-agent_en"
            summary = json.loads(
                (output_dir / "evaluation/evaluation_summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(summary["total_test_samples"], 1)
            self.assertEqual(summary["total_evaluated"], 1)
            self.assertEqual(summary["plan_files_found"], 1)
            self.assertEqual([item["sample_id"] for item in summary["results"]], ["0"])
            self.assertTrue((output_dir / "reports/id_0.txt").is_file())
            self.assertTrue((output_dir / "converted_plans/id_0_converted.json").is_file())
            self.assertTrue((output_dir / "trajectories/id_0.json").is_file())
            self.assertFalse(any(output_dir.rglob("id_1*")))

    def test_unavailable_id_fails_before_model_preflight_or_inference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            args, setup_paths = self.make_fixture(Path(temp_dir), selector="9")
            with (
                mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths),
                mock.patch.object(travel_run, "load_model_config") as load_config,
                mock.patch.object(travel_run, "run_agent_inference") as inference,
            ):
                success, *_ = travel_run.run_single_language(args, "en")
            self.assertFalse(success)
            load_config.assert_not_called()
            inference.assert_not_called()

    def test_missing_conversion_config_fails_before_inference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            args, setup_paths = self.make_fixture(Path(temp_dir))

            def preflight(model_name):
                if model_name == "caller-evaluator":
                    raise ValueError("missing evaluator")
                return {}

            with (
                mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths),
                mock.patch.object(travel_run, "load_model_config", side_effect=preflight),
                mock.patch.object(travel_run, "run_agent_inference") as inference,
            ):
                success, *_ = travel_run.run_single_language(args, "en")
            self.assertFalse(success)
            inference.assert_not_called()

    def test_missing_report_after_inference_fails_pipeline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            args, setup_paths = self.make_fixture(Path(temp_dir))

            def inference_without_report(**kwargs):
                return {"total": 1, "success": 1, "failed": 0, "results": [{"id": "0"}]}

            with (
                mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths),
                mock.patch.object(travel_run, "load_model_config", return_value={}),
                mock.patch.object(
                    travel_run,
                    "run_agent_inference",
                    side_effect=inference_without_report,
                ),
                mock.patch.object(convert_report, "load_model_config") as conversion_load,
                mock.patch.object(travel_run, "evaluate_plans") as evaluation,
            ):
                success, *_ = travel_run.run_single_language(args, "en")

            self.assertFalse(success)
            conversion_load.assert_not_called()
            evaluation.assert_not_called()

    def test_two_selected_runs_do_not_share_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)

            def run_one(task_id: int):
                root = base / f"run-{task_id}"
                args, _ = self.make_fixture(root, selector=str(task_id))
                success, *_ = travel_run.run_single_language(args, "en")
                self.assertTrue(success)
                return root / "output/caller-agent_en"

            def setup_paths(pipeline_args):
                return pipeline_args._test_setup_paths(pipeline_args)

            def inference(**kwargs):
                task_id = kwargs["rerun_ids"][0]
                output_dir = kwargs["output_dir"]
                (output_dir / f"reports/id_{task_id}.txt").write_text(
                    f"report {task_id}", encoding="utf-8"
                )
                (output_dir / f"trajectories/id_{task_id}.json").write_text(
                    "{}", encoding="utf-8"
                )
                return {"total": 1, "success": 1, "failed": 0, "results": [{"id": task_id}]}

            with (
                mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths),
                mock.patch.object(travel_run, "load_model_config", return_value={}),
                mock.patch.object(travel_run, "run_agent_inference", side_effect=inference),
                mock.patch.object(convert_report, "load_model_config", return_value={}),
                mock.patch.object(
                    convert_report, "create_client", side_effect=lambda *args: FakeConversionClient()
                ),
                mock.patch.object(convert_report, "get_format_convert_prompt", return_value="prompt"),
                mock.patch.object(
                    eval_converted,
                    "process_single_evaluation",
                    side_effect=successful_evaluation,
                ),
                ThreadPoolExecutor(max_workers=2) as executor,
            ):
                first, second = list(executor.map(run_one, (0, 1)))

            self.assertTrue((first / "converted_plans/id_0_converted.json").is_file())
            self.assertFalse((first / "converted_plans/id_1_converted.json").exists())
            self.assertTrue((second / "converted_plans/id_1_converted.json").is_file())
            self.assertFalse((second / "converted_plans/id_0_converted.json").exists())


class TravelTaskSubsetPipelineTests(unittest.TestCase):
    """--task-subset wiring: default narrows every stage, 'full' opts out,
    --rerun-ids keeps absolute precedence."""

    def make_fixture(self, root: Path, **kwargs):
        return TravelIntegratedSelectedPipelineTests.make_fixture(self, root, **kwargs)

    def conversion_mocks(self, client):
        return (
            mock.patch.object(
                convert_report, "load_model_config", return_value={"model_name": "m"}
            ),
            mock.patch.object(convert_report, "create_client", return_value=client),
            mock.patch.object(
                convert_report, "get_format_convert_prompt", return_value="prompt"
            ),
            mock.patch.object(
                eval_converted,
                "process_single_evaluation",
                side_effect=successful_evaluation,
            ),
        )

    def test_default_subset_narrows_all_stages(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args, setup_paths = self.make_fixture(
                root, selector=None, task_subset="standard"
            )
            client = FakeConversionClient()

            def inference(**kwargs):
                self.assertEqual(kwargs["rerun_ids"], [0])
                output_dir = kwargs["output_dir"]
                (output_dir / "reports/id_0.txt").write_text("zero", encoding="utf-8")
                return {"total": 1, "success": 1, "failed": 0, "results": [{"id": "0"}]}

            with contextlib.ExitStack() as stack:
                stack.enter_context(
                    mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths)
                )
                resolver = stack.enter_context(
                    mock.patch.object(travel_run, "resolve_task_subset", return_value=("0",))
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "load_model_config", return_value={})
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "run_agent_inference", side_effect=inference)
                )
                for manager in self.conversion_mocks(client):
                    stack.enter_context(manager)
                success, inference_result, conversion_result, evaluation_result = (
                    travel_run.run_single_language(args, "en")
                )

            self.assertTrue(success)
            resolver.assert_called_once_with("standard", "travel")
            self.assertEqual(inference_result["total"], 1)
            self.assertEqual(conversion_result["total"], 1)
            self.assertEqual(evaluation_result["total"], 1)
            output_dir = root / "output/caller-agent_en"
            summary = json.loads(
                (output_dir / "evaluation/evaluation_summary.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(summary["total_test_samples"], 1)
            self.assertEqual(
                [item["sample_id"] for item in summary["results"]], ["0"]
            )
            self.assertFalse(any(output_dir.rglob("id_1*")))

    def test_full_subset_runs_complete_dataset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args, setup_paths = self.make_fixture(
                root, selector=None, task_subset="full"
            )
            client = FakeConversionClient()

            def inference(**kwargs):
                self.assertEqual(kwargs["rerun_ids"], [0, 1])
                output_dir = kwargs["output_dir"]
                for task_id in ("0", "1"):
                    (output_dir / f"reports/id_{task_id}.txt").write_text(
                        task_id, encoding="utf-8"
                    )
                return {"total": 2, "success": 2, "failed": 0, "results": []}

            with contextlib.ExitStack() as stack:
                stack.enter_context(
                    mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths)
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "load_model_config", return_value={})
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "run_agent_inference", side_effect=inference)
                )
                for manager in self.conversion_mocks(client):
                    stack.enter_context(manager)
                success, _, conversion_result, evaluation_result = (
                    travel_run.run_single_language(args, "en")
                )

            self.assertTrue(success)
            self.assertEqual(conversion_result["total"], 2)
            self.assertEqual(evaluation_result["total"], 2)
            summary = json.loads(
                (
                    root / "output/caller-agent_en/evaluation/evaluation_summary.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(summary["total_test_samples"], 2)

    def test_rerun_ids_take_precedence_over_subset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args, setup_paths = self.make_fixture(
                root, selector="1", task_subset="standard"
            )
            client = FakeConversionClient()

            def inference(**kwargs):
                self.assertEqual(kwargs["rerun_ids"], [1])
                output_dir = kwargs["output_dir"]
                (output_dir / "reports/id_1.txt").write_text("one", encoding="utf-8")
                return {"total": 1, "success": 1, "failed": 0, "results": []}

            with contextlib.ExitStack() as stack:
                stack.enter_context(
                    mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths)
                )
                resolver = stack.enter_context(
                    mock.patch.object(travel_run, "resolve_task_subset")
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "load_model_config", return_value={})
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "run_agent_inference", side_effect=inference)
                )
                for manager in self.conversion_mocks(client):
                    stack.enter_context(manager)
                success, *_ = travel_run.run_single_language(args, "en")

            self.assertTrue(success)
            resolver.assert_not_called()
            summary = json.loads(
                (
                    root / "output/caller-agent_en/evaluation/evaluation_summary.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(
                [item["sample_id"] for item in summary["results"]], ["1"]
            )

    def test_subset_missing_report_scores_zero_instead_of_aborting(self):
        """Subset runs keep the full-run protocol: a case whose inference
        produced no report (no <plan> tag, 429 storm) stays in the denominator
        and scores 0 — it must not abort the language run the way the strict
        --rerun-ids contract does."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args, setup_paths = self.make_fixture(
                root, selector=None, task_subset="standard"
            )
            client = FakeConversionClient()

            def inference(**kwargs):
                self.assertEqual(kwargs["rerun_ids"], [0, 1])
                output_dir = kwargs["output_dir"]
                # Case 1 produces no report; the agent still counts it.
                (output_dir / "reports/id_0.txt").write_text("zero", encoding="utf-8")
                return {"total": 2, "success": 1, "failed": 1, "results": []}

            with contextlib.ExitStack() as stack:
                stack.enter_context(
                    mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths)
                )
                stack.enter_context(
                    mock.patch.object(
                        travel_run, "resolve_task_subset", return_value=("0", "1")
                    )
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "load_model_config", return_value={})
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "run_agent_inference", side_effect=inference)
                )
                for manager in self.conversion_mocks(client):
                    stack.enter_context(manager)
                success, _, conversion_result, evaluation_result = (
                    travel_run.run_single_language(args, "en")
                )

            self.assertTrue(success)
            self.assertEqual(conversion_result["total"], 1)
            summary = json.loads(
                (
                    root / "output/caller-agent_en/evaluation/evaluation_summary.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(summary["total_test_samples"], 2)
            self.assertEqual(
                [item["sample_id"] for item in summary["results"]], ["0"]
            )

    def test_default_name_resolution_reaches_standard(self):
        """With no --task-subset and no env override, the resolver must be
        asked for 'standard' — the v8 default."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args, setup_paths = self.make_fixture(
                Path(temp_dir), selector=None, task_subset=None
            )
            environment = {
                key: value
                for key, value in os.environ.items()
                if key != "BENCHMARK_TASK_SUBSET"
            }
            with (
                mock.patch.dict(os.environ, environment, clear=True),
                mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths),
                mock.patch.object(
                    travel_run,
                    "resolve_task_subset",
                    side_effect=ValueError("stop here"),
                ) as resolver,
                mock.patch.object(travel_run, "load_model_config") as load_config,
            ):
                success, *_ = travel_run.run_single_language(args, "en")
            self.assertFalse(success)
            resolver.assert_called_once_with("standard", "travel")
            load_config.assert_not_called()

    def test_subset_with_all_reports_missing_still_writes_zero_summary(self):
        """Even if every selected case failed inference (no reports at all),
        a subset run must complete and write a summary whose denominator is
        the subset size with all-zero metrics."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args, setup_paths = self.make_fixture(
                root, selector=None, task_subset="standard"
            )
            client = FakeConversionClient()

            def inference(**kwargs):
                self.assertEqual(kwargs["rerun_ids"], [0, 1])
                return {"total": 2, "success": 0, "failed": 2, "results": []}

            with contextlib.ExitStack() as stack:
                stack.enter_context(
                    mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths)
                )
                stack.enter_context(
                    mock.patch.object(
                        travel_run, "resolve_task_subset", return_value=("0", "1")
                    )
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "load_model_config", return_value={})
                )
                stack.enter_context(
                    mock.patch.object(travel_run, "run_agent_inference", side_effect=inference)
                )
                for manager in self.conversion_mocks(client):
                    stack.enter_context(manager)
                success, *_ = travel_run.run_single_language(args, "en")

            self.assertTrue(success)
            summary = json.loads(
                (
                    root / "output/caller-agent_en/evaluation/evaluation_summary.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(summary["total_test_samples"], 2)
            self.assertEqual(summary["results"], [])
            self.assertEqual(summary["metrics"]["case_acc"], 0.0)

    def test_invalid_subset_fails_before_model_preflight(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            args, setup_paths = self.make_fixture(
                Path(temp_dir), selector=None, task_subset="standard"
            )
            with (
                mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths),
                mock.patch.object(
                    travel_run,
                    "resolve_task_subset",
                    side_effect=ValueError("no such subset"),
                ),
                mock.patch.object(travel_run, "load_model_config") as load_config,
                mock.patch.object(travel_run, "run_agent_inference") as inference,
            ):
                success, *_ = travel_run.run_single_language(args, "en")
            self.assertFalse(success)
            load_config.assert_not_called()
            inference.assert_not_called()

    def test_subset_id_outside_dataset_fails_before_model_preflight(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            args, setup_paths = self.make_fixture(
                Path(temp_dir), selector=None, task_subset="standard"
            )
            with (
                mock.patch.object(travel_run, "setup_paths", side_effect=setup_paths),
                mock.patch.object(
                    travel_run, "resolve_task_subset", return_value=("9",)
                ),
                mock.patch.object(travel_run, "load_model_config") as load_config,
                mock.patch.object(travel_run, "run_agent_inference") as inference,
            ):
                success, *_ = travel_run.run_single_language(args, "en")
            self.assertFalse(success)
            load_config.assert_not_called()
            inference.assert_not_called()


if __name__ == "__main__":
    unittest.main()
