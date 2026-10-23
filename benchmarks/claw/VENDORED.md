# Provenance of benchmarks/claw

This directory is a copy of the multilingual Claw-Eval fork (23 languages) that
the paper's claw numbers were produced with. Upstream is Claw-Eval v1.0.0
(https://claw-eval.github.io, arXiv 2604.06132). `bench` drives it unchanged.

## Changes relative to upstream carried in `src/`

These are what the published runs used.

| file | change |
|---|---|
| `runner/providers/anthropic_native.py` | **new.** Agent provider speaking the Anthropic Messages protocol, selected by `model.provider: anthropic_native`. Claude's extended thinking is accepted but not engaged on the OpenAI-compatible route. |
| `config.py` | `model.provider` (`openai_compat` default), `model.echo_reasoning` (default true), `user_agent_model.api_format` (`openai` default, or `vertex`). |
| `cli.py` | Every agent-provider construction goes through `_make_model_provider`, which dispatches on `model.provider`; the user simulator receives `api_format`. |
| `runner/providers/openai_compat.py` | Re-sent assistant turns carry `reasoning_content` as well as `reasoning`; `echo_reasoning: false` strips both. `wrap_extra_body_for_gateway` moves a `google` block under a literal `extra_body` key (agent and user simulator). Transient upstream 404 / `upstream_error` responses are retried. |
| `runner/user_agent.py` | `api_format: vertex` calls Gemini `generateContent` directly, sending the key as `x-goog-api-key: Bearer <key>` (the form the gateway behind the published runs expects; Google's own endpoint takes the bare key). |
| `graders/llm_judge.py` | A judge request rejected as too large fails at once instead of exhausting its retries; the payload cannot shrink on retry. |
| `models/trace.py`, `runner/loop.py` | The trace header records `reasoning_effort`. `CLAW_EVAL_TIMEOUT_MULT` (default 1) scales every task's time limit; `bench` copies it into the run manifest when set. |

## Removed for this release

None of the following is on the run or grading path:

- the fork's failure-analysis module (`src/claw_eval/failure_analysis/` and the
  `analyze` / `failure-report` / `vocab` subcommands) and its tests;
- the translation, localization and validation tooling under `scripts/`, and
  the tests that gated the translated data. `scripts/generate_task_subset.py`
  remains as the provenance of the frozen `standard` subset;
- internal reproduction notes and data, per-model run configs, sweep scripts
  and local credentials.

Error messages that pointed at the removed translation scripts now point at
`bench fetch-data`, and the DashScope search backend no longer echoes its API
key in error logs.

## Task data

`tasks/` is git-ignored by the suite and filled in place by `bench fetch-data`
from `<source>/claw/tasks`. It is not moved to `data/` because claw resolves it
relative to its own checkout: `batch` starts mock services from the tasks dir's
parent and `graders/base.py` loads peer graders from `<checkout>/tasks`,
falling back silently to the zh grader when one is missing.

## How `bench` runs it

`bench run -b claw` runs `claw-eval batch` from this directory with
`--task-subset standard --language <iso> --sandbox --continue
results/<run-id>/claw/<lang>/`, then once more with `--regrade` to grade any
trace the judge missed. `CLAW_EVAL_FIXTURES_ROOT` points at `tasks/` so traces
stored under `results/` can be rehydrated when graded. See the top-level
README for the flags.
