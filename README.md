<div align="center">

  <h2>BabelArena: A Large-Scale Multilingual Benchmark for LLM Agents</h2>

</div>

<p align="center">
  <a href="https://arxiv.org/abs/2609.23490">
    <img src="https://img.shields.io/badge/arXiv-2609.23490-b31b1b.svg?logo=arxiv" alt="arXiv Badge"/>
  </a>
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?logo=open-source-initiative" alt="Apache-2.0 License Badge"/>
  </a>
</p>

## 📖 Introduction

**BabelArena** is a multilingual benchmark for LLM agents: **699 canonical
tasks** from **four agent benchmark families**, spanning **13 domains**, each
adapted into **23 languages** for **16,077 task instances**. Every language
variant keeps the source task identity and evaluation criteria, so agent
performance can be compared across languages on exactly the same tasks.

The language variants were built with **BabelFlow**, an agentic workflow that
traces each benchmark's runtime data flow to find the text it can safely
translate, translates it consistently across tasks, tools, databases, simulated
users and graders, and accepts a variant only after multi-layer verification and
human review.

Evaluating five frontier models, we find that no single model leads across all
four families, and that the gaps between languages go beyond task success:
lower-resource languages show larger shares of tool-use and control-flow
errors, consume up to roughly twice the input tokens of English on the same
tasks, and lose language consistency, with switches directed overwhelmingly
toward English.

## ✨ Features

