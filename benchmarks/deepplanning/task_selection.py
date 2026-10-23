"""Strict parsing and dataset validation for DeepPlanning task selectors."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Iterable, Mapping, Optional, Sequence


_ID_RE = re.compile(r"[0-9]+")
_RANGE_RE = re.compile(r"([0-9]+)-([0-9]+)")

# --- Named task subsets (frozen case-ID lists shared by all languages) ------
#
# A task subset is a directory task_subsets/<name>/ holding one plain-text ID
# list per domain unit (one canonical decimal ID per line; blank lines and
# ``#`` comments are ignored). The same list applies to every language because
# case IDs are language-invariant in both domains. ``full`` is the reserved
# opt-out name meaning "no subsetting".
DEFAULT_TASK_SUBSET = "standard"
FULL_TASK_SUBSET = "full"
SUBSET_DOMAIN_KEYS = (
    "travel",
    "shopping_level1",
    "shopping_level2",
    "shopping_level3",
)
_SUBSET_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
# Honors DEEPPLANNING_DATA_DIR so the frozen subset lists travel with the
# rest of the benchmark data. See data_paths.py.
from data_paths import task_subsets_dir as _task_subsets_dir  # noqa: E402
_SUBSETS_DIR = _task_subsets_dir()


def effective_task_subset_name(
    cli_value: Optional[str], env: Optional[Mapping[str, str]] = None
) -> str:
    """Resolve the subset name: CLI > BENCHMARK_TASK_SUBSET > default.

    Blank values fall through to the next source so an empty environment
    variable behaves like an unset one.
    """
    source = os.environ if env is None else env
    for candidate in (cli_value, source.get("BENCHMARK_TASK_SUBSET")):
        if candidate is not None and str(candidate).strip():
            return str(candidate).strip()
    return DEFAULT_TASK_SUBSET


def resolve_task_subset(
    name: str, domain_key: str, *, subsets_dir: Optional[Path] = None
) -> Optional[tuple[str, ...]]:
    """Load the frozen ID list for a named subset, or ``None`` for ``full``.

    IDs are returned in file order as canonical decimal strings. Every failure
    (unknown name, missing per-domain file, empty/malformed/duplicate IDs) is
    a ``ValueError`` — subsets never fall back silently.
    """
    if name is None or not str(name).strip():
        raise ValueError("Task subset name must not be empty")
    name = str(name).strip()
    if domain_key not in SUBSET_DOMAIN_KEYS:
        raise ValueError(
            f"Unknown task-subset domain key {domain_key!r}; "
            f"expected one of: {', '.join(SUBSET_DOMAIN_KEYS)}"
        )
    if name.lower() == FULL_TASK_SUBSET:
        return None
    if not _SUBSET_NAME_RE.fullmatch(name):
        raise ValueError(f"Unsafe task subset name {name!r}")

    directory = Path(subsets_dir) if subsets_dir is not None else _SUBSETS_DIR
    subset_file = directory / name / f"{domain_key}.txt"
    if not subset_file.is_file():
        if directory.is_dir():
            available = sorted(
                entry.name for entry in directory.iterdir() if entry.is_dir()
            )
        else:
            available = []
        detail = (
            f"available subsets: {', '.join(available)}"
            if available
            else f"no task subsets directory at {directory}"
        )
        raise ValueError(
            f"Task subset {name!r} has no {domain_key} list at {subset_file} "
            f"({detail}; pass {FULL_TASK_SUBSET!r} to run every case)"
        )

    lines = subset_file.read_text(encoding="utf-8").splitlines()
    ids = [
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not ids:
        raise ValueError(f"Task subset file is empty: {subset_file}")
    for line in ids:
        if not _ID_RE.fullmatch(line):
            raise ValueError(
                f"Invalid task subset file {subset_file}: "
                f"malformed task ID {line!r} (one ID per line)"
            )
    try:
        return normalize_task_ids(ids)
    except ValueError as exc:
        raise ValueError(f"Invalid task subset file {subset_file}: {exc}") from exc


def parse_task_selector(selector: str, *, allow_ranges: bool = False) -> tuple[str, ...]:
    """Parse a comma-separated selector without dropping or deduplicating values.

    IDs are returned in request order using their canonical decimal spelling.
    TravelPlanning may opt into inclusive ``start-end`` ranges.
    """
    if selector is None:
        raise ValueError("Task selector must not be None")
    if not selector.strip():
        raise ValueError("Task selector must not be empty")

    selected: list[str] = []
    seen: set[str] = set()

    for raw_part in selector.split(","):
        part = raw_part.strip()
        if not part:
            raise ValueError("Task selector contains an empty ID")

        values: Iterable[int]
        range_match = _RANGE_RE.fullmatch(part) if allow_ranges else None
        if range_match:
            start, end = (int(value) for value in range_match.groups())
            if start > end:
                raise ValueError(f"Task selector range starts after it ends: {part!r}")
            values = range(start, end + 1)
        elif _ID_RE.fullmatch(part):
            values = (int(part),)
        else:
            range_hint = " or an inclusive range" if allow_ranges else ""
            raise ValueError(
                f"Malformed task ID {part!r}; expected a non-negative integer{range_hint}"
            )

        for value in values:
            task_id = str(value)
            if task_id in seen:
                raise ValueError(f"Duplicate task ID: {task_id}")
            seen.add(task_id)
            selected.append(task_id)

    if not selected:
        raise ValueError("Task selector selected no tasks")
    return tuple(selected)


def normalize_task_ids(task_ids: Sequence[object]) -> tuple[str, ...]:
    """Validate already-parsed IDs and return canonical decimal strings."""
    if not task_ids:
        raise ValueError("Task selector must not be empty")
    return parse_task_selector(",".join(str(task_id) for task_id in task_ids))


def load_dataset_ids(dataset_path: Path) -> tuple[str, ...]:
    """Load and validate the IDs from a JSON list of task objects."""
    try:
        with dataset_path.open("r", encoding="utf-8") as handle:
            dataset = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load task dataset {dataset_path}: {exc}") from exc

    if not isinstance(dataset, list):
        raise ValueError(f"Task dataset must contain a JSON list: {dataset_path}")

    ids: list[str] = []
    seen: set[str] = set()
    for index, task in enumerate(dataset):
        if not isinstance(task, dict) or "id" not in task:
            raise ValueError(f"Task dataset entry {index} has no ID: {dataset_path}")
        raw_id = str(task["id"])
        if not _ID_RE.fullmatch(raw_id):
            raise ValueError(f"Task dataset entry {index} has malformed ID {raw_id!r}")
        task_id = str(int(raw_id))
        if task_id in seen:
            raise ValueError(f"Task dataset contains duplicate ID {task_id}")
        seen.add(task_id)
        ids.append(task_id)
    return tuple(ids)


def validate_dataset_selection(
    selected_ids: tuple[str, ...], dataset_path: Path
) -> tuple[str, ...]:
    """Require every selected ID to exist in the resolved language dataset."""
    available = set(load_dataset_ids(dataset_path))
    missing = [task_id for task_id in selected_ids if task_id not in available]
    if missing:
        raise ValueError(
            f"Task IDs are unavailable in {dataset_path}: {', '.join(missing)}"
        )
    if not selected_ids:
        raise ValueError("Task selector selected no tasks")
    return selected_ids


def validate_case_directories(
    selected_ids: tuple[str, ...], database_dir: Path
) -> tuple[str, ...]:
    """Require an exact direct ``case_<id>`` directory for every selected ID."""
    missing = [
        task_id
        for task_id in selected_ids
        if not (database_dir / f"case_{task_id}").is_dir()
    ]
    if missing:
        raise ValueError(
            f"Task IDs have no staged case directory in {database_dir}: "
            f"{', '.join(missing)}"
        )
    if not selected_ids:
        raise ValueError("Task selector selected no tasks")
    return selected_ids
