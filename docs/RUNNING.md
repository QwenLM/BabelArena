# Running BabelArena

The [README](../README.md) gets you from clone to Pass^k. This page covers the
rest: what each flag does, what each benchmark needs, how to read the output,
and the things that bite on a first run.

- [Requirements](#requirements)
- [Setup and data](#setup-and-data)
- [Configuring models](#configuring-models)
- [Running](#running)
  - [What `standard` means](#what-standard-means)
  - [claw](#claw)
  - [deepplanning](#deepplanning)
  - [tau3](#tau3)
- [Reading the results](#reading-the-results)
- [Language consistency](#language-consistency)
- [Commands](#commands)
- [Credentials](#credentials)
- [Layout](#layout)
- [Environments and tokenizers](#environments-and-tokenizers)
- [Languages](#languages)
- [What is not shipped](#what-is-not-shipped)

The four benchmark families keep their upstream directory names in this
repository: **tau3** (τ³-Bench), **vitabench** (VitaBench), **deepplanning**
(DeepPlanning) and **claw** (ClawEval).

## Requirements

- Python **3.12** (tau3, vitabench, claw) and **3.10 or 3.11** (deepplanning)
  on `PATH`. The four cannot share an interpreter; see
  [Environments](#environments-and-tokenizers).
- **Docker**, for claw's tool sandbox.
- **PyYAML** for `bench` itself (`pip install pyyaml`).
- An OpenAI-compatible endpoint serving the agent under test and the support
  models (user simulator, judge, deepplanning's plan converter).
- About 14 GB of disk for the data, more for run output.

## Setup and data

```bash
./bench setup            # one virtualenv per benchmark + claw's sandbox image
./bench fetch-data --source /path/to/BabelArena-data
./bench check            # data, environments, config -- no API calls
```

`bench setup` builds `.venvs/<benchmark>/`, prepares the two BM25 tokenizers
and builds the `claw-eval-agent:latest` Docker image. Re-running it is safe: it
skips virtualenvs that exist and only redoes the cheap steps.

`bench fetch-data` fills `data/` (tau3, vitabench, deepplanning) and
`benchmarks/claw/tasks/` (claw). The hosted dataset is not published yet, so
for now pass `--source <directory>` holding `tau3/`, `vitabench/`,
`deepplanning/` and `claw/tasks/`. `DATA_SOURCE_DEFAULT` in `bench` takes the
published location once there is one.

claw's data comes as three archives, one per split, each holding
`claw/tasks/<task_id>/...`:

```bash
mkdir -p /tmp/babel-data
for f in claw_general.tar.gz claw_multimodal.tar.gz claw_multi_turn.tar.gz; do
  tar -xzf "$f" -C /tmp/babel-data
done
./bench fetch-data --source /tmp/babel-data
```

They hold the 167 `standard` tasks plus the 16 tasks those depend on: a language
variant's grader inherits from its source task's grader, and one task reads
another's fixtures. The dependencies are not in the `standard` lists and never
run; without them claw would quietly grade with the wrong grader. Because only
these 183 of claw's 300 tasks ship, `--subset full` does not reproduce a
full-set claw number. `scripts/package_claw_data.py` builds the archives,
byte-identically from the same tree, and lists their contents and checksums in
`claw_MANIFEST.json` / `claw_SHA256SUMS`.

## Configuring models

```bash
cp configs/models.yaml.example configs/models.yaml
export REQUEST_BASE_URL="https://your-endpoint/v1/chat/completions"
export REQUEST_API_KEY="..."
```

`configs/models.yaml` is the one model config; `bench` renders it into each
runner's native format at run time. Two rules:

- **`base_url` is the full endpoint, ending in `/chat/completions`.** tau3 and
  vitabench POST it verbatim; `bench` strips the suffix for deepplanning and
  claw, which drive the OpenAI SDK. Leaving it off fails with an opaque HTTP 500.
- **Keys are `${ENV_VAR}` references, never literals.** `bench` refuses a file
  that looks like it holds a key. See [Credentials](#credentials).
- **Every `${ENV_VAR}` in the file must be set**, including those of models you
  do not run; `bench` stops and names any that are missing. Delete or comment
  out entries you do not need.

Besides the agent under test, a run needs support models, named under `roles:`:

| Role | Used by | Paper setting |
|---|---|---|
| `user` | the simulated user in tau3, vitabench and claw's multi_turn split | Gemini-3.5-Flash, thinking off |
| `evaluator` | the LLM judge of vitabench, tau3 (natural-language assertions) and claw | GPT-5.6-Sol |
| `conversion` | deepplanning's travel plan converter (free text → scoreable JSON) | Gemini-3.5-Flash |
| `lang_judge` | the language-consistency judge (falls back to `evaluator`) | Gemini-3.7-Flash |

These are part of the measuring instrument, not the system under test. Keep
them fixed across everything you compare: a different judge or simulator moves
the scale, and a weak converter silently depresses deepplanning's travel scores.

A model entry may carry a `claw:` block with settings only claw understands,
for example `provider: anthropic_native` to call a Claude model through the
Anthropic Messages protocol (the only route on which its extended thinking
engages), or `api_format: vertex` for a Gemini user simulator on its native
route. `models.yaml.example` shows both.

## Running

```bash
./bench run -b all -l all --agent-model <model>        # the paper's protocol
./bench run -b all -l all --agent-model <model> --dry-run   # print, run nothing
```

| Flag | Default | Effect |
|---|---|---|
| `-b/--benchmark` | `all` | `tau3`, `vitabench`, `deepplanning`, `claw` or `all` |
| `-l/--language` | required | a code or name, a comma-separated list (`ja,fr,ar`), or `all` for the 23 |
| `--agent-model` | required | the system under test, as named in `models.yaml` |
| `--domain` | all | restrict to domains, e.g. `--domain airline retail`; benchmarks without them are skipped |
| `--subset` | `standard` | `standard`, `full`, or a custom subset name |
| `--num-trials` | **3** | independent trials per task; Pass^3 needs three |
| `--num-tasks N` | whole subset | only the first N tasks of each unit -- for smoke tests |
| `--concurrency` | 4 | parallel tasks per benchmark step |
| `--run-id` | timestamp | reuse an id to resume an interrupted run |
| `--lang-consistency` | off | run the [language-consistency](#language-consistency) audit afterwards |

A full run is large: 699 tasks × 23 languages × 3 trials per agent. Smoke-test
first:

```bash
./bench run -b all -l en --agent-model <model> --num-tasks 1 --num-trials 1
```

Every run writes `results/<run_id>/manifest.json` recording each step's command
line, non-secret environment and exit code. Re-running with the same
`--run-id` resumes: tau3, vitabench and claw skip finished work, deepplanning
skips finished shopping levels and travel cases.

### What `standard` means

Every benchmark ships a frozen task subset named `standard`, the default
everywhere. It is a fixed sample chosen once by task ID, so **the same tasks run
in every language** and cross-language numbers stay comparable at roughly half
the cost of the full set.

| Benchmark | Unit | full | standard |
|---|---|---:|---:|
| tau3 | airline | 50 | **50** |
| | retail | 114 | 57 |
| | telecom | 114 | 57 |
| | banking_knowledge | 97 | 48 |
| vitabench | delivery / instore / ota / cross | 100 each | 50 each |
| deepplanning | travel | 120 | 60 |
| | shopping L1 / L2 | 50 each | 25 each |
| | shopping L3 | 20 | 10 |
| claw | general | 161 | 81 |
| | multimodal | 101 | 48 |
| | multi_turn | 38 | **38** |
| **total** | | **1,315** | **699** |

- **airline is not sampled.** It has only 50 tasks, and halving it would leave
  too much sampling noise, so `standard` keeps all 50. tau3's `standard` is
  therefore 212/375 = 57% of full.
- **tau3's telecom denominator is 114, not 2285.** `tasks.json` holds a
  generated `full` split used for RL training; evaluation uses the `base` split,
  the 114-task set matching the original τ-bench structure.
- **claw's multi_turn is not sampled either** (38 tasks), and claw's three
  splits always run as one batch: `--domain` cannot select one of them alone.

Scores from different subsets are not comparable.

### claw

claw runs every tool call inside a Docker container (`claw-eval-agent:latest`)
next to a set of local mock services (mail, calendar, files, web, OCR, ...).
Each language is two steps: the run itself, then a `--regrade` pass that grades
any trace the judge missed and refills tasks still short of `--num-trials`.

| Flag | Effect |
|---|---|
| `--claw-port-offset N` | Shift the mock-service ports (9100 and up) so two claw runs can share a host |
| `--claw-no-sandbox` | Run tools on the host instead of in Docker. Scores are not comparable with sandboxed runs |

If `CLAW_EVAL_TIMEOUT_MULT` is set in your shell, claw scales every task's time
limit by it; `bench` records the value in the manifest and flags the run as not
comparable with default-limit runs.

Things worth knowing before a first run:

- **Web search needs a key and internet access.** 49 of the 167 `standard`
  tasks start the `web_real` mock service, which forwards `/web/search` to a
  real search API and fetches pages for `/web/fetch` from the live web. Export
  the key in the shell you run `bench` from; `bench` passes the environment
  through to claw:

  ```bash
  export SERP_DEV_KEY="..."            # SERP backend (default); SERP_API_URL overrides its endpoint
  # or
  export WEB_SEARCH_PROVIDER=dashscope DASHSCOPE_SEARCH_KEY="..."
  ```

  Without a key the run still completes, but every search returns no results
  and those tasks score accordingly, so record which backend a run used and
  keep it fixed across everything you compare.

- **Time limits are wall-clock, per task** (120–1800 s across `standard`; most
  are 600 or 900 s). A slow endpoint fails tasks on time rather than on
  ability: at ~75 s per model call, a 180 s task gets two or three turns. A
  run that times out shows `[timeout] ... exceeded limit` in its log and
  scores completion 0 without ever calling the judge. Check your endpoint's
  latency before reading low scores as a weak model.
- **Some graders enforce how the work is done, not only the result.** The
  figure-reproduction tasks, for instance, score 0 unless the script uses a
  plotting library. A 0 with no judge call is usually one of these checks or a
  timeout, not an infrastructure failure.
- **Custom subsets** live in `benchmarks/claw/task_subsets/<name>/`, one
  `general.txt` / `multimodal.txt` / `multi_turn.txt` of task ids each; pass
  `--subset <name>`. Every split needs at least one id -- claw rejects an empty
  manifest. Names starting with `smoke-` are git-ignored.
- **An interrupted run can leave sandbox containers behind**, named
  `claw-agent-<task>-t<trial>-p<port offset>`. Remove them with `docker rm -f`
  before reusing the same `--claw-port-offset`, and likewise any mock service
  still listening on the ports that offset uses.

### deepplanning

deepplanning has no trial flag of its own, so `bench` runs it once per trial,
each trial in its own directory (`results/<run_id>/deepplanning/<lang>/trial<N>/`).
`bench report` scores every trial from its own directory and averages them.

The travel domain runs inference, then a **conversion** pass that reformats the
agent's free-text plan into scoreable JSON, then evaluation. The conversion
model is `roles.conversion`; a weak one depresses travel scores without failing
anything. Shopping needs its BM25 tokenizer prepared by `bench setup`.

Its metrics, per domain:

| Domain | Metric | Meaning |
|---|---|---|
| shopping | `match_rate` | share of expected items the agent matched |
| shopping | `weighted_average_case_score` | mean per-case completion score |
| travel | `case_acc` | share of cases that satisfy every constraint |
| travel | `commonsense_score` / `personalized_score` | commonsense-constraint and personalized-requirement satisfaction |
| travel | `composite_score` | weighted combination of the two |
| both | `avg_acc` | mean of shopping `weighted_average_case_score` and travel `case_acc`; the headline number |

All are computed over the cases of the subset run, so numbers from different
subsets are not comparable.

### tau3

`banking_knowledge` builds a BM25 index over its document corpus and needs a
tokenizer (prepared by `bench setup`) plus the retrieval dependencies installed
into tau3's virtualenv. Drop it with `--domain airline retail telecom` if you do
not want them.

## Reading the results

```bash
./bench report --run-id <id>
```

prints two tables. The first puts each benchmark's own headline metric side by
side. It does **not** average them into one score: a tool-call correctness rate,
an LLM-judged pass rate and a constraint-satisfaction accuracy do not share a
scale.

| Benchmark | Metric | Notes |
|---|---|---|
| tau3 | `mean_reward` | 1.0 only if the final DB state matches *and* every required action fired |
| vitabench | `mean_reward` | assigned by an LLM judge; comparable only across runs using the **same judge model** |
| deepplanning | `avg_acc` | mean of shopping `weighted_average_case_score` and travel `case_acc`, averaged over trials |
| claw | `avg_score` | mean composite `task_score` (completion, safety, robustness, judged communication) |

The second is the paper's scale, **Pass^1 and Pass^3**, per benchmark and
language (`scripts/passk_report.py`, also runnable on its own). Each trial
counts as passed on its benchmark's own full-success bit: reward 1.0 for tau3
and vitabench, a perfect case score for deepplanning, claw's `passed` flag.
With *s* passes out of *n* trials of a task,

```
Pass^k = mean over tasks of C(s, k) / C(n, k)
```

so Pass^1 is the per-trial success rate and, with three trials, Pass^3 counts a
task only if all three trials pass.

## Language consistency

Task reward says whether the agent did the right thing, not whether it did it
in the user's language: an agent can score full reward while answering a Thai
user in English. That is measured separately, and is opt-in because it costs a
judge call per trajectory:

```bash
./bench run -b all -l th --agent-model <m> --lang-consistency   # after the run
./bench lang-check --run-id <id>                                # or later
./bench lang-check --run-id <id> --dry-run                      # size it, call nothing
```

Each trajectory's user-visible text -- the assistant's replies and the text it
writes before tool calls; for claw also the markdown deliverables it writes --
goes to `roles.lang_judge` with the target language. Reasoning, user turns, tool
calls and tool results are excluded. A trajectory is consistent only if all of
it is in the target language; the report gives the consistent share per
language and per benchmark, plus quoted evidence for the trajectories that
drifted.

The judge is told to ignore what these benchmarks deliberately keep in the
original: entity IDs, tool and argument names, preserved brand and place names,
and the English field labels deepplanning's `<plan>` format requires
(`Day 1:`, `Current City:`). Without that it reports drift that is not there.
The prompt is the one in the paper's Appendix A.

Judging is per trajectory rather than one blob per language because one
vitabench language is ~5.5M characters, far past any context window.
`--lang-max-tasks N` samples to bound cost.

## Commands

| Command | What it does |
|---|---|
| `bench setup` | Build the four virtualenvs, prepare both BM25 tokenizers, build claw's sandbox image |
| `bench fetch-data` | Fetch the ~14 GB of data (into `data/`, and claw's into `benchmarks/claw/tasks/`) |
| `bench check` | Verify data, environments and config. Makes no API calls |
| `bench languages` | Print the 23 languages and each benchmark's spelling of them |
| `bench run` | Run one or more benchmarks |
| `bench report` | Per-benchmark headline metrics, then Pass^1 / Pass^3 |
| `bench lang-check` | Audit which language the agent actually replied in |
| `bench clean` | Delete `.runtime/` (`--configs`, `--results`, `--venvs` for more) |

## Credentials

Your API key is never written into a file you would commit.
`configs/models.yaml` holds only `${ENV_VAR}` references. The runners do need a
real key on disk, so `bench run` expands those references into `.runtime/`,
mode 0600 and git-ignored -- the one place a credential lands. Clear it when you
are done, particularly before archiving or sharing a working tree:

```bash
./bench clean                    # remove .runtime/
./bench clean --configs          # ...and configs/models.yaml
```

Nothing under `results/` records a credential: manifests store the command
line and the non-secret environment only.

## Layout

```
bench                         unified CLI
configs/
  languages.yaml              language identity across the four benchmarks
  models.yaml.example         one model config, rendered into four native formats
benchmarks/                   code, in git
  tau3/  vitabench/  deepplanning/
  claw/                       code + task_subsets/; tasks/ (3.1 GB) fetched in place
data/                         fetched, not in git (except task_subsets/)
  tau3/                       tau2/domains/ + task_subsets/
  vitabench/                  vita/domains/ + task_subsets/
  deepplanning/               travelplanning/database/ + shoppingplanning/database_level*/
                              + task_subsets/
scripts/
  report.py                   per-benchmark headline metrics
  passk_report.py             Pass^1 / Pass^3 on one scale
  lang_consistency.py         the language-consistency audit
results/<run_id>/             manifest.json and each benchmark's output
docs/RUNNING.md               this page
```

`data/*/task_subsets/` **is** committed: a few KB of task IDs that define what
`standard` means. Each runner is pointed at `data/` by an environment variable
`bench` sets (`TAU2_DATA_DIR`, `VITA_DATA_DIR`, `DEEPPLANNING_DATA_DIR`).
`bench` only translates arguments and renders config; it never reimplements a
runner, which keeps numbers comparable with runs made through the native CLIs.

**claw's task data is the one exception to `data/`.** Its 300 task directories
(3.1 GB; fixtures include PDFs and 65 videos) are fetched into
`benchmarks/claw/tasks/`, which is git-ignored, and its subsets stay in
`benchmarks/claw/task_subsets/`. claw starts its mock services and loads each
language's grader relative to its own checkout -- a grader it cannot find
silently falls back to the Chinese one -- so moving them would mean patching
claw.

deepplanning dominates the footprint: its travel database is materialised per
case per language, about 375 MB × 23.

## Environments and tokenizers

tau3 requires Python ≥3.12 while deepplanning pins a Hugging Face stack that
wants 3.10, so `bench setup` builds one virtualenv each under `.venvs/` and
`bench` activates the right one per step. claw (Python ≥3.11) also needs
Docker; `bench check` reports whether its image is present.

Two domains build a BM25 index and need a tokenizer before they will run:
tau3's `banking_knowledge` and deepplanning's `shopping`. Neither downloads one
mid-benchmark -- they refuse to start instead -- so `bench setup` prepares both
and records what it did in `.runtime/tokenizers.json`, which `bench run` reads.

Both come from Hugging Face by default. Behind a TLS-inspecting proxy that fails
with a self-signed-certificate error; point setup at a local checkpoint instead
(any Qwen3 checkpoint works -- the family shares a tokenizer):

```bash
./bench setup --tokenizer-model /path/to/Qwen3-8B
```

## Languages

All four benchmarks ship the same 23 languages; `bench languages` prints them
with each benchmark's spelling. The benchmarks spell languages differently
(`TAU2_LANGUAGE="Eastern Panjabi"` vs `--language punjabi` vs `--language pa`);
`configs/languages.yaml` is the one place that maps between them, and `bench`
accepts the ISO code or the English name.

German is deliberately absent. tau3's tree carried partial German artifacts
(policy, tasks, tool descriptions) but no localized database in any domain, so
a German run had nothing to score against.

## What is not shipped

- **The translation and DB-rendering pipeline** for all four benchmarks. All
  23 languages arrive pre-rendered; adding a 24th is not supported here.
- **tau3 voice mode.** The release is text-only; voice task files and audio
  assets are excluded.
- **Upstream baseline trajectories.** `tau2-bench`'s shipped result archive is
  not redistributed.

Attribution, and the list of changes made to each upstream benchmark, are in
[NOTICE](../NOTICE); `benchmarks/claw/VENDORED.md` records claw's source
snapshot.
