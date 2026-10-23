"""Language-aware tokenization for BM25 indexing and retrieval.

Whitespace-delimited languages use str.split(); languages without word
boundaries (CJK, Thai, Lao, Khmer, Burmese) use Qwen3's BPE tokenizer
to produce subword tokens suitable for BM25 scoring.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable, List, Optional

from loguru import logger

NON_WHITESPACE_LANGUAGES = frozenset(
    {
        "chinese",
        "japanese",
        "korean",
        "thai",
        "lao",
        "khmer",
        "burmese",
    }
)

QWEN_TOKENIZER_MODEL = "Qwen/Qwen3-0.6B"
QWEN_TOKENIZER_REVISION = "c1899de289a04d12100db370d81485cdf75e47ca"
TOKENIZER_PATH_ENV_VAR = "TAU2_BM25_TOKENIZER_PATH"
TOKENIZER_CACHE_ENV_VAR = "TAU2_BM25_TOKENIZER_CACHE"
TOKENIZER_OFFLINE_ENV_VAR = "TAU2_BM25_TOKENIZER_OFFLINE"

_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
_FALSE_VALUES = frozenset({"0", "false", "no", "off"})

_qwen_tokenizer = None


def _offline_mode_enabled() -> bool:
    value = os.getenv(TOKENIZER_OFFLINE_ENV_VAR)
    if value is None:
        return False
    normalized = value.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False
    raise ValueError(
        f"{TOKENIZER_OFFLINE_ENV_VAR} must be one of "
        f"{sorted(_TRUE_VALUES | _FALSE_VALUES)}, got {value!r}"
    )


def _get_tokenizer_source() -> tuple[str, Optional[str]]:
    local_path = os.getenv(TOKENIZER_PATH_ENV_VAR)
    if local_path:
        path = Path(local_path).expanduser()
        if not path.exists():
            raise FileNotFoundError(
                f"BM25 tokenizer path does not exist: {path}. "
                f"Unset {TOKENIZER_PATH_ENV_VAR} to use the pinned Hugging Face "
                "tokenizer, or point it to a downloaded tokenizer directory."
            )
        return str(path), None
    return QWEN_TOKENIZER_MODEL, QWEN_TOKENIZER_REVISION


def _load_from_pretrained(*, local_files_only: bool) -> Any:
    try:
        from transformers import AutoTokenizer
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Multilingual BM25 tokenization requires the knowledge extra. "
            "Install it with `uv sync --extra knowledge`."
        ) from exc

    source, revision = _get_tokenizer_source()
    kwargs: dict[str, Any] = {"local_files_only": local_files_only}
    cache_dir = os.getenv(TOKENIZER_CACHE_ENV_VAR)
    if cache_dir:
        kwargs["cache_dir"] = cache_dir
    if revision is not None:
        kwargs["revision"] = revision
    return AutoTokenizer.from_pretrained(source, **kwargs)


def _offline_remediation_message() -> str:
    return (
        "The pinned BM25 tokenizer is not available locally. Run "
        "`tau2 knowledge prefetch-tokenizer` once with network access, set "
        f"{TOKENIZER_PATH_ENV_VAR} to a local tokenizer directory, or unset "
        f"{TOKENIZER_OFFLINE_ENV_VAR} to permit the pinned download."
    )


def _load_qwen_tokenizer() -> Any:
    global _qwen_tokenizer
    if _qwen_tokenizer is None:
        try:
            _qwen_tokenizer = _load_from_pretrained(local_files_only=True)
        except FileNotFoundError:
            raise
        except OSError as exc:
            if _offline_mode_enabled():
                raise RuntimeError(_offline_remediation_message()) from exc
            logger.warning(
                "BM25 tokenizer artifacts are not cached; downloading pinned "
                "tokenizer {} at revision {}. This one-time setup can be run "
                "in advance with `tau2 knowledge prefetch-tokenizer`.",
                QWEN_TOKENIZER_MODEL,
                QWEN_TOKENIZER_REVISION,
            )
            try:
                _qwen_tokenizer = _load_from_pretrained(local_files_only=False)
            except OSError as download_exc:
                raise RuntimeError(
                    "Failed to download the pinned BM25 tokenizer. "
                    + _offline_remediation_message()
                ) from download_exc
    return _qwen_tokenizer


def prefetch_bm25_tokenizer() -> tuple[str, Optional[str]]:
    """Download or validate the configured multilingual BM25 tokenizer.

    Returns:
        The tokenizer source and immutable revision. The revision is ``None``
        when a local tokenizer directory is configured.
    """
    global _qwen_tokenizer
    if _offline_mode_enabled():
        raise RuntimeError(
            f"Cannot prefetch while {TOKENIZER_OFFLINE_ENV_VAR} is enabled. "
            "Unset it and retry with network access."
        )
    source, revision = _get_tokenizer_source()
    logger.info(
        "Prefetching multilingual BM25 tokenizer from {}{}...",
        source,
        f" at revision {revision}" if revision else "",
    )
    try:
        _qwen_tokenizer = _load_from_pretrained(local_files_only=False)
    except FileNotFoundError:
        raise
    except OSError as exc:
        raise RuntimeError(
            f"Failed to prefetch the BM25 tokenizer from {source!r}. "
            "Check Hugging Face connectivity, HF_ENDPOINT, and cache permissions."
        ) from exc
    return source, revision


def _whitespace_tokenize(text: str) -> List[str]:
    return text.lower().split()


def _qwen_tokenize(text: str) -> List[str]:
    tokenizer = _load_qwen_tokenizer()
    token_ids = tokenizer.encode(text, add_special_tokens=False)
    tokens = [tokenizer.decode([tid]).strip().lower() for tid in token_ids]
    return [t for t in tokens if t]


def _needs_subword_tokenizer(language: Optional[str]) -> bool:
    if not language:
        return False
    return language.strip().lower() in NON_WHITESPACE_LANGUAGES


def get_tokenize_fn(language: Optional[str] = None) -> Callable[[str], List[str]]:
    if _needs_subword_tokenizer(language):
        return _qwen_tokenize
    return _whitespace_tokenize
