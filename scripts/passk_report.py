#!/usr/bin/env python3
"""Unified pass^k report across every benchmark in a `bench run`.

scripts/report.py prints each benchmark's native headline metric
(mean_reward / avg_acc) side by side and deliberately refuses to combine them.
This script does the opposite: it puts all benchmarks on ONE scale -- pass^1
and pass^3 -- computed identically for every one.

pass^k needs, per (item, trial), a single binary pass. Each benchmark already
exposes its own notion of "this trial fully succeeded"; we take that native
bit (policy: prefer the benchmark's own per-item success flag; where only a
graded score exists, require full marks == 1.0), then apply the canonical
estimator from the tau-bench paper (https://arxiv.org/pdf/2406.12045):

    pass^k = mean over items of  C(success_count, k) / C(num_trials, k)

so pass^1 is the per-trial pass rate and pass^3 is "all 3 trials pass", on the
exact definition tau3 uses natively (tau2.metrics.agent_metrics.pass_hat_k).

What counts as a passing trial, per benchmark:
    tau3          reward == 1.0  -- DB state matches AND every required action
                  fired (tau2's own is_successful()).
    vitabench     reward == 1.0  -- the LLM judge's rubric reward; only a full
                  score counts, as the reward is otherwise continuous.
    deepplanning  shopping: case_score == 1.0 (every expected product + coupon
                  matched). travel: case_acc == 1.0 (all commonsense AND all
                  hard constraints pass -- the benchmark's own one-vote veto).
    claw          the per-trial `passed` flag (claw thresholds its own
                  composite task_score; we use that flag unchanged).

Only tau3 and claw are lossless here; vitabench and deepplanning-shopping carry
a continuous score that this collapses to pass/fail at 1.0, so their pass^1 is
NOT their published mean_reward / avg_acc. That is the intended trade for a
single comparable scale.

Usage:  scripts/passk_report.py --run-id 20260908_143000 [--format md|csv|json]
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any, Optional

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"

_EPS = 1e-6
_KS = (1, 3)


def _read_json(path: Path) -> Optional[Any]:
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _is_full(score: Any) -> bool:
    """A graded score counts as a pass only at full marks (1.0 +/- eps)."""
    try:
        return (1 - _EPS) <= float(score) <= (1 + _EPS)
    except (TypeError, ValueError):
        return False


def pass_hat_k(num_trials: int, success_count: int, k: int) -> float:
    """Canonical pass^k (tau-bench, arxiv 2406.12045): C(s,k)/C(n,k)."""
    if num_trials < k:
        return float("nan")
    return math.comb(success_count, k) / math.comb(num_trials, k)


def _passk_over_items(items: dict[str, list[bool]]) -> dict:
    """items: item_id -> per-trial pass bits. Returns pass^k (mean over items),
    the item count, and the modal trial count."""
    if not items:
        return {"n_items": 0, "trials": 0, **{f"pass^{k}": float("nan") for k in _KS}}
    out: dict[str, Any] = {
        "n_items": len(items),
        "trials": max(len(v) for v in items.values()),
    }
    for k in _KS:
        vals = [pass_hat_k(len(b), sum(b), k) for b in items.values() if len(b) >= k]
        out[f"pass^{k}"] = (sum(vals) / len(vals)) if vals else float("nan")
    return out


# --------------------------------------------------------------------------
# per-benchmark adapters -> {item_id: [pass_bit_per_trial, ...]}
# --------------------------------------------------------------------------

def _bits_tau_like(results_path: Path) -> dict[str, list[bool]]:
    """tau3 & vitabench share one results.json. simulations[] each carry
    task_id + reward_info.reward + termination_reason; the N trials of a task
    appear as N rows. A trial passes iff reward == 1.0; infrastructure-error
    simulations (which never ran) are excluded, matching tau2's own metric."""
    doc = _read_json(results_path)
    items: dict[str, list[bool]] = {}
    if not doc:
        return items
    for sim in doc.get("simulations") or []:
        if str(sim.get("termination_reason") or "").lower() == "infrastructure_error":
            continue
        info = sim.get("reward_info") or {}
        if "evaluation_error" in (info.get("info") or {}):
            continue
        reward = info.get("reward")
        if reward is None:
            continue
        task_id = sim.get("task_id") or (sim.get("task") or {}).get("id") or sim.get("id")
        if task_id is None:
            continue
        items.setdefault(str(task_id), []).append(_is_full(reward))
    return items