- 🧩 **Four complementary agent settings.** Interactive services, long-horizon
  planning, knowledge-grounded tool use and heterogeneous autonomous tasks, each
  scored by its source benchmark's own evaluator.

  | Family | What it tests | Domains | Tasks |
  |---|---|---|---:|
  | [VitaBench](https://github.com/meituan-longcat/vitabench) | versatile interactive tasks with a simulated user | delivery, in-store, online travel, cross-domain | 200 |
  | [DeepPlanning](https://huggingface.co/datasets/Qwen/DeepPlanning) | long-horizon planning under verifiable constraints | travel, shopping | 120 |
  | [τ³-Bench](https://github.com/sierra-research/tau2-bench) (text) | simulated-user interaction, tool calling, knowledge retrieval, policy compliance | airline, retail, telecom, banking | 212 |
  | [ClawEval](https://claw-eval.github.io) | service orchestration, multimodal perception and generation, professional dialogue | general, multimodal, multi-turn | 167 |
  | **Total** | | **13** | **699** |

- 🌍 **23 languages, 15 scripts, three resource levels.** The languages vary in
  writing direction, word delimiters and glyph shaping.

  | High resource (7) | Medium resource (8) | Low resource (8) |
  |---|---|---|
  | English `en` · Chinese `zh` · Japanese `ja` · French `fr` · Russian `ru` · Arabic `ar` · Spanish `es` | Korean `ko` · Indonesian `id` · Hindi `hi` · Thai `th` · Hebrew `he` · Turkish `tr` · Vietnamese `vi` · Malay `ms` | Belarusian `be` · Eastern Panjabi `pa` · Kazakh `kk` · Khmer `km` · Burmese `my` · Lao `lo` · Tamil `ta` · Telugu `te` |

- 🔧 **Every component adapted.** System, simulator and evaluation prompts, task
  inputs, tool descriptions and environment content are all localized, with
  shared entities kept consistent across them. Among the multilingual agent
  benchmarks below, BabelArena adapts every component and has the broadest
  language and domain coverage.

  | Benchmark | Prompt | Task | Tool | Env. | Tasks | Domains | Languages | Instances |
  |---|:---:|:---:|:---:|:---:|---:|---:|---:|---:|
  | MAPS | ✗ | ✓ | ✗ | ✗ | 805 | 4 | 12 | 9,660 |
  | GAIA-v2-LILT | ✓ | ✓ | ✗ | ✗ | 165 | 1 | 6 | 990 |
  | OmnilingualGAIA2 | ✓ | ✓ | ✗ | ✓ | 640 | 1 | 11 | 7,040 |
  | MLCL | ✗ | ✓ | ✗ | ✗ | 200 | 1 | 4 | 800 |
  | SEATauBench | ✓ | ✓ | ✓ | ✓ | 278 | 3 | 6 | 1,668 |
  | PolyWorkBench | ✓ | ✓ | ✗ | ✓ | 67 | 5 | 10 | 67 |
  | **BabelArena** | ✓ | ✓ | ✓ | ✓ | **699** | **13** | **23** | **16,077** |

- ✅ **Verified translation quality.** On 4,600 sampled translations (200 per
  language), mean quality is 4.28 / 4.02 / 3.91 out of 5 for high-, medium- and
  low-resource languages (human experts for high-resource, inter-annotator
  Cohen's κ = 0.71). In a controlled ablation, BabelFlow cuts tasks with broken
  references from 20.0% to 2.5% and behavioral mismatches from 5.0% to 0.0%
  compared with independent field translation.

- 📏 **Task success and language consistency, measured separately.** Every task
  runs three independent trials and reports **Pass^1** (the per-trial success
  rate) and **Pass^3** (all three trials succeed), plus **language consistency
  (LC)**, the share of trajectories whose user-visible text stays in the target
  language.

## 🏆 Main Results

Five frontier models on BabelArena, in percent; higher is better, best in bold.

**By benchmark family**

| Model | VitaBench<br>Pass^1 | <br>Pass^3 | <br>LC | DeepPlanning<br>Pass^1 | <br>Pass^3 | <br>LC | τ³-Bench<br>Pass^1 | <br>Pass^3 | <br>LC | ClawEval<br>Pass^1 | <br>Pass^3 | <br>LC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude-Opus-4.8 | 36.9 | 20.1 | 98.5 | 36.2 | 17.2 | 61.8 | 62.6 | 49.5 | **95.0** | **55.8** | **43.0** | 96.3 |
| GPT-5.6-Terra | 29.6 | 15.1 | 99.1 | 22.5 | 10.7 | **90.0** | 69.2 | 38.5 | 82.5 | 46.1 | 33.5 | 98.7 |
| Gemini-3.1-Pro | 34.3 | 17.7 | **99.9** | 18.6 | 5.6 | 74.3 | **71.4** | 46.9 | 86.2 | 41.5 | 29.3 | **98.8** |
| Qwen-3.7-Max | 36.1 | 18.9 | 98.6 | 41.6 | 23.8 | 57.5 | 59.0 | 49.1 | 92.8 | 32.4 | 24.6 | 98.5 |
| Qwen-3.8-Max | **42.3** | **25.0** | 94.7 | **46.0** | **26.5** | 75.8 | 67.6 | **57.0** | 87.6 | 40.8 | 27.1 | 88.7 |

**By language resource level**

| Model | High<br>Pass^1 | <br>Pass^3 | <br>LC | Medium<br>Pass^1 | <br>Pass^3 | <br>LC | Low<br>Pass^1 | <br>Pass^3 | <br>LC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude-Opus-4.8 | **51.3** | 34.3 | 90.4 | **48.1** | **33.9** | 87.2 | **44.8** | **29.6** | 86.7 |
| GPT-5.6-Terra | 45.3 | 26.3 | **98.8** | 43.9 | 25.1 | **90.9** | 36.8 | 21.9 | **89.6** |
| Gemini-3.1-Pro | 45.9 | 27.4 | 98.6 | 42.4 | 25.8 | 87.5 | 36.4 | 21.0 | 83.8 |
| Qwen-3.7-Max | 45.8 | 32.4 | 89.0 | 42.9 | 29.5 | 86.9 | 40.1 | 27.6 | 84.9 |
| Qwen-3.8-Max | 51.2 | **34.3** | 94.5 | 48.0 | 33.6 | 84.5 | 44.7 | 29.4 | 81.7 |

No model leads every family, and all five score lower on Pass^1, Pass^3 and LC
in low-resource languages than in high-resource ones. See the paper for the
failure, token-cost and language-switching analyses.

## 🛠️ Data

Download the BabelArena dataset from
[Hugging Face](https://huggingface.co/datasets/Qwen/BabelArena) or
[ModelScope](https://modelscope.cn/datasets/Qwen/BabelArena).

The repository carries the code and the frozen `standard` task lists; the task
data (~14 GB) is fetched separately:

```
data/
  tau3/             tau2/domains/              per-language tasks, policies, databases
  vitabench/        vita/domains/              per-language tasks and environments
  deepplanning/     travelplanning/database/   per-case, per-language databases
                    shoppingplanning/database_level*/
  */task_subsets/standard/                     the frozen task lists (in git)
benchmarks/claw/
  tasks/            per-task prompts, fixtures and graders, one file per language
  task_subsets/standard/                       (in git)
```

`standard` is the frozen task set, with the same task IDs in every language:
699 tasks, 167 of them from ClawEval. Each language variant lives next to its
source as a language-suffixed file (for example `task_ja.yaml`, `tasks_ja.json`,
`database_ja/`), and `./bench languages` prints how each benchmark spells each
language.

ClawEval's data ships as three archives, one per split --
`claw_general.tar.gz`, `claw_multimodal.tar.gz` and `claw_multi_turn.tar.gz`
(1.26 GB, videos included). Unpack them into one directory and install it with
`./bench fetch-data --source <directory>`, or unpack them straight into
`benchmarks/`.

The image and video assets in this dataset come from the ClawEval dataset
(https://huggingface.co/datasets/claw-eval/Claw-Eval), whose tasks are adapted
from the community-contributed OpenClaw, PinchBench, OfficeQA, OneMillion-Bench,
Finance Agent and Terminal-Bench 2.0.

## 🧪 Evaluation

### Environment

You need Python 3.12 and Python 3.10 (or 3.11) on `PATH` -- the four benchmarks
cannot share an interpreter -- Docker for ClawEval's tool sandbox, and PyYAML.

```bash
git clone https://code.alibaba-inc.com/alitranx/BabelArena.git
cd BabelArena
pip install pyyaml
./bench setup                                   # one virtualenv per benchmark + sandbox image
./bench fetch-data --source /path/to/BabelArena-data
```

### Models

```bash
cp configs/models.yaml.example configs/models.yaml
export REQUEST_BASE_URL="https://your-endpoint/v1/chat/completions"   # the full endpoint
export REQUEST_API_KEY="..."
./bench check                                   # data, environments, config; no API calls
```

`configs/models.yaml` lists the agents you evaluate and the support models, which
are part of the measuring instrument. Keep them fixed to compare with the paper:

| Role | Used by | Paper setting |
|---|---|---|
| agent under test | all | medium reasoning effort and temperature 0, where the endpoint accepts them |
| `user` (simulated user) | VitaBench, τ³-Bench, ClawEval multi-turn | Gemini-3.5-Flash, thinking off |
| `evaluator` (LLM judge) | VitaBench, τ³-Bench, ClawEval | GPT-5.6-Sol, thinking off |
| `conversion` | DeepPlanning (free-text plan → structured format) | Gemini-3.5-Flash, thinking off |
| `lang_judge` | language consistency | Gemini-3.7-Flash |

DeepPlanning is scored by deterministic rules and needs no judge.

ClawEval's web-search tasks call a real search API: export `SERP_DEV_KEY` as
well (see [docs/RUNNING.md](docs/RUNNING.md#claw)). Without it they still run,
but every search comes back empty.

### Run

```bash
# smoke test: one task per unit, one trial, one language
./bench run -b all -l en --agent-model <model> --num-tasks 1 --num-trials 1

# the paper's protocol: standard subset, all 23 languages, 3 trials
./bench run -b all -l all --agent-model <model>
```

`-b` takes `tau3`, `vitabench`, `deepplanning`, `claw` or `all`; `-l` takes a
language code, a comma-separated list or `all`. Re-running with the same
`--run-id` resumes an interrupted run. Add `--dry-run` to print every command
without running it.

### Score

```bash
./bench report --run-id <id>        # each benchmark's own metric, then Pass^1 / Pass^3
./bench lang-check --run-id <id>    # language consistency (one judge call per trajectory)
```

Results are written under `results/<run_id>/`. Pass^k follows
`C(s, k) / C(n, k)` averaged over tasks, for *s* successful trials out of *n*,
where a trial succeeds on its benchmark's own full-success criterion.

For every flag, per-benchmark details, credentials handling and first-run
pitfalls, see **[docs/RUNNING.md](docs/RUNNING.md)**.

## Acknowledgements

BabelArena is built on four agent benchmarks; please also cite them when you
use it: [VitaBench](https://github.com/meituan-longcat/vitabench),
[DeepPlanning](https://huggingface.co/datasets/Qwen/DeepPlanning),
[τ-bench / τ²-bench / τ-knowledge](https://github.com/sierra-research/tau2-bench)
and [Claw-Eval](https://claw-eval.github.io). τ³-bench's task fixes come from
SABER, and Claw-Eval adapts tasks from OpenClaw, PinchBench, OfficeQA,
OneMillion-Bench, Finance Agent and Terminal-Bench 2.0. [NOTICE](NOTICE) lists
the attribution and every change made to them in this repository.

## 📄 Citation

If you use **BabelArena** in your research or find our work useful, please cite
us:

```bibtex
@article{babelarena2026,
  title={BabelArena: A Large-Scale Multilingual Benchmark for LLM Agents},
  author={Peng Kuang and Yuchun Fan and Jiangnan Li and Minghao Wu and Jialong Tang and Haoran Wei and Weixuan Wang and Jianhong Tu and Baosong Yang and Tong Xiao},
  journal={arXiv preprint arXiv:2609.23490},
  year={2026},
  url={https://arxiv.org/abs/2609.23490}
}
```

<details>
<summary>Source benchmarks</summary>

```bibtex
@article{he2025vitabench,
  title={VitaBench: Benchmarking LLM Agents with Versatile Interactive Tasks in Real-world Applications},
  author={Wei He and Yueqing Sun and Hongyan Hao and Xueyuan Hao and Zhikang Xia and Qi Gu and Chengcheng Han and Dengchang Zhao and Hui Su and Kefeng Zhang and Man Gao and Xi Su and Xiaodong Cai and Xunliang Cai and Yu Yang and Yunke Zhao},
  journal={arXiv preprint arXiv:2509.26490},
  year={2025}
}

@inproceedings{zhang2026deepplanning,
  title={DeepPlanning: Benchmarking Long-Horizon Agentic Planning with Verifiable Constraints},
  author={Yinger Zhang and Shutong Jiang and Renhao Li and Jianhong Tu and Yang Su and Lianghao Deng and Xudong Guo and Chenxu Lv and Junyang Lin},
  booktitle={Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={7377--7407},
  year={2026}
}

@article{yao2024taubench,
  title={$\tau$-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains},
  author={Shunyu Yao and Noah Shinn and Pedram Razavi and Karthik Narasimhan},
  journal={arXiv preprint arXiv:2406.12045},
  year={2024}
}

@article{barres2025tau2bench,
  title={$\tau^2$-bench: Evaluating Conversational Agents in a Dual-Control Environment},
  author={Victor Barres and Honghua Dong and Soham Ray and Xujie Si and Karthik Narasimhan},
  journal={arXiv preprint arXiv:2506.07982},
  year={2025}
}

@article{shi2026tauknowledge,
  title={$\tau$-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge},
  author={Quan Shi and Alexandra Zytek and Pedram Razavi and Karthik Narasimhan and Victor Barres},
  journal={arXiv preprint arXiv:2603.04370},
  year={2026}
}

@article{ray2026tauvoice,
  title={$\tau$-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains},
  author={Soham Ray and Keshav Dhandhania and Victor Barres and Karthik Narasimhan},
  journal={arXiv preprint arXiv:2603.13686},
  year={2026}
}

@inproceedings{cuadron2026saber,
  title={{SABER}: Small Actions, Big Errors {\textemdash} Safeguarding Mutating Steps in {LLM} Agents},
  author={Alejandro Cuadron and Pengfei Yu and Yang Liu and Arpit Gupta},
  booktitle={ICLR 2026 Workshop on Memory for LLM-Based Agentic Systems},
  year={2026},
  url={https://openreview.net/forum?id=En2z9dckgP}
}

@article{ye2026claweval,
  title={Claw-Eval: Toward Trustworthy Evaluation of Autonomous Agents},
  author={Bowen Ye and Rang Li and Qibin Yang and Yuanxin Liu and Linli Yao and Hanglong Lv and Zhihui Xie and Chenxin An and Lei Li and Lingpeng Kong and Qi Liu and Zhifang Sui and Tong Yang},
  journal={arXiv preprint arXiv:2604.06132},
  year={2026}
}
```

</details>
