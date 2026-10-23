import os
from pathlib import Path
from typing import Optional

from tau2.utils.utils import DATA_DIR

RETAIL_DATA_DIR = DATA_DIR / "tau2" / "domains" / "retail"
RETAIL_DB_PATH = RETAIL_DATA_DIR / "db.json"
RETAIL_POLICY_PATH = RETAIL_DATA_DIR / "policy.md"
RETAIL_TASK_SET_PATH = RETAIL_DATA_DIR / "tasks.json"

# Language for translated policy and tasks. Mirrors the convention used by
# banking_knowledge and user_simulator: if TAU2_LANGUAGE is set, prefer the
# matching translated files; otherwise fall back to English.
LANGUAGE = os.getenv("TAU2_LANGUAGE", "").strip()


def get_policy_path(language: Optional[str] = None) -> Path:
    """Return the policy path for a language.

    For non-English languages, requires the translated file to exist; raises
    FileNotFoundError otherwise. English (or unset) returns the source path.
    """
    lang = (language or LANGUAGE or "").strip()
    if lang and lang.lower() != "english":
        translated = RETAIL_DATA_DIR / f"policy_{lang}.md"
        if not (translated.exists() and translated.stat().st_size > 0):
            raise FileNotFoundError(
                f"Translated retail policy missing for language {lang!r}: "
                f"{translated}. Re-fetch the task data (`./bench fetch-data`)."
            )
        return translated
    return RETAIL_POLICY_PATH


def get_tasks_path(language: Optional[str] = None) -> Path:
    """Return the tasks.json path for a language.

    For non-English languages, requires the translated file to exist; raises
    FileNotFoundError otherwise. English (or unset) returns the source path.
    """
    lang = (language or LANGUAGE or "").strip()
    if lang and lang.lower() != "english":
        translated = RETAIL_DATA_DIR / f"tasks_{lang}.json"
        if not (translated.exists() and translated.stat().st_size > 0):
            raise FileNotFoundError(
                f"Translated retail tasks missing for language {lang!r}: "
                f"{translated}. Re-fetch the task data (`./bench fetch-data`)."
            )
        return translated
    return RETAIL_TASK_SET_PATH


def get_db_path(language: str = LANGUAGE) -> Path:
    """Resolve the DB path for ``language``.

    English (or empty) returns the canonical English DB. Any other language
    requires ``db_<Lang>.json`` to exist and be non-empty; raises
    FileNotFoundError otherwise (no silent fallback).
    """
    if not language or language == "English":
        return RETAIL_DB_PATH
    candidate = RETAIL_DB_PATH.with_name(f"db_{language}.json")
    if not candidate.exists() or candidate.stat().st_size == 0:
        raise FileNotFoundError(
            f"Translated DB missing or empty for language={language!r}: {candidate}"
        )
    return candidate