def _bits_shopping(trial_dir: Path) -> dict[str, list[bool]]:
    """One trial's shopping cases. Each level folder's summary_report.json lists
    case_results[] with a binary case_score (1.0 iff every expected product +
    coupon matched). Item id = <level>/<case_name>."""
    bits: dict[str, list[bool]] = {}
    pat = "shopping/result_report/*/database_*_level*/summary_report.json"
    for summ in sorted(trial_dir.glob(pat)):
        name = summ.parent.name
        level = "L" + name.split("_level", 1)[1].split("_", 1)[0] if "_level" in name else "L?"
        doc = _read_json(summ)
        if not doc:
            continue
        for c in doc.get("case_results") or []:
            bits[f"{level}/{c.get('case_name')}"] = [_is_full(c.get("case_score", 0.0))]
    return bits


def _bits_travel(trial_dir: Path) -> dict[str, list[bool]]:
    """One trial's travel cases. evaluation_summary.json lists results[] with
    scores.case_acc (1.0 iff all commonsense AND all hard constraints pass --
    the benchmark's one-vote veto). Invalid/failed cases score 0."""
    bits: dict[str, list[bool]] = {}
    for summ in sorted(trial_dir.glob("travel/*/evaluation/evaluation_summary.json")):
        doc = _read_json(summ)
        if not doc:
            continue
        for r in doc.get("results") or []:
            sid = str(r.get("sample_id"))
            ok = bool(r.get("success")) and _is_full((r.get("scores") or {}).get("case_acc"))
            bits[sid] = [ok]
    return bits


def _claw_results(path: Path) -> list[Path]:
    """Where a claw step's batch_results.json actually is.

    `bench` runs claw with --continue, so it is exactly the recorded path. Run
    without it, claw nests output one level down in <model>_<timestamp>/;
    accept that layout too and return every candidate, newest last, so the
    caller can warn when there is more than one."""
    if path.is_file():
        return [path]
    d = path if path.is_dir() else path.parent
    if (d / "batch_results.json").is_file():
        return [d / "batch_results.json"]
    return sorted(d.glob("*/batch_results.json"), key=lambda f: f.stat().st_mtime)


def _claw_subset_size(step: dict) -> Optional[int]:
    """How many tasks the step's --task-subset holds, or None if unknown
    ('full', or no manifest). claw leaves a task with no graded trial out of
    batch_results.json entirely, so this is what exposes a silent gap."""
    argv = step.get("argv") or []
    if "--task-subset" not in argv:
        return None
    name = argv[argv.index("--task-subset") + 1]
    root = REPO / "benchmarks" / "claw" / "task_subsets" / name
    if name == "full" or not root.is_dir():
        return None
    ids: set[str] = set()
    for f in root.glob("*.txt"):
        ids |= {ln.strip() for ln in f.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.lstrip().startswith("#")}
    return len(ids) or None


def _bits_claw(path: Path) -> dict[str, list[bool]]:
    """claw's batch_results.json is a top-level JSON array of per-task entries,
    each with task_id and a `trials` list whose entries carry a `passed` flag
    (claw thresholds its own composite task_score via is_pass)."""
    doc = _read_json(path)
    items: dict[str, list[bool]] = {}
    if not doc:
        return items
    tasks = doc if isinstance(doc, list) else (doc.get("results") or doc.get("tasks") or [])
    for t in tasks:
        tid = str(t.get("task_id") or t.get("id"))
        items[tid] = [bool(tr.get("passed")) for tr in (t.get("trials") or [])]
    return items


def _merge_trials(per_trial: list[dict[str, list[bool]]]) -> dict[str, list[bool]]:
    """Concatenate N single-trial {item: [bit]} dicts into {item: [bit1, ...]}.
    An item missing from a trial simply contributes no bit for it -- its trial
    count is then smaller and pass^3 skips it."""
    merged: dict[str, list[bool]] = {}
    for trial in per_trial:
        for item, b in trial.items():
            merged.setdefault(item, []).extend(b)
    return merged


# --------------------------------------------------------------------------
# collection
# --------------------------------------------------------------------------

def _row(bench: str, lang: str, unit: str, items: dict[str, list[bool]]) -> dict:
    return {"benchmark": bench, "language": lang, "unit": unit,
            **_passk_over_items(items)}


