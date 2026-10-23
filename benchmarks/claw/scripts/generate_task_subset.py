#!/usr/bin/env python3
"""Generate the frozen "standard" task subset (50% per split, stratified).

Mirrors the DeepPlanning task_subsets discipline:

  * ONE-TIME, FROZEN.  The output files under task_subsets/<name>/ ARE the
    source of truth and are committed to git.  Never re-sample a published
    subset — to change the selection, start a NEW subset name.  This script
    refuses to overwrite existing files unless --force is passed.

  * CROSS-VERSION-STABLE sampling.  We seed a single random.Random(SEED)
    (an int seed — the only primitive CPython guarantees stable across
    versions) and consume .random() as a sort key over a DETERMINISTICALLY
    sorted pool.  Regeneration on any Python 3.x yields identical output.

  * FAIL-LOUD, AUDITABLE.  Every selected task id is written verbatim, one
    per line, with header comments recording the seed and the per-difficulty
    allocation.  Reading back ignores blank lines and '#' comments.

Sampling policy for "standard":
  * general    : 161 -> 81   (stratified by `difficulty`)
  * multimodal : 101 -> 51   (stratified by `difficulty`)
  * multi_turn :  38 -> 38   (full — too small to sample, kept entire)

Stratified allocation uses the largest-remainder method so the per-split
totals land EXACTLY on 81 / 51 while preserving the difficulty distribution
as closely as integer rounding allows.  A stratum can round to zero (e.g.
multimodal has a single `expert` task); this is logged, never silent.

Usage:
    python scripts/generate_task_subset.py            # dry-run: print, refuse overwrite
    python scripts/generate_task_subset.py --write     # write frozen files (first time)
    python scripts/generate_task_subset.py --write --force   # explicit re-freeze
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Frozen parameters — DO NOT change once the subset is published.
# ---------------------------------------------------------------------------
SEED = 20260824
SUBSET_NAME = "standard"

REPO = Path(__file__).resolve().parent.parent
TASKS_DIR = REPO / "tasks"
OUT_DIR = REPO / "task_subsets" / SUBSET_NAME

# split -> target count (None = keep the whole split, no sampling)
SPLIT_TARGETS = {
    "general": 81,
    "multimodal": 51,
    "multi_turn": None,  # 38/38, full
}

_PREFIX_TO_SPLIT = {"T": "general", "M": "multimodal", "C": "multi_turn"}


def split_of(task_id: str) -> str:
    """Map a task id to its split via the T/M/C prefix."""
    pfx = task_id[:1]
    if pfx not in _PREFIX_TO_SPLIT:
        raise ValueError(f"task id {task_id!r} has no recognised split prefix (T/M/C)")
    return _PREFIX_TO_SPLIT[pfx]


def _sort_key(task_id: str) -> tuple:
    """Deterministic numeric-then-name ordering, e.g. T001.. before T010.."""
    pfx = task_id[:1]
    num = ""
    for ch in task_id[1:]:
        if ch.isdigit():
            num += ch
        else:
            break
    return (pfx, int(num) if num else -1, task_id)


def _difficulty(task_id: str) -> str:
    raw = yaml.safe_load((TASKS_DIR / task_id / "task.yaml").read_text())
    diff = raw.get("difficulty")
    if not diff:
        raise ValueError(f"{task_id}: task.yaml missing `difficulty`")
    return str(diff)


def _allocate(counts: dict[str, int], target: int) -> dict[str, int]:
    """Largest-remainder apportionment of `target` across strata by size.

    Guarantees sum(result.values()) == target.  Ties in the fractional
    remainder are broken by stratum name for determinism.
    """
    total = sum(counts.values())
    base: dict[str, int] = {}
    remainder: dict[str, float] = {}
    for stratum, c in counts.items():
        ideal = c * target / total
        base[stratum] = int(ideal)  # floor
        remainder[stratum] = ideal - base[stratum]
    need = target - sum(base.values())
    order = sorted(counts, key=lambda s: (-remainder[s], s))
    for stratum in order[:need]:
        base[stratum] += 1
    return base


def _sample_split(task_ids: list[str], target: int, rng: random.Random) -> tuple[list[str], dict]:
    """Difficulty-stratified sample of `target` ids using a shared rng.

    Returns (selected_sorted, report) where report records per-difficulty
    (pool_size -> picked) for the header/log.
    """
    strata: dict[str, list[str]] = {}
    for tid in task_ids:
        strata.setdefault(_difficulty(tid), []).append(tid)

    counts = {s: len(v) for s, v in strata.items()}
    alloc = _allocate(counts, target)

    selected: list[str] = []
    report: dict[str, tuple[int, int]] = {}
    for stratum in sorted(strata):  # fixed order for rng determinism
        pool = sorted(strata[stratum], key=_sort_key)
        # one rng.random() per item, in the deterministically-sorted order
        decorated = sorted((rng.random(), tid) for tid in pool)
        k = alloc[stratum]
        picked = sorted((tid for _, tid in decorated[:k]), key=_sort_key)
        selected.extend(picked)
        report[stratum] = (len(pool), k)

    return sorted(selected, key=_sort_key), report


def build_subsets() -> dict[str, dict]:
    """Compute the frozen subset for every split. Deterministic.

    Returns {split: {"ids": [...], "target": int|None, "pool": int,
                     "report": {difficulty: (pool, picked)}}}.
    """
    all_ids = sorted(
        (d.name for d in TASKS_DIR.iterdir() if d.is_dir() and (d / "task.yaml").exists()),
        key=_sort_key,
    )
    by_split: dict[str, list[str]] = {"general": [], "multimodal": [], "multi_turn": []}
    for tid in all_ids:
        by_split[split_of(tid)].append(tid)

    # single rng, splits consumed in a fixed order -> reproducible
    rng = random.Random(SEED)
    out: dict[str, dict] = {}
    for split in ("general", "multimodal", "multi_turn"):
        pool = by_split[split]
        target = SPLIT_TARGETS[split]
        if target is None:
            out[split] = {"ids": sorted(pool, key=_sort_key), "target": None,
                          "pool": len(pool), "report": {}}
        else:
            ids, report = _sample_split(pool, target, rng)
            out[split] = {"ids": ids, "target": target, "pool": len(pool), "report": report}
    return out


def _render(split: str, info: dict) -> str:
    lines = [
        f"# task_subsets/{SUBSET_NAME}/{split}.txt",
        f"# FROZEN — generated by scripts/generate_task_subset.py (SEED={SEED}).",
        f"# Do not hand-edit; do not re-sample. To change selection, use a new subset name.",
    ]
    if info["target"] is None:
        lines.append(f"# split={split}  FULL  {info['pool']}/{info['pool']} (no sampling)")
    else:
        lines.append(f"# split={split}  {len(info['ids'])}/{info['pool']}  (stratified by difficulty)")
        for diff in sorted(info["report"]):
            pool, picked = info["report"][diff]
            note = "  <-- rounds to 0 (dropped)" if picked == 0 else ""
            lines.append(f"#   difficulty={diff}: {picked}/{pool}{note}")
    lines.append("")
    lines.extend(info["ids"])
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the frozen 'standard' task subset.")
    ap.add_argument("--write", action="store_true", help="Write files (default: dry-run print).")
    ap.add_argument("--force", action="store_true", help="Allow overwriting existing frozen files.")
    args = ap.parse_args(argv)

    subsets = build_subsets()

    total = sum(len(v["ids"]) for v in subsets.values())
    print(f"Subset '{SUBSET_NAME}' (SEED={SEED}) — {total} tasks total:")
    for split, info in subsets.items():
        print(_render(split, info))

    if not args.write:
        print("[dry-run] nothing written. Re-run with --write to freeze.")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for split, info in subsets.items():
        path = OUT_DIR / f"{split}.txt"
        if path.exists() and not args.force:
            print(f"[REFUSE] {path} already exists. Published subsets are frozen; "
                  f"pass --force only if you truly mean to re-freeze.", file=sys.stderr)
            return 1
        path.write_text(_render(split, info))
        print(f"[write] {path}  ({len(info['ids'])} ids)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
