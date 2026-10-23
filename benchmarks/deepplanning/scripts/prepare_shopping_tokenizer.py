#!/usr/bin/env python3
"""Download and validate the pinned ShoppingPlanning BM25 tokenizer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
_SHOPPING_ROOT = _REPO_ROOT / "shoppingplanning"
if str(_SHOPPING_ROOT) not in sys.path:
    sys.path.insert(0, str(_SHOPPING_ROOT))

from tokenizer_config import (  # noqa: E402
    DEFAULT_TOKENIZER_MODEL,
    DEFAULT_TOKENIZER_REVISION,
    prepare_tokenizer,
    resolve_tokenizer_settings,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        default=None,
        help=(
            "Tokenizer repository (default: $SHOPPING_BM25_TOKENIZER or "
            f"{DEFAULT_TOKENIZER_MODEL})"
        ),
    )
    parser.add_argument(
        "--revision",
        default=None,
        help=(
            "Immutable repository revision (default: "
            "$SHOPPING_BM25_TOKENIZER_REVISION or "
            f"{DEFAULT_TOKENIZER_REVISION})"
        ),
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Caller-owned Hugging Face cache directory",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Repeat preparation and validation even when the manifest is valid",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings = resolve_tokenizer_settings(args.model, args.revision, args.cache_dir)
    print("Preparing ShoppingPlanning tokenizer")
    print(f"  Model:    {settings.model}")
    print(f"  Revision: {settings.revision}")
    print(f"  Cache:    {settings.cache_dir}")
    try:
        tokenizer, changed = prepare_tokenizer(settings, force=args.force)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    action = "downloaded and validated" if changed else "already prepared and valid"
    print(f"Tokenizer {action}: {type(tokenizer).__name__}")
    print(f"Manifest: {settings.manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