def collect(run_id: str) -> tuple[list[dict], list[str], dict]:
    manifest_path = RESULTS / run_id / "manifest.json"
    manifest = _read_json(manifest_path)
    if not manifest:
        print(f"passk_report: no manifest at {manifest_path}", file=sys.stderr)
        raise SystemExit(1)

    rows: list[dict] = []
    warnings: list[str] = []
    deep_dirs: dict[str, list[Path]] = {}  # lang -> deepplanning trial dirs
    # claw records two steps per language (run, then a regrade pass) that
    # share one output; count it once.
    claw_done: set[str] = set()

    for step in manifest.get("steps", []):
        bench, lang = step["benchmark"], step["language"]
        out = REPO / step["output"]

        if bench in ("tau3", "vitabench"):
            unit = (out.parent.name if bench == "tau3"
                    else out.stem.rsplit("__", 1)[-1])
            items = _bits_tau_like(out)
            if not items:
                warnings.append(f"{bench}/{lang}/{unit}: no scored simulations at {step['output']}")
                continue
            rows.append(_row(bench, lang, unit, items))

        elif bench == "deepplanning":
            deep_dirs.setdefault(lang, [])
            if out not in deep_dirs[lang]:
                deep_dirs[lang].append(out)

        elif bench == "claw":
            if step["output"] in claw_done:
                continue
            claw_done.add(step["output"])
            found = _claw_results(out)
            if len(found) > 1:
                warnings.append(f"claw/{lang}: {len(found)} batch_results.json under "
                                f"{out.parent.relative_to(REPO)}; using the newest")
            items = _bits_claw(found[-1]) if found else {}
            if not items:
                warnings.append(f"claw/{lang}: no graded tasks at {step['output']}")
                continue
            want = manifest.get("num_trials")
            short = sum(1 for b in items.values() if want and len(b) < want)
            if short:
                warnings.append(f"claw/{lang}: {short} task(s) have fewer than {want} "
                                f"graded trials -- re-run with the same --run-id to fill them")
            size = _claw_subset_size(step)
            if size and len(items) < size:
                warnings.append(f"claw/{lang}: {size - len(items)} of {size} tasks have no "
                                f"graded trial and are left out of pass^k")
            rows.append(_row(bench, lang, "(tasks)", items))

    # deepplanning: one trial per directory; merge per (language, domain).
    for lang, dirs in deep_dirs.items():
        shop = _merge_trials([_bits_shopping(d) for d in dirs])
        trav = _merge_trials([_bits_travel(d) for d in dirs])
        if not shop and not trav:
            warnings.append(f"deepplanning/{lang}: no per-case results under {len(dirs)} trial dir(s)")
        if shop:
            rows.append(_row("deepplanning", lang, "shopping", shop))
        if trav:
            rows.append(_row("deepplanning", lang, "travel", trav))
        if shop or trav:
            both = {f"shopping/{k}": v for k, v in shop.items()}
            both.update({f"travel/{k}": v for k, v in trav.items()})
            rows.append(_row("deepplanning", lang, "(overall)", both))

    return rows, warnings, manifest


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def _fmt(x: Any) -> str:
    return "--" if isinstance(x, float) and math.isnan(x) else f"{x:.4f}"


def as_markdown(rows: list[dict], manifest: dict) -> str:
    out = [
        f"# Run `{manifest.get('run_id')}` -- unified pass^k",
        "",
        f"- agent model: `{manifest.get('agent_model')}`",
        f"- task subset: `{manifest.get('subset')}`",
        f"- trials per task: {manifest.get('num_trials')}",
        "",
        "One scale for every benchmark: pass^1 is the per-trial pass rate, pass^3",
        '"all 3 trials pass", both as C(s,k)/C(n,k) averaged over items. A trial',
        "passes on the benchmark's own full-success bit (reward/score == 1.0;",
        "claw: its per-trial `passed` flag).",
        "",
        "| benchmark | language | unit | items | trials | pass^1 | pass^3 |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for r in rows:
        out.append(
            f"| {r['benchmark']} | {r['language']} | {r['unit']} "
            f"| {r['n_items']} | {r['trials']} "
            f"| {_fmt(r.get('pass^1'))} | {_fmt(r.get('pass^3'))} |"
        )
    if not rows:
        out.append("| _(no scored results yet)_ | | | | | | |")
    return "\n".join(out) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--run-id", required=True)
    p.add_argument("--format", default="md", choices=("md", "csv", "json"))
    a = p.parse_args()

    rows, warnings, manifest = collect(a.run_id)

    if a.format == "md":
        text = as_markdown(rows, manifest)
        out_path = RESULTS / a.run_id / "passk_report.md"
        out_path.write_text(text, encoding="utf-8")
        print(text)
        print(f"written to {out_path.relative_to(REPO)}", file=sys.stderr)
    elif a.format == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=["benchmark", "language", "unit",
                                                   "n_items", "trials", "pass^1", "pass^3"])
        w.writeheader()
        w.writerows(rows)
    else:
        json.dump({"run": manifest, "rows": rows}, sys.stdout, ensure_ascii=False, indent=2)
        print()

    for warning in warnings:
        print(f"passk_report: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
