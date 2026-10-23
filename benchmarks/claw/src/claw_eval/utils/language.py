"""Language resolution for claw-eval multi-language support.

A single resolver table maps the user-facing language name (CLI flag, env
var) to its file-suffix form, ISO code, and display name. All four naming
dimensions live in one place so every loader / verifier / translator
references the same source of truth.

Adding a language: append one entry to ``_LANGUAGES``. The pipeline picks
up the rest (path resolver, verifier, translator config).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


@dataclass(frozen=True)
class LanguageInfo:
    """All naming dimensions for one language.

    - ``key``     : canonical lower-case switch (CLI flag value, dict key)
    - ``code``    : lowercase ISO-639-1 code (matches ``prompt.language`` in YAML)
    - ``suffix``  : sidecar-file suffix, identical to ``code`` by default
    - ``display`` : capitalised English display name, used inside LLM prompts
    - ``aliases`` : extra accepted spellings (for example BCP-47 tags)
    """

    key: str
    code: str
    display: str
    suffix: str
    aliases: tuple[str, ...] = ()


_LANGUAGES: tuple[LanguageInfo, ...] = (
    LanguageInfo("english",  "en",  "English",          "en"),
    LanguageInfo("chinese",  "zh",  "Chinese",          "zh", aliases=("zh-cn", "zh_cn", "mandarin")),
    LanguageInfo("japanese", "ja",  "Japanese",         "ja"),
    LanguageInfo("french",   "fr",  "French",           "fr"),
    LanguageInfo("russian",  "ru",  "Russian",          "ru"),
    LanguageInfo("arabic",   "ar",  "Arabic",           "ar"),
    LanguageInfo("spanish",  "es",  "Spanish",          "es"),
    LanguageInfo("korean",   "ko",  "Korean",           "ko"),
    LanguageInfo("indonesian","id", "Indonesian",       "id"),
    LanguageInfo("hindi",    "hi",  "Hindi",            "hi"),
    LanguageInfo("thai",     "th",  "Thai",             "th"),
    LanguageInfo("hebrew",   "he",  "Hebrew",           "he", aliases=("iw",)),
    LanguageInfo("turkish",  "tr",  "Turkish",          "tr"),
    LanguageInfo("vietnamese","vi", "Vietnamese",       "vi"),
    LanguageInfo("malay",    "ms",  "Malay",            "ms"),
    LanguageInfo("belarusian","be", "Belarusian",       "be"),
    LanguageInfo("punjabi",  "pa",  "Eastern Panjabi",  "pa", aliases=("eastern_panjabi", "panjabi")),
    LanguageInfo("kazakh",   "kk",  "Kazakh",           "kk"),
    LanguageInfo("khmer",    "km",  "Khmer",            "km"),
    LanguageInfo("burmese",  "my",  "Burmese",          "my", aliases=("myanmar",)),
    LanguageInfo("lao",      "lo",  "Lao",              "lo"),
    LanguageInfo("tamil",    "ta",  "Tamil",            "ta"),
    LanguageInfo("telugu",   "te",  "Telugu",           "te"),
)


_BY_LOOKUP: dict[str, LanguageInfo] = {}
for _info in _LANGUAGES:
    _BY_LOOKUP[_info.key] = _info
    _BY_LOOKUP[_info.code] = _info
    _BY_LOOKUP[_info.suffix] = _info
    _BY_LOOKUP[_info.display.lower()] = _info
    for _alias in _info.aliases:
        _BY_LOOKUP[_alias.lower()] = _info


_ENV_VAR = "CLAW_EVAL_LANGUAGE"


def all_languages() -> tuple[LanguageInfo, ...]:
    """Return every registered language (source order, includes baselines)."""
    return _LANGUAGES


def non_baseline_languages() -> Iterable[LanguageInfo]:
    """Yield every translation target (excludes English / Chinese baselines)."""
    return [info for info in _LANGUAGES if info.code not in ("en", "zh")]


def resolve_language(name: str | None) -> LanguageInfo | None:
    """Map any accepted spelling to its ``LanguageInfo``.

    Returns ``None`` when ``name`` is empty / None. Raises ``ValueError``
    if the spelling is non-empty but unknown — never silently fall back.
    """
    if name is None:
        return None
    cleaned = name.strip().lower()
    if not cleaned:
        return None
    if cleaned in _BY_LOOKUP:
        return _BY_LOOKUP[cleaned]
    accepted = ", ".join(sorted({info.key for info in _LANGUAGES}))
    raise ValueError(
        f"Unknown language '{name}'. Accepted (case-insensitive): {accepted}. "
        f"ISO codes and capitalised display names are also accepted."
    )


def get_runtime_language() -> LanguageInfo | None:
    """Read ``CLAW_EVAL_LANGUAGE`` from the environment.

    Used as a last-resort fallback when the CLI didn't pass ``--language``
    explicitly (mostly for worker subprocesses).
    """
    return resolve_language(os.environ.get(_ENV_VAR))


def task_source_language(task_yaml: str | Path) -> str:
    """Return the ``prompt.language`` field of a task YAML (or empty)."""
    path = Path(task_yaml)
    if not path.exists():
        return ""
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return ((data.get("prompt") or {}).get("language") or "").strip().lower()


def task_yaml_path(
    task_dir: str | Path,
    language: str | LanguageInfo | None = None,
) -> Path:
    """Pick ``task_<suffix>.yaml`` or ``task.yaml`` for the requested language.

    Resolution order:
    1. ``language`` empty / None → ``task.yaml`` (baseline).
    2. ``language`` resolves to the task's source language → ``task.yaml``.
    3. Otherwise → ``task_<suffix>.yaml``, raising if it is missing or empty.

    The strict raise on step 3 is deliberate: silent baseline fallback turns
    a "completed" cross-language run into a lie about which language was
    actually evaluated (see the language-support skill).
    """
    base_dir = Path(task_dir)
    if base_dir.is_file():
        base_dir = base_dir.parent

    baseline = base_dir / "task.yaml"
    if not baseline.exists():
        raise FileNotFoundError(f"No task.yaml found in {base_dir}")

    info = language if isinstance(language, LanguageInfo) else resolve_language(language)
    if info is None:
        return baseline

    src_code = task_source_language(baseline)
    if info.code == src_code:
        return baseline

    sidecar = base_dir / f"task_{info.suffix}.yaml"
    if not sidecar.exists() or sidecar.stat().st_size == 0:
        raise FileNotFoundError(
            f"Language '{info.display}' requested but {sidecar} is missing or empty. "
            f"Re-fetch the task data (./bench fetch-data)."
        )
    return sidecar
