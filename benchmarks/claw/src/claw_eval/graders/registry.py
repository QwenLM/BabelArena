"""Task ID -> Grader dynamic loading from tasks/<id>/grader.py."""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

from ..utils.language import get_runtime_language
from .base import AbstractGrader


def _candidate_grader_paths(base: Path) -> list[Path]:
    """Yield grader file paths in load priority order.

    When ``CLAW_EVAL_LANGUAGE`` is set we prefer ``grader_<suffix>.py``
    over the source ``grader.py`` so the grader's matchers / embedded
    judge prompts are in the same language as the conversation it grades.
    """
    paths: list[Path] = []
    info = get_runtime_language()
    if info is not None:
        paths.append(base.parent / f"grader_{info.suffix}.py")
    paths.append(base)
    return paths


def get_grader(
    task_id: str,
    tasks_dir: str | Path = "tasks",
    task_dir: str | Path | None = None,
) -> AbstractGrader:
    """Dynamically load and instantiate a grader from tasks/<task_id>/grader.py.

    If ``task_dir`` is given, try loading from that directory first (handles
    cases where the directory name differs from the task_id in task.yaml).
    """
    primary = Path(tasks_dir) / task_id / "grader.py"
    alt = Path(task_dir) / "grader.py" if task_dir is not None else None

    for base in [primary] + ([alt] if alt is not None else []):
        for candidate in _candidate_grader_paths(base):
            if not candidate.exists():
                continue
            try:
                result = _load_grader_from(candidate, task_id)
                if result is not None:
                    return result
            except Exception as exc:
                if candidate.name == "grader.py":
                    raise
                print(
                    f"[grader] {candidate.name} failed to load ({exc}), "
                    f"falling back to grader.py"
                )

    raise FileNotFoundError(
        f"No grader found at {primary} for task_id={task_id!r}"
    )


def _load_grader_from(path: Path, task_id: str) -> AbstractGrader | None:
    """Load and instantiate a grader from a single file, or return None."""
    module_name = f"task_grader_{task_id}_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load grader module from {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for _name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ != module.__name__:
            continue
        if issubclass(obj, AbstractGrader) and obj is not AbstractGrader:
            return obj()
    return None
