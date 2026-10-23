from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from task_selection import (
    DEFAULT_TASK_SUBSET,
    FULL_TASK_SUBSET,
    SUBSET_DOMAIN_KEYS,
    effective_task_subset_name,
    resolve_task_subset,
)


ROOT = Path(__file__).resolve().parents[1]
STANDARD_SIZES = {
    "travel": 60,
    "shopping_level1": 25,
    "shopping_level2": 25,
    "shopping_level3": 10,
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EffectiveNameTests(unittest.TestCase):
    def test_defaults_and_precedence(self):
        self.assertEqual(DEFAULT_TASK_SUBSET, "standard")
        self.assertEqual(FULL_TASK_SUBSET, "full")
        self.assertEqual(effective_task_subset_name(None, env={}), "standard")
        self.assertEqual(
            effective_task_subset_name(None, env={"BENCHMARK_TASK_SUBSET": "full"}),
            "full",
        )
        self.assertEqual(
            effective_task_subset_name("mine", env={"BENCHMARK_TASK_SUBSET": "full"}),
            "mine",
        )

    def test_blank_values_fall_through(self):
        self.assertEqual(
            effective_task_subset_name("  ", env={"BENCHMARK_TASK_SUBSET": " "}),
            "standard",
        )


class ResolverTests(unittest.TestCase):
    def make_subsets(self, root: Path) -> Path:
        subsets = root / "task_subsets"
        mine = subsets / "mine"
        mine.mkdir(parents=True)
        (mine / "travel.txt").write_text(
            "# fixture subset\n3\n1\n\n7\n", encoding="utf-8"
        )
        (mine / "shopping_level1.txt").write_text("2\n", encoding="utf-8")
        return subsets

    def test_full_disables_subsetting_case_insensitively(self):
        for name in ("full", "FULL", "Full"):
            with self.subTest(name=name):
                self.assertIsNone(resolve_task_subset(name, "travel"))

    def test_reads_ids_in_file_order_skipping_comments_and_blanks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            subsets = self.make_subsets(Path(temp_dir))
            self.assertEqual(
                resolve_task_subset("mine", "travel", subsets_dir=subsets),
                ("3", "1", "7"),
            )
            self.assertEqual(
                resolve_task_subset("mine", "shopping_level1", subsets_dir=subsets),
                ("2",),
            )

    def test_unknown_subset_name_lists_available(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            subsets = self.make_subsets(Path(temp_dir))
            with self.assertRaises(ValueError) as ctx:
                resolve_task_subset("nope", "travel", subsets_dir=subsets)
            self.assertIn("mine", str(ctx.exception))

    def test_missing_domain_file_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            subsets = self.make_subsets(Path(temp_dir))
            with self.assertRaises(ValueError):
                resolve_task_subset("mine", "shopping_level2", subsets_dir=subsets)

    def test_unknown_domain_key_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            subsets = self.make_subsets(Path(temp_dir))
            with self.assertRaises(ValueError):
                resolve_task_subset("mine", "delivery", subsets_dir=subsets)
            # Even 'full' must not mask a typo'd domain key.
            with self.assertRaises(ValueError):
                resolve_task_subset("full", "delivery", subsets_dir=subsets)

    def test_unsafe_subset_names_fail(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            subsets = self.make_subsets(Path(temp_dir))
            for name in ("../mine", "a/b", ".hidden", ""):
                with self.subTest(name=name):
                    with self.assertRaises(ValueError):
                        resolve_task_subset(name, "travel", subsets_dir=subsets)

    def test_empty_duplicate_and_malformed_files_fail(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            subsets = Path(temp_dir) / "task_subsets"
            bad = subsets / "bad"
            bad.mkdir(parents=True)
            for content in ("", "# only a comment\n", "1\n1\n", "1\nx\n", "1,2\n"):
                (bad / "travel.txt").write_text(content, encoding="utf-8")
                with self.subTest(content=content):
                    with self.assertRaises(ValueError):
                        resolve_task_subset("bad", "travel", subsets_dir=subsets)


class ResolveCliTests(unittest.TestCase):
    SCRIPT = ROOT / "scripts/resolve_task_subset.py"

    def run_cli(self, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(self.SCRIPT), *argv],
            cwd=ROOT, capture_output=True, text=True,
        )

    def test_full_prints_nothing(self):
        result = self.run_cli("travel", "--name", "full")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "")

    def test_standard_prints_matching_csv(self):
        result = self.run_cli("travel", "--name", "standard")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            tuple(result.stdout.strip().split(",")),
            resolve_task_subset("standard", "travel"),
        )

    def test_unknown_subset_fails_with_stderr(self):
        result = self.run_cli("travel", "--name", "nope")
        self.assertEqual(result.returncode, 2)
        self.assertIn("nope", result.stderr)

    def test_unknown_domain_key_fails(self):
        result = self.run_cli("delivery", "--name", "standard")
        self.assertNotEqual(result.returncode, 0)


class FrozenStandardSubsetTests(unittest.TestCase):
    """The committed standard lists are the source of truth — gate them."""

    def dataset_ids(self, path: Path) -> set[str]:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {str(int(item["id"])) for item in data}

    def test_files_exist_with_expected_sizes(self):
        for key, size in STANDARD_SIZES.items():
            with self.subTest(domain_key=key):
                ids = resolve_task_subset("standard", key)
                self.assertEqual(len(ids), size)
                self.assertEqual(len(set(ids)), size)

    def test_travel_ids_are_valid_stratified_and_skip_id_10(self):
        dataset_path = ROOT / "travelplanning/data/travelplanning_query_en.json"
        data = json.loads(dataset_path.read_text(encoding="utf-8"))
        days_by_id = {str(int(item["id"])): item["meta_info"]["days"] for item in data}
        ids = resolve_task_subset("standard", "travel")
        self.assertTrue(set(ids) <= set(days_by_id))
        self.assertNotIn("10", ids)
        buckets = Counter(days_by_id[task_id] for task_id in ids)
        self.assertEqual(buckets, Counter({days: 10 for days in range(2, 8)}))

    def test_shopping_ids_exist_in_every_level_dataset(self):
        for level in (1, 2, 3):
            with self.subTest(level=level):
                ids = resolve_task_subset("standard", f"shopping_level{level}")
                available = self.dataset_ids(
                    ROOT / f"shoppingplanning/data/level_{level}_query_meta.json"
                )
                self.assertTrue(set(ids) <= available)

    def test_ids_are_committed_sorted_numerically(self):
        for key in STANDARD_SIZES:
            with self.subTest(domain_key=key):
                ids = resolve_task_subset("standard", key)
                self.assertEqual(list(ids), sorted(ids, key=int))

    def test_generator_reproduces_the_committed_lists(self):
        generator = load_module(
            ROOT / "scripts/generate_task_subset.py", "generate_task_subset_test"
        )
        regenerated = generator.generate_standard(ROOT)
        self.assertEqual(set(regenerated), set(STANDARD_SIZES))
        for key in STANDARD_SIZES:
            with self.subTest(domain_key=key):
                self.assertEqual(
                    list(regenerated[key]),
                    list(resolve_task_subset("standard", key)),
                )


if __name__ == "__main__":
    unittest.main()
