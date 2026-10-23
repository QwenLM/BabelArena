"""Single place that resolves where the seed benchmark data lives.

By default the databases sit inside this source tree, exactly as upstream ships
them (``travelplanning/database/``, ``shoppingplanning/database_level<N>``).
Setting ``DEEPPLANNING_DATA_DIR`` relocates that bulk elsewhere while keeping
the same internal layout, which is how the surrounding suite shares one
top-level ``data/`` directory across three benchmarks. Mirrors tau3's
``TAU2_DATA_DIR`` and vitabench's ``VITA_DATA_DIR``.

Only *seed* data is affected. The per-run working copy that
``prepare_database.py`` stages into ``shoppingplanning/database/`` stays inside
the source tree, because it is run output rather than distributed data.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

_ENV = os.getenv("DEEPPLANNING_DATA_DIR")
DATA_ROOT = Path(_ENV).expanduser().resolve() if _ENV else REPO_ROOT


def travel_database_dir(db_code: str) -> Path:
    """Seed travel DB for a language code, e.g. database/database_ja."""
    return DATA_ROOT / "travelplanning" / "database" / f"database_{db_code}"


def shopping_seed_dir(level: int | str, db_code: str) -> Path:
    """Seed shopping DB for a level and language code.

    English is the baseline and carries no suffix (``database_level1``); every
    other language is ``database_level<N>_<code>``.
    """
    name = f"database_level{level}" if db_code == "en" else f"database_level{level}_{db_code}"
    return DATA_ROOT / "shoppingplanning" / name


def task_subsets_dir() -> Path:
    return DATA_ROOT / "task_subsets"
