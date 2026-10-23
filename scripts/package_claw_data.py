#!/usr/bin/env python3
"""Package claw's `standard` task data into release archives.

    scripts/package_claw_data.py --out /path/to/release

writes one archive per split -- claw_general.tar.gz, claw_multimodal.tar.gz,
claw_multi_turn.tar.gz -- plus claw_MANIFEST.json and claw_SHA256SUMS. Each
archive holds `claw/tasks/<task_id>/...`, so unpacking them into one directory
gives a tree `bench fetch-data --source <directory>` installs as-is.

What goes in
------------
The tasks of the `standard` subset, plus every task they depend on. Some
tasks do not stand alone: a language variant's grader inherits from its
source task's grader (`load_peer_grader("T005zh_...")`), and a few tasks read
fixtures from another task's directory (`tasks/T021zh_.../fixtures/...`).
Leave a dependency out and claw does not fail -- a missing peer grader falls
back to the task's own `grader.py`, which scores the wrong thing -- so the
closure is computed, not assumed. Dependencies ship as task directories but
are not in the `standard` lists, so they are never run.

Each archive must be self-contained: a dependency has to fall in the same
split as the task that needs it, or the script stops.

Reproducible: members are sorted, owners and mtimes fixed, and gzip writes no
timestamp, so packaging the same tree twice gives byte-identical archives.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLAW = REPO / "benchmarks" / "claw"
SPLITS = {"general": "T", "multimodal": "M", "multi_turn": "C"}
# Fixed so archives are byte-identical across runs; the date of this layout.
MTIME = "2026-10-12 00:00:00 UTC"

_PEER = re.compile(r"""load_peer_grader\(\s*['"]([A-Za-z0-9_]+)['"]""")
_FIXTURE = re.compile(r"tasks/([A-Za-z0-9_]+)/")


def read_subset(name: str) -> dict[str, list[str]]:
    out = {}
    for split in SPLITS:
        f = CLAW / "task_subsets" / name / f"{split}.txt"
        out[split] = [ln.strip() for ln in f.read_text(encoding="utf-8").splitlines()
                      if ln.strip() and not ln.lstrip().startswith("#")]
    return out


def references(task_dir: Path) -> set[str]:
    """Other tasks this task's yaml files and graders point at."""
    refs: set[str] = set()
    for f in task_dir.rglob("*"):
        if f.suffix in (".py", ".yaml", ".yml") and f.is_file():
            text = f.read_text(encoding="utf-8", errors="replace")
            refs.update(_PEER.findall(text))
            refs.update(_FIXTURE.findall(text))
    refs.discard(task_dir.name)
    return refs


def closure(roots: list[str], tasks_dir: Path) -> dict[str, set[str]]:
    """task -> the tasks it needs, over the transitive closure of `roots`."""
    needs: dict[str, set[str]] = {}
    todo = list(roots)
    while todo:
        t = todo.pop()
        if t in needs:
            continue
        if not (tasks_dir / t).is_dir():
            sys.exit(f"package: task directory missing: {t}")
        needs[t] = references(tasks_dir / t)
        todo.extend(needs[t] - needs.keys())
    return needs


def split_of(task_id: str) -> str:
    for split, prefix in SPLITS.items():
        if task_id.startswith(prefix):
            return split
    sys.exit(f"package: cannot place {task_id} in a split")


def build_archive(tasks_dir: Path, members: list[str], out: Path) -> None:
    compressor = shutil.which("pigz") or "gzip"
    tar = ["tar", "--create", "--file=-", f"--directory={tasks_dir}",
           "--sort=name", "--format=gnu", f"--mtime={MTIME}",
           "--owner=0", "--group=0", "--numeric-owner", "--mode=u+rwX,go+rX,go-w",
           "--exclude=__pycache__", "--exclude=*.pyc", "--exclude=.DS_Store",
           "--transform=s,^,claw/tasks/,", "--"] + sorted(members)
    with out.open("wb") as fh:
        p_tar = subprocess.Popen(tar, stdout=subprocess.PIPE)
        p_gz = subprocess.Popen([compressor, "-n", "-9"], stdin=p_tar.stdout, stdout=fh)
        p_tar.stdout.close()
        if p_gz.wait() or p_tar.wait():
            sys.exit(f"package: failed to build {out.name}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", required=True, type=Path, help="directory to write the archives to")
    p.add_argument("--subset", default="standard")
    p.add_argument("--tasks-dir", type=Path, default=CLAW / "tasks")
    a = p.parse_args()

    subset = read_subset(a.subset)
    standard = {t for ids in subset.values() for t in ids}
    needs = closure(sorted(standard), a.tasks_dir)
    deps = sorted(set(needs) - standard)

    # Every dependency must ship in the same archive as whatever needs it.
    for t, refs in needs.items():
        for r in refs:
            if split_of(r) != split_of(t):
                sys.exit(f"package: {t} ({split_of(t)}) needs {r} ({split_of(r)}); "
                         f"the split archives would not be self-contained")

    a.out.mkdir(parents=True, exist_ok=True)
    manifest = {"subset": a.subset, "archive_root": "claw/tasks", "archives": {}}
    sums = []
    for split in SPLITS:
        members = sorted(t for t in needs if split_of(t) == split)
        out = a.out / f"claw_{split}.tar.gz"
        print(f"building {out.name}: {len(members)} task directories ...", flush=True)
        build_archive(a.tasks_dir, members, out)
        digest = sha256(out)
        sums.append(f"{digest}  {out.name}")
        manifest["archives"][out.name] = {
            "split": split,
            "bytes": out.stat().st_size,
            "sha256": digest,
            "standard_tasks": sorted(subset[split]),
            "dependency_tasks": [t for t in deps if split_of(t) == split],
            "dependency_of": {t: sorted(r for r in needs if t in needs[r])
                              for t in deps if split_of(t) == split},
        }
        print(f"  {out.stat().st_size / 1e6:,.1f} MB  sha256 {digest[:16]}...")

    (a.out / "claw_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (a.out / "claw_SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print(f"{len(standard)} standard tasks + {len(deps)} dependencies -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
