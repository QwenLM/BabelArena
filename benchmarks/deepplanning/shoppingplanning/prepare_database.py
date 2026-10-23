#!/usr/bin/env python3
"""Stage an exact, isolated set of ShoppingPlanning case databases."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Sequence

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from task_selection import parse_task_selector


def _source_cases(source: Path) -> dict[str, Path]:
    if not source.is_dir():
        raise ValueError(f"Source database is not a directory: {source}")

    cases: dict[str, Path] = {}
    for entry in source.iterdir():
        if not entry.name.startswith("case_"):
            continue
        suffix = entry.name.removeprefix("case_")
        if not suffix.isdigit() or str(int(suffix)) != suffix:
            raise ValueError(f"Malformed source case entry: {entry}")
        if entry.is_symlink() or not entry.is_dir():
            raise ValueError(f"Source case entry is not a regular directory: {entry}")
        cases[suffix] = entry
    return cases


def stage_database(
    source: Path,
    destination: Path,
    task_ids: Sequence[str] | None,
) -> tuple[str, ...]:
    """Copy selected direct ``case_*`` directories into an empty destination."""
    source = Path(source)
    destination = Path(destination)

    source_resolved = source.resolve()
    destination_resolved = destination.resolve(strict=False)
    if destination_resolved == source_resolved or source_resolved in destination_resolved.parents:
        raise ValueError("Destination must not be the source database or a child of it")

    if destination.exists():
        if not destination.is_dir():
            raise ValueError(f"Destination is not a directory: {destination}")
        if any(destination.iterdir()):
            raise ValueError(f"Destination must be empty: {destination}")

    source_cases = _source_cases(source)
    if task_ids is None:
        selected_ids = tuple(sorted(source_cases, key=int))
    else:
        if not task_ids:
            raise ValueError("Task selector must not be empty")
        # Reuse the strict parser so direct function callers receive the same
        # canonicalization and duplicate/unsafe-ID checks as the CLI.
        selected_ids = parse_task_selector(",".join(str(value) for value in task_ids))

    if not selected_ids:
        raise ValueError(f"No case directories found in source database: {source}")

    missing = [task_id for task_id in selected_ids if task_id not in source_cases]
    if missing:
        raise ValueError(f"Requested cases are missing from {source}: {', '.join(missing)}")

    destination_existed = destination.exists()
    destination.mkdir(parents=True, exist_ok=True)
    staged: list[str] = []
    try:
        for task_id in selected_ids:
            case_name = f"case_{task_id}"
            shutil.copytree(source_cases[task_id], destination / case_name)
            staged.append(case_name)
    except Exception:
        for task_id in selected_ids:
            shutil.rmtree(destination / f"case_{task_id}", ignore_errors=True)
        if not destination_existed:
            try:
                destination.rmdir()
            except OSError:
                pass
        raise

    if len(staged) != len(selected_ids):
        raise RuntimeError(
            f"Staged {len(staged)} cases, but {len(selected_ids)} were requested"
        )
    return tuple(staged)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument(
        "--task-ids",
        default=None,
        help="Comma-separated exact task IDs; omit to stage all cases",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    task_ids = None
    if args.task_ids is not None:
        task_ids = parse_task_selector(args.task_ids)
    for case_name in stage_database(args.source, args.destination, task_ids):
        print(case_name)


if __name__ == "__main__":
    main()
