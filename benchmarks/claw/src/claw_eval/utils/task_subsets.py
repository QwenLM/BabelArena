"""Resolve frozen task-subset manifests (e.g. the 50% "standard" subset).

Runtime counterpart to ``scripts/generate_task_subset.py``.  The manifests
under ``task_subsets/<name>/<split>.txt`` are the frozen source of truth; this
module only READS them and never falls back silently — an unknown subset name,
a missing split file, or an empty manifest all raise ``ValueError``.  Mirrors
the strict resolver discipline of ``utils/language.py``.

Name resolution precedence (highest first):
    1. explicit CLI value (``--task-subset``)
    2. environment ``BENCHMARK_TASK_SUBSET``
    3. default ``"standard"``

The reserved name ``"full"`` means "no subsetting — run every task"; the
resolvers return ``None`` for it so callers can skip narrowing.
"""
from __future__ import annotations

import os
from pathlib import Path

_ENV_VAR = "BENCHMARK_TASK_SUBSET"
_DEFAULT = "standard"
_RESERVED_FULL = "full"
_DIRNAME = "task_subsets"

VALID_SPLITS = ("general", "multimodal", "multi_turn")
_PREFIX_TO_SPLIT = {"T": "general", "M": "multimodal", "C": "multi_turn"}

# Search order for the task_subsets/ root: CWD first (matches how `batch`
# resolves --tasks-dir), then the installed package's repo root.
_PKG_ROOT = Path(__file__).resolve().parents[3]


def split_of(task_id: str) -> str:
    """Map a task id to its split via the T/M/C directory-name prefix."""
    pfx = task_id[:1]
    if pfx not in _PREFIX_TO_SPLIT:
        raise ValueError(f"task id {task_id!r} has no recognised split prefix (T/M/C)")
    return _PREFIX_TO_SPLIT[pfx]


def effective_task_subset_name(cli_value: str | None, default: str = _DEFAULT) -> str:
    """Resolve the active subset name from CLI > env > default.

    Empty / whitespace-only values fall through to the next source, so an
    explicit empty ``--task-subset ''`` still lands on the env or default.
    ``default`` lets callers substitute another fallback (e.g. ``"full"`` when
    the user already made an explicit ad-hoc selection via ``--filter``).
    """
    for candidate in (cli_value, os.environ.get(_ENV_VAR)):
        if candidate and candidate.strip():
            return candidate.strip()
    return default


def subsets_root(base: str | Path | None = None) -> Path:
    """Locate the ``task_subsets/`` directory."""
    if base is not None:
        return Path(base)
    cwd_candidate = Path.cwd() / _DIRNAME
    if cwd_candidate.is_dir():
        return cwd_candidate
    return _PKG_ROOT / _DIRNAME


def _available_names(root: Path) -> str:
    if not root.is_dir():
        return "(none)"
    names = sorted(p.name for p in root.iterdir() if p.is_dir())
    return ", ".join(names) if names else "(none)"


def resolve_task_subset(
    name: str,
    split: str,
    base: str | Path | None = None,
) -> set[str] | None:
    """Return the frozen task-id set for one split, or ``None`` for ``full``.

    Raises ``ValueError`` on an invalid split, unknown subset name, missing
    file, or empty manifest — never a silent fallback to the full split.
    """
    if split not in VALID_SPLITS:
        raise ValueError(f"Unknown split {split!r}. Valid: {', '.join(VALID_SPLITS)}")

    if name == _RESERVED_FULL:
        return None

    root = subsets_root(base)
    path = root / name / f"{split}.txt"
    if not path.exists():
        raise ValueError(
            f"Task subset {name!r} has no manifest for split {split!r} "
            f"(expected {path}). Available subsets: {_available_names(root)}. "
            f"Use --task-subset full to run every task."
        )

    ids = {
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if not ids:
        raise ValueError(f"Task subset manifest {path} is empty.")
    return ids


def resolve_subset_ids(
    name: str,
    base: str | Path | None = None,
) -> set[str] | None:
    """Union of allowed task ids across every split, or ``None`` for ``full``.

    Every split manifest must be present for a named subset; a partial subset
    raises via :func:`resolve_task_subset`.
    """
    if name == _RESERVED_FULL:
        return None
    allowed: set[str] = set()
    for split in VALID_SPLITS:
        allowed |= resolve_task_subset(name, split, base=base)
    return allowed
