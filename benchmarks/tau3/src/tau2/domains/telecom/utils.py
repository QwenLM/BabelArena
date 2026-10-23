import os
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from tau2.utils.utils import DATA_DIR

TELECOM_DATA_DIR = DATA_DIR / "tau2" / "domains" / "telecom"
TELECOM_DB_PATH = TELECOM_DATA_DIR / "db.toml"
TELECOM_USER_DB_PATH = TELECOM_DATA_DIR / "user_db.toml"
TELECOM_MAIN_POLICY_PATH = TELECOM_DATA_DIR / "main_policy.md"
TELECOM_TECH_SUPPORT_POLICY_MANUAL_PATH = TELECOM_DATA_DIR / "tech_support_manual.md"
TELECOM_TECH_SUPPORT_POLICY_WORKFLOW_PATH = (
    TELECOM_DATA_DIR / "tech_support_workflow.md"
)
TELECOM_MAIN_POLICY_SOLO_PATH = TELECOM_DATA_DIR / "main_policy_solo.md"
TELECOM_TECH_SUPPORT_POLICY_MANUAL_SOLO_PATH = (
    TELECOM_DATA_DIR / "tech_support_manual.md"
)
TELECOM_TECH_SUPPORT_POLICY_WORKFLOW_SOLO_PATH = (
    TELECOM_DATA_DIR / "tech_support_workflow_solo.md"
)
# TELECOM_TASK_SET_PATH_FULL = TELECOM_DATA_DIR / "tasks_full.json" # Not used anymore. Use full task split instead
# TELECOM_TASK_SET_PATH_SMALL = TELECOM_DATA_DIR / "tasks_small.json" # Not used anymore. Use small task split instead
TELECOM_TASK_SET_PATH = TELECOM_DATA_DIR / "tasks.json"


# Language for translated policy and tasks. Mirrors the convention used by
# banking_knowledge, retail, and user_simulator: if TAU2_LANGUAGE is set,
# prefer the matching translated files; otherwise fall back to English.
LANGUAGE = os.getenv("TAU2_LANGUAGE", "").strip()


def _resolve_translated(path: Path, language: Optional[str]) -> Path:
    """Return the language-suffixed sibling of *path* for non-English languages.

    For non-English languages, the translated file MUST exist; raises
    FileNotFoundError otherwise (no silent fallback to English — that
    would produce mixed-language eval runs whose rewards are untrustworthy).

    Example: ``main_policy.md`` + ``"Arabic"`` -> ``main_policy_Arabic.md``.
    """
    lang = (language or LANGUAGE or "").strip()
    if not lang or lang.lower() == "english":
        return path
    translated = path.with_name(f"{path.stem}_{lang}{path.suffix}")
    if not (translated.exists() and translated.stat().st_size > 0):
        raise FileNotFoundError(
            f"Translated telecom file missing for language {lang!r}: "
            f"{translated}. Re-fetch the task data (`./bench fetch-data`)."
        )
    return translated


def get_main_policy_path(
    solo_mode: bool = False, language: Optional[str] = None
) -> Path:
    base = TELECOM_MAIN_POLICY_SOLO_PATH if solo_mode else TELECOM_MAIN_POLICY_PATH
    return _resolve_translated(base, language)


def get_tech_support_manual_path(
    solo_mode: bool = False, language: Optional[str] = None
) -> Path:
    base = (
        TELECOM_TECH_SUPPORT_POLICY_MANUAL_SOLO_PATH
        if solo_mode
        else TELECOM_TECH_SUPPORT_POLICY_MANUAL_PATH
    )
    return _resolve_translated(base, language)


def get_tech_support_workflow_path(
    solo_mode: bool = False, language: Optional[str] = None
) -> Path:
    base = (
        TELECOM_TECH_SUPPORT_POLICY_WORKFLOW_SOLO_PATH
        if solo_mode
        else TELECOM_TECH_SUPPORT_POLICY_WORKFLOW_PATH
    )
    return _resolve_translated(base, language)


def get_tasks_path(language: Optional[str] = None) -> Path:
    return _resolve_translated(TELECOM_TASK_SET_PATH, language)


def get_now() -> datetime:
    # assume now is 2025-02-25 12:08:00
    return datetime(2025, 2, 25, 12, 8, 0)


def get_today() -> date:
    # assume today is 2025-02-25
    return date(2025, 2, 25)


def get_db_path(language: str = LANGUAGE) -> Path:
    if not language or language == "English":
        return TELECOM_DB_PATH
    candidate = TELECOM_DB_PATH.with_name(f"db_{language}.toml")
    if not candidate.exists() or candidate.stat().st_size == 0:
        raise FileNotFoundError(f"Translated telecom DB missing: {candidate}")
    return candidate


def get_user_db_path(language: str = LANGUAGE) -> Path:
    if not language or language == "English":
        return TELECOM_USER_DB_PATH
    candidate = TELECOM_USER_DB_PATH.with_name(f"user_db_{language}.toml")
    if not candidate.exists() or candidate.stat().st_size == 0:
        raise FileNotFoundError(f"Translated telecom user_db missing: {candidate}")
    return candidate
