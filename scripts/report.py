#!/usr/bin/env python3
"""Collect scores from a finished `bench run` into one table.

Each benchmark keeps its own evaluator and its own headline metric. This script
does not invent a combined score -- averaging a tool-call correctness rate, an
LLM-judged pass rate and a constraint-satisfaction accuracy would produce a
number that means nothing. It reports them side by side, labelled.

    tau3          mean reward over simulations. A task scores 1.0 only if the
                  final database state matches and every required action fired.
    vitabench     mean reward, assigned by an LLM judge against per-task
                  rubrics. Comparable only across runs using the same judge.
    deepplanning  avg_acc, the mean of shopping weighted_average_case_score and
                  travel case_acc, as defined by the benchmark's own aggregator,
                  averaged over trials (each trial is scored from its own
                  directory).
    claw          avg_score, the mean composite task_score (completion, safety,
                  robustness, LLM-judged communication) from claw's own
                  batch_summary.json, with its pass^N count alongside.

Usage:  scripts/report.py --run-id 20260908_143000 [--format md|csv|json]
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Optional

REPO = Path(__file__).resolve().parent.parent
BENCHMARKS = REPO / "benchmarks"
DATA = REPO / "data"
RESULTS = REPO / "results"


def _read_json(path: Path) -> Optional[Any]:
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _reward_rows(path: Path) -> Optional[dict]:
    """tau3 and vitabench share this schema."""
    doc = _read_json(path)
    if not doc:
        return None
    sims = doc.get("simulations") or []
    rewards, unscored = [], 0
    for sim in sims:
        info = sim.get("reward_info") or {}
        if "evaluation_error" in (info.get("info") or {}):
            unscored += 1
            continue
        r = info.get("reward")
        if r is None:
            unscored += 1
        else:
            rewards.append(float(r))
    if not rewards:
        return None
    return {
        "score": statistics.mean(rewards),
        "n": len(rewards),
        "unscored": unscored,
        "trials": (doc.get("info") or {}).get("num_trials"),
    }


def _deepplanning_rows(manifest: dict, lang: str, agent: str,
                       warnings: list[str]) -> list[dict]:
    """deepplanning's rows for one language, averaged over its trials.

    Each trial ran in its own directory (TRAVEL_OUTPUT_DIR / DEEPPLANNING_RUN_DIR
    in the step's env), so read every trial from there with the benchmark's own
    loaders. Not from benchmarks/deepplanning/aggregated_results/: that holds one
    file per (model, language), which each trial -- and each later run of the
    same model -- overwrites, and its aggregator looks for shopping statistics in
    the source tree rather than in the trial directory, so under `bench` the
    shopping row came out missing or stale.
    """
    import contextlib
    import io

    sys.path.insert(0, str(BENCHMARKS / "deepplanning"))
    import aggregate_results as agg

    trials: dict[int, dict] = {}
    domains: set[str] = set()
    for step in manifest.get("steps", []):
        if step["benchmark"] == "deepplanning" and step["language"] == lang:
            env = step.get("env") or {}
            trials.setdefault(step.get("trial", 1), env)
            domains.update((env.get("DOMAINS") or "").split())

    per_unit: dict[str, list[tuple[float, int]]] = {"shopping": [], "travel": [], "(overall)": []}
    for t, env in sorted(trials.items()):
        model = env.get("BENCHMARK_MODEL", agent)
        language = env.get("DEEPPLANNING_LANGUAGE")
        quiet = io.StringIO()   # the loaders print their own warnings
        with contextlib.redirect_stdout(quiet):
            shop = trav = None
            if env.get("DEEPPLANNING_RUN_DIR"):
                shop = agg.load_shopping_statistics(Path(env["DEEPPLANNING_RUN_DIR"]),
                                                    model, language)
            if env.get("TRAVEL_OUTPUT_DIR"):
                trav = agg.load_travel_statistics(BENCHMARKS / "deepplanning" / "travelplanning",
                                                  model, env["TRAVEL_OUTPUT_DIR"], language)
        got = {}
        for unit, stats in (("shopping", shop), ("travel", trav)):
            if stats:
                total = stats["total"]
                got[unit] = (total["weighted_average_case_score"], total["total_cases"])
                per_unit[unit].append(got[unit])
            elif unit in domains:
                warnings.append(f"deepplanning/{lang}/trial{t}: no {unit} statistics found")
        if "shopping" in got and "travel" in got:
            per_unit["(overall)"].append(((got["shopping"][0] + got["travel"][0]) / 2,
                                          got["shopping"][1] + got["travel"][1]))

    metric = {"shopping": "weighted_avg_case_score", "travel": "case_acc", "(overall)": "avg_acc"}
    rows = []
    for unit, vals in per_unit.items():
        if not vals:
            continue
        found = len(vals)
        rows.append({"benchmark": "deepplanning", "language": lang, "unit": unit,
                     "metric": metric[unit], "score": statistics.mean(v for v, _ in vals),
                     "n": vals[0][1], "trials": found,
                     "note": "" if found == len(trials) else f"{found}/{len(trials)} trials scored"})
    return rows


def collect(run_id: str) -> tuple[list[dict], list[str]]:
    manifest_path = RESULTS / run_id / "manifest.json"
    manifest = _read_json(manifest_path)
    if not manifest:
        print(f"report: no manifest at {manifest_path}", file=sys.stderr)
        raise SystemExit(1)

    rows: list[dict] = []
    warnings: list[str] = []
    agent = manifest.get("agent_model", "?")
    # deepplanning emits one step per trial (and per domain under --num-tasks);
    # its rows are built once per language from all of them.
    deepplanning_done: set[str] = set()
    # claw records a run step and a regrade step per language; same output.
    claw_done: set[str] = set()

    for step in manifest.get("steps", []):
        bench, lang = step["benchmark"], step["language"]
        out = REPO / step["output"]

        if bench in ("tau3", "vitabench"):
            # output path encodes the domain; recover it for the row label
            domain = (out.parent.name if bench == "tau3"
                      else out.stem.rsplit("__", 1)[-1])
            got = _reward_rows(out)
            if got is None:
                warnings.append(f"{bench}/{lang}/{domain}: no scored simulations at {step['output']}")
                continue
            rows.append({
                "benchmark": bench, "language": lang, "unit": domain,
                "metric": "mean_reward", "score": got["score"],
                "n": got["n"], "trials": got["trials"] or "",
                "note": f"{got['unscored']} unscored" if got["unscored"] else "",
            })

        elif bench == "deepplanning":
            if lang in deepplanning_done:
                continue
            deepplanning_done.add(lang)
            rows += _deepplanning_rows(manifest, lang, agent, warnings)

        elif bench == "claw":
            if step["output"] in claw_done:
                continue
            claw_done.add(step["output"])
            # bench pins the directory with --continue; a run made without it
            # nests output one level down in <model>_<timestamp>/.
            summ = out.parent / "batch_summary.json"
            if not summ.is_file():
                cands = sorted(out.parent.glob("*/batch_summary.json"),
                               key=lambda f: f.stat().st_mtime)
                summ = cands[-1] if cands else summ
            doc = _read_json(summ)
            if not doc or not doc.get("tasks"):
                warnings.append(f"claw/{lang}: no batch_summary.json with graded tasks "
                                f"next to {step['output']}")
                continue
            n_tr = doc.get("trials_per_task")
            hat = doc.get(f"pass_hat_{n_tr}")
            note = [f"pass^{n_tr} {hat}/{doc['tasks']}" if hat is not None else "",
                    f"{doc['errored']} errored" if doc.get("errored") else ""]
            rows.append({"benchmark": bench, "language": lang, "unit": "(tasks)",
                         "metric": "avg_score", "score": doc.get("avg_score", 0.0),
                         "n": doc["tasks"], "trials": n_tr or "",
                         "note": "; ".join(x for x in note if x)})
    return rows, warnings


def as_markdown(rows: list[dict], manifest: dict) -> str:
    subset = manifest.get("subset")
    what = {"standard": "the frozen, roughly half-size release default",
            "full": "full task set"}.get(subset, "custom subset")
    out = [
        f"# Run `{manifest.get('run_id')}`",
        "",
        f"- agent model: `{manifest.get('agent_model')}`",
        f"- task subset: `{subset}`  ({what})",
        f"- trials per task: {manifest.get('num_trials')}",
        "",
        "Metrics are **not** comparable across benchmarks -- each column is that",
        "benchmark's own headline metric, computed by its own evaluator.",
        "",
        "| benchmark | language | unit | metric | score | n | note |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for r in rows:
        out.append(
            f"| {r['benchmark']} | {r['language']} | {r['unit']} | {r['metric']} "
            f"| {r['score']:.4f} | {r['n']} | {r['note']} |"
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

    rows, warnings = collect(a.run_id)
    manifest = _read_json(RESULTS / a.run_id / "manifest.json") or {}

    if a.format == "md":
        text = as_markdown(rows, manifest)
        out_path = RESULTS / a.run_id / "report.md"
        out_path.write_text(text, encoding="utf-8")
        print(text)
        print(f"written to {out_path.relative_to(REPO)}", file=sys.stderr)
    elif a.format == "csv":
        w = csv.DictWriter(sys.stdout,
                           fieldnames=["benchmark", "language", "unit", "metric",
                                       "score", "n", "trials", "note"])
        w.writeheader()
        w.writerows(rows)
    else:
        json.dump({"run": manifest, "rows": rows}, sys.stdout, ensure_ascii=False, indent=2)
        print()

    for warning in warnings:
        print(f"report: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
