#!/usr/bin/env python3
"""Judge whether an agent actually answered in the language it was asked in.

A multilingual agent benchmark measures two different things at once. Task
reward says whether the agent did the right thing; it says nothing about the
language it did it in. A model that reasons correctly but replies in English
when the user wrote Thai scores full reward and is still useless to that user.
This script measures the second thing separately.

Method
------
For each task, the assistant's own turns are concatenated (user turns, tool
calls and tool results are excluded -- only what the agent said) and handed to
an LLM judge together with the language the run was supposed to be in. The
judge returns a verdict per task; the per-language number is the share of tasks
judged consistent.

claw adds the markdown deliverables the agent wrote with its Write tool, judged
as the agent's own prose, and only graded traces count; its prompt and target
language names are the ones its published numbers were judged with
(PROMPT_CLAW, CLAW_LANG_NAMES). deepplanning is read from each trial's own
directories, as `bench` lays them out.

Why per task rather than one blob per language
---------------------------------------------
Concatenating every assistant turn of a language into a single prompt does not
fit: one vitabench language is ~5.5M characters (~1.4M tokens). Judging per
task keeps every prompt small, makes the result an average over independent
judgements instead of one fragile call, and tells you *which* tasks drifted.
`--granularity language` still offers the single-blob behaviour, truncated to
`--max-chars`, for when a quick one-shot read is all you want.

What counts as a violation
--------------------------
These benchmarks deliberately keep some strings in their original form: entity
IDs, tool and argument names, flight and train numbers, prices, dates, and (in
several domains) brand and product proper nouns. The evaluator anchors on them,
so an agent that echoes them verbatim is behaving correctly. The judge is
instructed to ignore them and to flag only prose the agent composed itself --
sentences, explanations, questions -- that is not in the target language.

Usage
-----
    scripts/lang_consistency.py --run-id 20260908_143000
    scripts/lang_consistency.py --run-id <id> --granularity language
    scripts/lang_consistency.py --path data/tau3/simulations/<...>/results.json \\
                                --language japanese --benchmark tau3
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

REPO = Path(__file__).resolve().parent.parent
BENCHMARKS = REPO / "benchmarks"
DATA = REPO / "data"
RESULTS = REPO / "results"
CONFIGS = REPO / "configs"

DEFAULT_MAX_CHARS = 60_000        # per judge prompt
DEFAULT_CONCURRENCY = 8


# --------------------------------------------------------------------------
# extracting what the agent said
# --------------------------------------------------------------------------

@dataclass
class TaskText:
    """Everything one agent said during one task."""
    benchmark: str
    language: str
    unit: str            # domain / level
    task_id: str
    text: str
    target: str = ""     # language as named to the judge; defaults to `language`

    @property
    def key(self) -> str:
        return f"{self.benchmark}/{self.language}/{self.unit}/{self.task_id}"


def _assistant_text(messages: Iterable[dict]) -> str:
    """Join the assistant's own words, dropping tool traffic and empty turns.

    Turns that carry only tool_calls have empty content; they say nothing about
    language and would dilute the sample, so they are skipped.
    """
    out = []
    for m in messages or []:
        if (m or {}).get("role") != "assistant":
            continue
        content = m.get("content")
        if isinstance(content, list):        # some providers chunk content
            content = "".join(
                part.get("text", "") for part in content if isinstance(part, dict)
            )
        if content and str(content).strip():
            out.append(str(content).strip())
    return "\n\n".join(out)


def _read_json(path: Path) -> Optional[Any]:
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def extract_simulation_file(path: Path, benchmark: str, language: str,
                            unit: str) -> list[TaskText]:
    """tau3 and vitabench share this schema: {"simulations": [{messages: []}]}.

    One judgement per *simulation*, not per task. With --num-trials > 1 the same
    task appears several times; each run is an independent sample of how the
    agent behaves, and merging them would both quadruple the prompt (past the
    truncation limit on vitabench) and throw away statistical power.
    """
    doc = _read_json(path)
    if not doc:
        return []
    out: list[TaskText] = []
    seen: dict[str, int] = defaultdict(int)
    for sim in doc.get("simulations") or []:
        text = _assistant_text(sim.get("messages"))
        if not text:
            continue
        tid = str(sim.get("task_id", sim.get("id", "?")))
        trial = sim.get("trial")
        if trial is None:
            seen[tid] += 1
            trial = seen[tid]
        out.append(TaskText(benchmark, language, unit, f"{tid}#{trial}", text))
    return out


def extract_deepplanning_travel(traj_dir: Path, language: str) -> list[TaskText]:
    """travelplanning/results/**/trajectories/id_<n>.json -> {"messages": [...]}."""
    out = []
    for f in sorted(traj_dir.glob("id_*.json")):
        doc = _read_json(f)
        if not doc:
            continue
        text = _assistant_text(doc.get("messages"))
        if text:
            out.append(TaskText("deepplanning", language, "travel", f.stem, text))
    return out


def extract_deepplanning_shopping(infer_dir: Path, language: str,
                                  level: str) -> list[TaskText]:
    """shoppingplanning/database_infered/<run>/case_<n>/messages.json.

    The payload is {"step", "description", "messages"} rather than a bare list.
    """
    out = []
    for f in sorted(infer_dir.glob("case_*/messages.json")):
        doc = _read_json(f)
        if not doc:
            continue
        text = _assistant_text(doc.get("messages") if isinstance(doc, dict) else doc)
        if text:
            out.append(TaskText("deepplanning", language, f"shopping_{level}",
                                f.parent.name, text))
    return out


# claw judges with its target language spelled out, as the published claw
# numbers were produced.
CLAW_LANG_NAMES = {
    "ar": "Arabic", "be": "Belarusian", "en": "English", "es": "Spanish",
    "fr": "French", "he": "Hebrew", "hi": "Hindi", "id": "Indonesian",
    "ja": "Japanese", "kk": "Kazakh", "km": "Khmer", "ko": "Korean",
    "lo": "Lao", "ms": "Malay", "my": "Burmese", "pa": "Punjabi",
    "ru": "Russian", "ta": "Tamil", "te": "Telugu", "th": "Thai",
    "tr": "Turkish", "vi": "Vietnamese", "zh": "Chinese",
}
CLAW_SPLITS = {"T": "general", "M": "multimodal", "C": "multi_turn"}
CLAW_DELIVERABLE_CHARS = 40_000   # per deliverable file


def extract_claw_trace(path: Path) -> Optional[tuple[str, str]]:
    """One claw trace (.jsonl) -> (task_id, sample), or None if it is ungraded
    or the agent wrote no prose.

    The sample is the assistant's own prose -- the text blocks of its messages;
    reasoning lives in a separate field and is never read -- followed by every
    markdown deliverable it wrote with the Write tool, which is judged as the
    agent's prose too. A trace with no grading_result is a run that was
    retried; its graded sibling is the trial that counts.
    """
    prose: list[str] = []
    deliverables: list[tuple[str, str]] = []
    task_id, graded = None, False
    try:
        fh = path.open(encoding="utf-8", errors="replace")
    except OSError:
        return None
    with fh:
        for line in fh:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            kind = ev.get("type")
            if kind in ("trace_start", "grading_result"):
                task_id = task_id or ev.get("task_id")
                graded = graded or kind == "grading_result"
            elif kind == "message":
                msg = ev.get("message") or {}
                if msg.get("role") != "assistant":
                    continue
                for block in msg.get("content") or []:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = (block.get("text") or "").strip()
                        if text:
                            prose.append(text)
            elif kind == "tool_dispatch" and ev.get("tool_name") == "Write":
                body = ev.get("request_body") or {}
                file_path = str(body.get("file_path") or "")
                content = (body.get("content") or "").strip()
                if file_path.endswith(".md") and content:
                    deliverables.append((file_path, content))
    if not graded or not task_id:
        return None
    sample = "\n\n".join(prose)
    for file_path, content in deliverables:
        sample += f"\n\n[DELIVERABLE FILE {file_path}]\n{content[:CLAW_DELIVERABLE_CHARS]}"
    sample = sample.strip()
    return (task_id, sample) if sample else None


def extract_claw(trace_dir: Path, language: str) -> list[TaskText]:
    """results/<run>/claw/<lang>/*.jsonl, one judgement per graded trace."""
    out: list[TaskText] = []
    trials: dict[str, int] = defaultdict(int)
    for f in sorted(trace_dir.glob("*.jsonl")):
        got = extract_claw_trace(f)
        if not got:
            continue
        task_id, sample = got
        trials[task_id] += 1
        out.append(TaskText("claw", language, CLAW_SPLITS.get(task_id[:1], "-"),
                            f"{task_id}#{trials[task_id]}", sample,
                            target=CLAW_LANG_NAMES.get(language, language)))
    return out


# --------------------------------------------------------------------------
# the judge
# --------------------------------------------------------------------------

PROMPT = """You are auditing whether an AI assistant replied in the language it was supposed to use.

Target language: {language}

Below is everything the assistant said during one task, with its tool calls and \
the user's turns removed. Judge ONLY the language of the assistant's own prose.

Treat these as CORRECT, never as violations:
- Identifiers echoed from the environment: reservation/order/user IDs, flight, \
train and product codes, SKUs, phone numbers, addresses, dates, times, prices \
and currency symbols.
- Tool names, function names, argument names, JSON keys, code and file paths.
- Structural scaffolding the output format requires. deepplanning's travel plans, for example, are emitted inside <plan> tags with English field labels ("Day 1:", "Current City:", "Accommodation:", "Transportation:") because the scorer parses them; only the values around those labels should be in the target language. Markdown headings, table headers and bullet markers are likewise formatting, not prose.
- Proper nouns that the benchmark deliberately keeps in their original form: \
brand names, product model names, hotel/restaurant/attraction names, airline \
and city names. These benchmarks preserve such names on purpose so that tool \
calls still match, so their presence is expected and correct.
- Standard loanwords and technical terms that a fluent speaker of the target \
language would normally leave untranslated.

Count as a VIOLATION only prose the assistant composed itself -- sentences, \
explanations, questions, apologies, summaries -- written in a language other \
than the target. An empty or near-empty sample is not a violation.

Answer with a single JSON object and nothing else:
{{"consistent": true|false, "share_in_target": <0.0-1.0>, "observed_language": \
"<dominant language of the assistant's prose>", "evidence": "<at most 200 \
characters quoting the strongest off-language prose, or empty>"}}

share_in_target is your estimate of how much of the assistant's own prose was \
in the target language. Set consistent=false when meaningful prose is in the \
wrong language, not merely because identifiers or proper nouns appear.

--- ASSISTANT OUTPUT ---
{sample}
--- END ---"""

# claw's variant: the sample also carries the markdown deliverables the agent
# wrote, and claw has no <plan> scaffolding. The wording is the one the
# published claw numbers were judged with.
PROMPT_CLAW = """You are auditing whether an AI assistant replied in the language it was supposed to use.

Target language: {language}

Below is everything the assistant said during one task, with its tool calls and \
the user's turns removed. It also includes, at the end, any markdown deliverable \
file the assistant wrote (marked with [DELIVERABLE FILE ...]); judge that as the \
assistant's own prose too. Judge ONLY the language of the assistant's own prose.

Treat these as CORRECT, never as violations:
- Identifiers echoed from the environment: reservation/order/user IDs, flight, \
train and product codes, SKUs, phone numbers, addresses, dates, times, prices \
and currency symbols.
- Tool names, function names, argument names, JSON keys, code and file paths.
- Structural scaffolding the output format requires. Markdown headings, table \
headers and bullet markers are formatting, not prose; only the values/sentences \
around them should be in the target language.
- Proper nouns that the benchmark deliberately keeps in their original form: \
brand names, product model names, hotel/restaurant/attraction names, airline \
and city names, and terms the task explicitly asks to preserve.
- Standard loanwords and technical terms that a fluent speaker of the target \
language would normally leave untranslated.

Count as a VIOLATION only prose the assistant composed itself -- sentences, \
explanations, questions, apologies, summaries, and deliverable documents -- \
written in a language other than the target. An empty or near-empty sample is \
not a violation.

Answer with a single JSON object and nothing else:
{{"consistent": true|false, "share_in_target": <0.0-1.0>, "observed_language": \
"<dominant language of the assistant's prose>", "evidence": "<at most 200 \
characters quoting the strongest off-language prose, or empty>"}}

share_in_target is your estimate of how much of the assistant's own prose was \
in the target language. Set consistent=false when meaningful prose is in the \
wrong language, not merely because identifiers or proper nouns appear.

--- ASSISTANT OUTPUT ---
{sample}
--- END ---"""

PROMPTS = {"claw": PROMPT_CLAW}


@dataclass
class Verdict:
    task: TaskText
    consistent: Optional[bool] = None
    share: Optional[float] = None
    observed: str = ""
    evidence: str = ""
    error: str = ""


class Judge:
    """Minimal OpenAI-compatible chat client (stdlib only)."""

    def __init__(self, base_url: str, api_key: str, model: str,
                 headers: Optional[dict] = None, timeout: int = 120):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}
        if headers:
            self.headers.update(headers)
        if api_key and "Authorization" not in self.headers:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def __call__(self, prompt: str) -> dict:
        body = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }).encode("utf-8")
        req = urllib.request.Request(self.url, data=body, headers=self.headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            payload = json.loads(r.read().decode("utf-8"))
        return payload["choices"][0]["message"]["content"] or ""


_JSON_RE = re.compile(r"\{.*\}", re.S)


def judge_one(judge: Judge, task: TaskText, max_chars: int, retries: int = 2) -> Verdict:
    sample = task.text
    if len(sample) > max_chars:
        # keep both ends: drift often appears only after a long correct opening
        head, tail = max_chars * 2 // 3, max_chars // 3
        sample = sample[:head] + "\n[... truncated ...]\n" + sample[-tail:]
    prompt = PROMPTS.get(task.benchmark, PROMPT).format(
        language=task.target or task.language, sample=sample)
    last = ""
    for _ in range(retries + 1):
        try:
            raw = judge(prompt)
            m = _JSON_RE.search(raw)
            if not m:
                last = f"no JSON in reply: {raw[:120]}"
                continue
            got = json.loads(m.group(0))
            return Verdict(
                task=task,
                consistent=bool(got.get("consistent")),
                share=float(got.get("share_in_target", 0.0)),
                observed=str(got.get("observed_language", ""))[:40],
                evidence=str(got.get("evidence", ""))[:200],
            )
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            last = f"{type(e).__name__}: {e}"
        except (KeyError, ValueError, TypeError) as e:
            last = f"{type(e).__name__}: {e}"
    return Verdict(task=task, error=last)


# --------------------------------------------------------------------------
# discovery from a run manifest
# --------------------------------------------------------------------------

def collect_from_manifest(run_id: str) -> list[TaskText]:
    manifest = _read_json(RESULTS / run_id / "manifest.json")
    if not manifest:
        sys.exit(f"lang-consistency: no manifest at results/{run_id}/manifest.json")

    tasks: list[TaskText] = []
    claw_seen: set[str] = set()   # claw logs a run and a regrade step per language
    dp_seen: set[Path] = set()    # deepplanning dirs already read (one step per trial/domain)
    dp_found: dict[str, bool] = {}
    for step in manifest.get("steps", []):
        bench, lang = step["benchmark"], step["language"]
        out = REPO / step["output"]

        if bench in ("tau3", "vitabench"):
            unit = (out.parent.name if bench == "tau3"
                    else out.stem.rsplit("__", 1)[-1])
            if out.exists():
                tasks += extract_simulation_file(out, bench, lang, unit)
            else:
                print(f"  (skip) {bench}/{lang}/{unit}: {step['output']} missing",
                      file=sys.stderr)

        elif bench == "deepplanning":
            # bench gives every trial its own directories: travel trajectories
            # under TRAVEL_OUTPUT_DIR, shopping's inferred databases under
            # DEEPPLANNING_RUN_DIR. A step that has neither ran deepplanning's
            # legacy in-tree layout, so fall back to the source tree there.
            env = step.get("env", {})
            # deepplanning names its output directories with the full language
            # word ("japanese"), while the manifest carries the ISO code ("ja").
            dp_lang = env.get("DEEPPLANNING_LANGUAGE", lang)
            found = False
            travel_root = Path(env["TRAVEL_OUTPUT_DIR"]) if env.get("TRAVEL_OUTPUT_DIR") else None
            if travel_root and travel_root.exists() and travel_root not in dp_seen:
                dp_seen.add(travel_root)
                for traj in sorted(travel_root.rglob("trajectories")):
                    tasks += extract_deepplanning_travel(traj, lang)
                    found = True
            if env.get("DEEPPLANNING_RUN_DIR"):
                infer, latest_only = Path(env["DEEPPLANNING_RUN_DIR"]) / "database_infered", False
            else:
                infer, latest_only = BENCHMARKS / "deepplanning/shoppingplanning/database_infered", True
            if infer.exists() and infer not in dp_seen:
                dp_seen.add(infer)
                runs = sorted(infer.glob(f"*_{dp_lang}_level*"),
                              key=lambda p: p.stat().st_mtime)
                if latest_only:                         # in-tree: newest run per level
                    runs = runs[-3:]
                for r in runs:
                    level = r.name.split("_level")[-1].split("_")[0]
                    tasks += extract_deepplanning_shopping(r, lang, level)
                    found = True
            dp_found[lang] = dp_found.get(lang, False) or found

        elif bench == "claw":
            # claw logs a run step and a regrade step per language; same traces.
            if step["output"] in claw_seen:
                continue
            claw_seen.add(step["output"])
            got = extract_claw(out.parent, lang)
            if not got:
                print(f"  (skip) claw/{lang}: no graded traces in {out.parent.relative_to(REPO)}",
                      file=sys.stderr)
            tasks += got
    for lang, found in dp_found.items():
        if not found:
            print(f"  (skip) deepplanning/{lang}: no trajectories found", file=sys.stderr)
    return tasks


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

@dataclass
class Bucket:
    consistent: int = 0
    total: int = 0
    errors: int = 0
    shares: list[float] = field(default_factory=list)
    examples: list[Verdict] = field(default_factory=list)

    @property
    def rate(self) -> Optional[float]:
        return self.consistent / self.total if self.total else None


def summarize(verdicts: list[Verdict]) -> tuple[dict, dict]:
    by_lang: dict[str, Bucket] = defaultdict(Bucket)
    by_pair: dict[tuple[str, str], Bucket] = defaultdict(Bucket)
    for v in verdicts:
        for b in (by_lang[v.task.language], by_pair[(v.task.benchmark, v.task.language)]):
            if v.error:
                b.errors += 1
                continue
            b.total += 1
            b.consistent += bool(v.consistent)
            if v.share is not None:
                b.shares.append(v.share)
            if not v.consistent and len(b.examples) < 3:
                b.examples.append(v)
    return by_lang, by_pair


def as_markdown(by_lang, by_pair, run_id: str, model: str) -> str:
    def pct(x): return "n/a" if x is None else f"{100 * x:.1f}%"
    lines = [
        f"# Language consistency — run `{run_id}`",
        "",
        f"Judge model: `{model}`. Score = share of tasks whose assistant prose the",
        "judge found to be in the requested language. Identifiers, tool names and",
        "deliberately-preserved proper nouns are not counted as violations.",
        "",
        "## Per language",
        "",
        "| language | consistent | tasks | mean share in target | errors |",
        "|---|---:|---:|---:|---:|",
    ]
    for lang in sorted(by_lang, key=lambda l: (by_lang[l].rate is None, by_lang[l].rate or 0)):
        b = by_lang[lang]
        mean = sum(b.shares) / len(b.shares) if b.shares else None
        lines.append(f"| {lang} | {pct(b.rate)} | {b.total} | {pct(mean)} | {b.errors} |")

    lines += ["", "## Per benchmark × language", "",
              "| benchmark | language | consistent | tasks |", "|---|---|---:|---:|"]
    for (bench, lang) in sorted(by_pair):
        b = by_pair[(bench, lang)]
        lines.append(f"| {bench} | {lang} | {pct(b.rate)} | {b.total} |")

    flagged = [(l, v) for l, b in by_lang.items() for v in b.examples]
    if flagged:
        lines += ["", "## Examples flagged as off-language", ""]
        for lang, v in flagged[:15]:
            lines.append(f"- **{lang}** `{v.task.key}` — observed *{v.observed}*: "
                         f"{v.evidence[:160]}")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------

def load_judge(model_override: Optional[str]) -> Judge:
    import yaml
    cfg_path = CONFIGS / "models.yaml"
    if not cfg_path.exists():
        sys.exit("lang-consistency: configs/models.yaml not found")
    raw = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

    def expand(v):
        if isinstance(v, str):
            return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}",
                          lambda m: os.environ.get(m.group(1), m.group(0)), v)
        if isinstance(v, dict):
            return {k: expand(x) for k, x in v.items()}
        if isinstance(v, list):
            return [expand(x) for x in v]
        return v

    raw = expand(raw)
    roles = raw.get("roles") or {}
    name = model_override or roles.get("lang_judge") or roles.get("evaluator")
    if not name:
        sys.exit("lang-consistency: set roles.lang_judge (or roles.evaluator) "
                 "in configs/models.yaml, or pass --judge-model")
    default = raw.get("default", {})
    entry = next((m for m in raw.get("models", []) if m["name"] == name), None)
    if entry is None:
        sys.exit(f"lang-consistency: judge model {name!r} not defined in models.yaml")
    merged = {**default, **entry}
    headers = merged.get("headers") or {}
    auth = headers.get("Authorization", "")
    key = auth.split(None, 1)[1] if auth.lower().startswith("bearer ") else auth
    return Judge(merged.get("base_url", ""), key,
                 merged.get("model_name", name), headers=headers)


def main() -> int:
    try:                        # keep progress visible under redirection
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)
    except AttributeError:      # pragma: no cover
        pass

    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--run-id", help="a finished `bench run`")
    src.add_argument("--path", help="a single results/simulation file to audit")
    p.add_argument("--language", help="target language (required with --path)")
    p.add_argument("--benchmark", default="tau3", help="benchmark for --path")
    p.add_argument("--judge-model", help="override roles.lang_judge")
    p.add_argument("--granularity", choices=("task", "language"), default="task",
                   help="task (default): judge each task, report the rate. "
                        "language: one truncated blob per language, the literal "
                        "single-call reading")
    p.add_argument("--max-tasks-per-language", type=int,
                   help="sample at most N tasks per language to bound cost")
    p.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    p.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    p.add_argument("--dry-run", action="store_true",
                   help="report what would be judged and stop, calling nothing")
    a = p.parse_args()

    if a.path:
        if not a.language:
            sys.exit("lang-consistency: --path requires --language")
        tasks = extract_simulation_file(Path(a.path), a.benchmark, a.language, "-")
        run_id = "adhoc"
    else:
        tasks = collect_from_manifest(a.run_id)
        run_id = a.run_id

    if not tasks:
        print("lang-consistency: nothing to judge (no assistant text found)",
              file=sys.stderr)
        return 1

    if a.max_tasks_per_language:
        kept: list[TaskText] = []
        seen: dict[str, int] = defaultdict(int)
        for t in tasks:
            if seen[t.language] < a.max_tasks_per_language:
                kept.append(t)
                seen[t.language] += 1
        if len(kept) < len(tasks):
            print(f"lang-consistency: sampled {len(kept)}/{len(tasks)} tasks "
                  f"(--max-tasks-per-language {a.max_tasks_per_language})",
                  file=sys.stderr)
        tasks = kept

    if a.granularity == "language":
        merged: dict[str, TaskText] = {}
        for t in tasks:
            if t.language in merged:
                merged[t.language].text += "\n\n" + t.text
            else:
                merged[t.language] = TaskText(t.benchmark, t.language, "(all)",
                                              "(all)", t.text)
        tasks = list(merged.values())

    total_chars = sum(len(t.text) for t in tasks)
    print(f"lang-consistency: {len(tasks)} judgement(s), "
          f"{total_chars:,} chars (~{total_chars // 4:,} tokens before truncation)",
          file=sys.stderr)
    if a.dry_run:
        for lang in sorted({t.language for t in tasks}):
            n = sum(1 for t in tasks if t.language == lang)
            c = sum(len(t.text) for t in tasks if t.language == lang)
            print(f"  {lang:16s} {n:5d} judgement(s)  {c:,} chars", file=sys.stderr)
        print("dry run -- no API calls made", file=sys.stderr)
        return 0

    judge = load_judge(a.judge_model)
    verdicts: list[Verdict] = []
    with ThreadPoolExecutor(max_workers=a.concurrency) as pool:
        futures = {pool.submit(judge_one, judge, t, a.max_chars): t for t in tasks}
        for i, fut in enumerate(as_completed(futures), 1):
            verdicts.append(fut.result())
            if i % 25 == 0 or i == len(futures):
                print(f"  judged {i}/{len(futures)}", file=sys.stderr)

    by_lang, by_pair = summarize(verdicts)
    text = as_markdown(by_lang, by_pair, run_id, judge.model)
    print(text)

    if a.run_id:
        out_dir = RESULTS / run_id
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "lang_consistency.md").write_text(text, encoding="utf-8")
        (out_dir / "lang_consistency.json").write_text(json.dumps({
            "run_id": run_id,
            "judge_model": judge.model,
            "granularity": a.granularity,
            "per_language": {
                l: {"consistent_rate": b.rate, "tasks": b.total, "errors": b.errors,
                    "mean_share_in_target": (sum(b.shares) / len(b.shares)) if b.shares else None}
                for l, b in by_lang.items()
            },
            "per_benchmark_language": {
                f"{bch}/{lng}": {"consistent_rate": b.rate, "tasks": b.total}
                for (bch, lng), b in by_pair.items()
            },
            "flagged": [
                {"task": v.task.key, "observed": v.observed, "evidence": v.evidence}
                for b in by_lang.values() for v in b.examples
            ],
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"written to results/{run_id}/lang_consistency.{{md,json}}",
              file=sys.stderr)

    errs = sum(b.errors for b in by_lang.values())
    if errs:
        print(f"lang-consistency: {errs} judgement(s) failed", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
