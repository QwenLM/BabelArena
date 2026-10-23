import os
from pathlib import Path
from typing import Optional

from tau2.utils.utils import DATA_DIR

LANGUAGE = os.getenv("TAU2_LANGUAGE", "").strip()

AIRLINE_DATA_DIR = DATA_DIR / "tau2" / "domains" / "airline"
AIRLINE_DB_PATH = AIRLINE_DATA_DIR / "db.json"
AIRLINE_POLICY_PATH = AIRLINE_DATA_DIR / "policy.md"
AIRLINE_TASK_SET_PATH = AIRLINE_DATA_DIR / "tasks.json"


def get_localized_paths(lang: str) -> dict[str, Path]:
    """Return paths for a deeply localized environment."""
    loc_dir = AIRLINE_DATA_DIR / "localization" / "generated" / lang
    return {
        "policy": loc_dir / "policy.md",
        "tools": loc_dir / "tools.py",
        "db": loc_dir / "db.json",
        "tasks": loc_dir / "tasks.json",
        "manifest": loc_dir / "manifest.json",
    }


def get_db_path(language: str = LANGUAGE) -> Path:
    """Language-aware airline DB path.

    English / empty returns AIRLINE_DB_PATH. Other languages require
    db_<Lang>.json adjacent. Raises FileNotFoundError otherwise.
    """
    if not language or language == "English":
        return AIRLINE_DB_PATH
    candidate = AIRLINE_DB_PATH.with_name(f"db_{language}.json")
    if not candidate.exists() or candidate.stat().st_size == 0:
        raise FileNotFoundError(f"Translated airline DB missing or empty: {candidate}")
    return candidate


def _resolve_translated(path: Path, language: Optional[str]) -> Path:
    lang = (language or LANGUAGE or "").strip()
    if not lang or lang.lower() == "english":
        return path
    translated = path.with_name(f"{path.stem}_{lang}{path.suffix}")
    if not translated.exists() or translated.stat().st_size == 0:
        raise FileNotFoundError(
            f"Translated airline file missing for language {lang!r}: {translated}. "
            "Re-fetch the task data (`./bench fetch-data`)."
        )
    return translated


def get_policy_path(language: Optional[str] = None) -> Path:
    """Return English or language-suffixed airline policy path."""
    return _resolve_translated(AIRLINE_POLICY_PATH, language)


def get_tasks_path(language: Optional[str] = None) -> Path:
    """Return English or language-suffixed airline tasks path."""
    return _resolve_translated(AIRLINE_TASK_SET_PATH, language)
