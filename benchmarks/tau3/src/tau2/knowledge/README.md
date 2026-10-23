# Knowledge Retrieval

Domains with a knowledge base (currently just `banking_knowledge`) use a `--retrieval-config` flag that controls how the agent accesses the knowledge base.

```bash
tau2 run --domain banking_knowledge --retrieval-config <config_name> --agent-llm gpt-4.1 --user-llm gpt-4.1
```

If `--retrieval-config` is omitted, the default is `bm25` (local computation, no API keys needed). A warning is printed to remind you to choose a config explicitly. For Chinese, Japanese, Korean, Thai, Lao, Khmer, and Burmese, the first BM25 run needs the pinned tokenizer artifacts described below.

## Retrieval Configs

| Config | Tools | Requirements |
|--------|-------|--------------|
| `no_knowledge` | None | None (offline) |
| `full_kb` | None | None (offline) |
| `golden_retrieval` | None | None (offline) |
| `grep_only` | `grep` | None (offline) |
| `bm25` | `KB_search` | Local tokenizer; one-time download for non-whitespace languages |
| `openai_embeddings` | `KB_search` | `OPENAI_API_KEY` |
| `qwen_embeddings` | `KB_search` | `OPENROUTER_API_KEY` |
| `terminal_use` | `shell` | `sandbox-runtime` (see below) |
| `terminal_use_write` | `shell` | `sandbox-runtime` (see below) |

The `bm25`, `openai_embeddings`, and `qwen_embeddings` configs can also be combined with:
- `_reranker` suffix — adds an LLM reranker postprocessor (requires `OPENAI_API_KEY`)
- `_grep` suffix — adds a `grep` tool
- Both (e.g. `openai_embeddings_reranker_grep`)

Note: `*_reranker` variants always require `OPENAI_API_KEY` for the pointwise LLM reranker, even when the base embedder uses a different provider (e.g. `qwen_embeddings_reranker` needs both `OPENROUTER_API_KEY` and `OPENAI_API_KEY`).

## Multilingual BM25 Tokenizer

English and other whitespace-delimited languages use a built-in whitespace tokenizer. Chinese, Japanese, Korean, Thai, Lao, Khmer, and Burmese use the tokenizer from `Qwen/Qwen3-0.6B`, pinned to the immutable revision `c1899de289a04d12100db370d81485cdf75e47ca`.

Prefetch it once before starting a multilingual batch:

```bash
uv sync --extra knowledge
uv run tau2 knowledge prefetch-tokenizer
```

The tokenizer runs locally after download; no model weights or inference service are used. Hugging Face's shared cache and file locking make the prefetch safe across processes, but prefetching once avoids making parallel language workers wait on the same download.

Setup can be customized with these environment variables:

- `TAU2_BM25_TOKENIZER_CACHE`: tokenizer cache directory.
- `TAU2_BM25_TOKENIZER_PATH`: an already-downloaded local tokenizer directory. This overrides the Hugging Face source.
- `TAU2_BM25_TOKENIZER_OFFLINE=1`: prohibit downloads and fail immediately with setup instructions if the tokenizer is unavailable locally.
- `HF_ENDPOINT`: Hugging Face endpoint mirror used during prefetch/download.

At runtime, tau2 checks the local cache first. If artifacts are missing and strict offline mode is not enabled, it prints a warning before starting the pinned download. For reproducible offline batches, run the prefetch command during setup and enable `TAU2_BM25_TOKENIZER_OFFLINE=1` during evaluation.

## Embedding Cache

Embedding-based configs (`openai_embeddings*`, `qwen_embeddings*`) cache document embeddings on disk at `data/.embeddings_cache` (gitignored). This avoids re-computing embeddings on repeated runs. The cache is automatically invalidated when document content changes.

## Additional Setup

### OpenRouter API Key

The `qwen_embeddings*` configs route through [OpenRouter](https://openrouter.ai/). Set the `OPENROUTER_API_KEY` environment variable (or add it to your `.env` file — see `.env.example`).

### sandbox-runtime

The `terminal_use` and `terminal_use_write` configs require [Anthropic's sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime) for secure filesystem isolation:

```bash
npm install -g @anthropic-ai/sandbox-runtime@0.0.23
```

**macOS**: Also requires `ripgrep`:
```bash
brew install ripgrep
```

**Linux**: Also requires `ripgrep`, `bubblewrap`, and `socat`:
```bash
# Ubuntu/Debian
sudo apt-get install ripgrep bubblewrap socat
```
