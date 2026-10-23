"""Pinned, offline-safe configuration for ShoppingPlanning BM25 tokenization."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_TOKENIZER_MODEL = "Qwen/Qwen3-8B"
DEFAULT_TOKENIZER_REVISION = "21073ac5a57f8ac6b159dae129728af51ac707e8"
TOKENIZER_MODEL_ENV = "SHOPPING_BM25_TOKENIZER"
TOKENIZER_REVISION_ENV = "SHOPPING_BM25_TOKENIZER_REVISION"
TOKENIZER_CACHE_ENV = "SHOPPING_BM25_TOKENIZER_CACHE_DIR"


@dataclass(frozen=True)
class TokenizerSettings:
    model: str
    revision: str
    cache_dir: Path
    manifest_path: Path


def _default_hf_cache() -> Path:
    try:
        from huggingface_hub.constants import HF_HUB_CACHE
    except ImportError as exc:
        raise RuntimeError(
            "huggingface-hub is required for ShoppingPlanning tokenizer setup; "
            "install the repository requirements first"
        ) from exc
    return Path(HF_HUB_CACHE).expanduser()


def resolve_tokenizer_settings(
    model: str | None = None,
    revision: str | None = None,
    cache_dir: str | Path | None = None,
) -> TokenizerSettings:
    """Resolve independent repository, revision, and cache settings."""
    resolved_model = model or os.environ.get(TOKENIZER_MODEL_ENV, DEFAULT_TOKENIZER_MODEL)
    resolved_revision = revision or os.environ.get(
        TOKENIZER_REVISION_ENV, DEFAULT_TOKENIZER_REVISION
    )
    configured_cache = cache_dir or os.environ.get(TOKENIZER_CACHE_ENV)
    resolved_cache = (
        Path(configured_cache).expanduser() if configured_cache else _default_hf_cache()
    )
    if not resolved_model.strip():
        raise ValueError("Shopping tokenizer model must not be empty")
    if not resolved_revision.strip():
        raise ValueError("Shopping tokenizer revision must not be empty")
    fingerprint = hashlib.sha256(
        f"{resolved_model}@{resolved_revision}".encode("utf-8")
    ).hexdigest()[:16]
    manifest = resolved_cache / f"deepplanning-shopping-tokenizer-{fingerprint}.json"
    return TokenizerSettings(
        model=resolved_model,
        revision=resolved_revision,
        cache_dir=resolved_cache,
        manifest_path=manifest,
    )


def load_prepared_manifest(settings: TokenizerSettings) -> dict[str, Any]:
    """Load and validate the manifest written by the explicit setup command."""
    try:
        payload = json.loads(settings.manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Shopping BM25 tokenizer is not prepared. Run: "
            f"python scripts/prepare_shopping_tokenizer.py --model {settings.model} "
            f"--revision {settings.revision} --cache-dir {settings.cache_dir}"
        ) from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"Shopping tokenizer manifest is unreadable or invalid: "
            f"{settings.manifest_path}: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"Shopping tokenizer manifest must be an object: {settings.manifest_path}")
    if payload.get("model") != settings.model or payload.get("revision") != settings.revision:
        raise RuntimeError(
            f"Shopping tokenizer manifest does not match requested model/revision: "
            f"{settings.manifest_path}"
        )
    if payload.get("validated_offline") is not True:
        raise RuntimeError(
            f"Shopping tokenizer manifest has no successful offline validation: "
            f"{settings.manifest_path}"
        )
    return payload


def _load_auto_tokenizer(settings: TokenizerSettings, *, local_files_only: bool):
    try:
        from transformers import AutoTokenizer
    except ImportError as exc:
        raise RuntimeError(
            "transformers is required for non-whitespace ShoppingPlanning languages; "
            "install the repository requirements first"
        ) from exc
    return AutoTokenizer.from_pretrained(
        settings.model,
        revision=settings.revision,
        cache_dir=str(settings.cache_dir),
        local_files_only=local_files_only,
    )


def validate_prepared_tokenizer(settings: TokenizerSettings):
    """Validate setup metadata and perform an offline tokenizer load and encode."""
    load_prepared_manifest(settings)
    try:
        tokenizer = _load_auto_tokenizer(settings, local_files_only=True)
        tokens = tokenizer.encode("DeepPlanning tokenizer preflight", add_special_tokens=False)
    except Exception as exc:
        raise RuntimeError(
            f"Prepared Shopping tokenizer is missing or incomplete for "
            f"{settings.model}@{settings.revision} in {settings.cache_dir}. "
            "Rerun scripts/prepare_shopping_tokenizer.py. "
            f"Offline validation error: {exc}"
        ) from exc
    if not tokens:
        raise RuntimeError("Prepared Shopping tokenizer returned no preflight tokens")
    return tokenizer


def prepare_tokenizer(settings: TokenizerSettings, *, force: bool = False):
    """Download once, verify offline use, and atomically record setup metadata."""
    settings.cache_dir.mkdir(parents=True, exist_ok=True)
    if not force and settings.manifest_path.is_file():
        try:
            tokenizer = validate_prepared_tokenizer(settings)
            return tokenizer, False
        except RuntimeError:
            pass

    try:
        _load_auto_tokenizer(settings, local_files_only=False)
        tokenizer = _load_auto_tokenizer(settings, local_files_only=True)
        tokens = tokenizer.encode("DeepPlanning tokenizer preflight", add_special_tokens=False)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to prepare Shopping tokenizer {settings.model}@{settings.revision}: {exc}"
        ) from exc
    if not tokens:
        raise RuntimeError("Downloaded Shopping tokenizer returned no validation tokens")

    try:
        import huggingface_hub
        import tokenizers
        import transformers
    except ImportError as exc:
        raise RuntimeError(f"Tokenizer runtime dependency is missing: {exc}") from exc

    payload = {
        "model": settings.model,
        "revision": settings.revision,
        "cache_dir": str(settings.cache_dir.resolve()),
        "validated_offline": True,
        "prepared_at": datetime.now(timezone.utc).isoformat(),
        "tokenizer_class": type(tokenizer).__name__,
        "versions": {
            "transformers": transformers.__version__,
            "tokenizers": tokenizers.__version__,
            "huggingface_hub": huggingface_hub.__version__,
        },
    }
    temporary_manifest = settings.manifest_path.with_suffix(".tmp")
    temporary_manifest.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    temporary_manifest.replace(settings.manifest_path)
    # Re-read the completed manifest and prove the recorded artifact still
    # loads offline before reporting setup success.
    tokenizer = validate_prepared_tokenizer(settings)
    return tokenizer, True
