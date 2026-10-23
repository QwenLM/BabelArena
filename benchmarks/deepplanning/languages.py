"""Central language registry for the deepplanning benchmark.

Single source of truth for language identity. Every component (translator,
verifier, runners, prompt loaders) reads from this table — never invents its
own casing or aliasing logic.

Naming dimensions captured here:
  - switch_key: lowercase English name used in CLI / env vars / dicts.
                  e.g. "japanese", "eastern_panjabi"
  - code: ISO-639-1 / -3 short code used as file suffix.
                  e.g. "ja", "pa"
  - display: capitalized English name passed to translator LLM prompts.
                  e.g. "Japanese", "Eastern Panjabi"

Canonical baseline languages are English and Chinese — these ship pre-built in
the repo (database_en/database_zh, tool_schema_en/tool_schema_zh, etc.). Every
non-baseline language ships its own per-language rendered seed DB
(database_<code>/, rendered from database_en/ by
the rendering pipeline) whose meta_info anchors are the localized
values; each LanguageSpec's canonical_db_code points at that per-language DB.
Only the user-facing surface is translated — query text, constraint context,
prompts, tool descriptions, and tool response labels — with proper nouns
preserved by the translator and then localized to the per-language DB by
a prose-localization pass. Scoring anchors on the per-language DB,
not on English.

A language is supported when:
  1. It is registered here.
  2. Its translated artifacts exist on disk (all 23 ship pre-rendered).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class LanguageSpec:
    switch_key: str
    code: str
    display: str
    script_family: str  # 'latin', 'cjk', 'cyrillic', 'arabic', 'devanagari', 'thai', 'hebrew', 'gurmukhi', 'khmer', 'burmese', 'lao', 'tamil', 'telugu'
    baseline: bool = False  # True for languages that ship pre-built (en, zh)
    canonical_db_code: str = "en"  # travel: which database_<code>/ to use as the data layer
    shopping_canonical_db_code: str = "en"  # shopping: which database_level{N}_<code>/ to use

    @property
    def is_baseline(self) -> bool:
        return self.baseline


_LANGUAGES: List[LanguageSpec] = [
    # Baseline (ship pre-built — DB, tool schemas, prompts already curated)
    LanguageSpec("english", "en", "English", "latin", baseline=True, canonical_db_code="en"),
    LanguageSpec("chinese", "zh", "Chinese", "cjk", baseline=True, canonical_db_code="zh", shopping_canonical_db_code="zh"),
    # Non-baseline — each has a localized database_<code>/ rendered by
    # the rendering pipeline from database_en/, with the
    # canonical_db_code pointing at its own DB.
    LanguageSpec("japanese", "ja", "Japanese", "cjk", canonical_db_code="ja", shopping_canonical_db_code="ja"),
    LanguageSpec("french", "fr", "French", "latin", canonical_db_code="fr", shopping_canonical_db_code="fr"),
    LanguageSpec("russian", "ru", "Russian", "cyrillic", canonical_db_code="ru", shopping_canonical_db_code="ru"),
    LanguageSpec("arabic", "ar", "Arabic", "arabic", canonical_db_code="ar", shopping_canonical_db_code="ar"),
    LanguageSpec("spanish", "es", "Spanish", "latin", canonical_db_code="es", shopping_canonical_db_code="es"),
    LanguageSpec("korean", "ko", "Korean", "cjk", canonical_db_code="ko", shopping_canonical_db_code="ko"),
    LanguageSpec("indonesian", "id", "Indonesian", "latin", canonical_db_code="id", shopping_canonical_db_code="id"),
    LanguageSpec("hindi", "hi", "Hindi", "devanagari", canonical_db_code="hi", shopping_canonical_db_code="hi"),
    LanguageSpec("thai", "th", "Thai", "thai", canonical_db_code="th", shopping_canonical_db_code="th"),
    LanguageSpec("hebrew", "he", "Hebrew", "hebrew", canonical_db_code="he", shopping_canonical_db_code="he"),
    LanguageSpec("turkish", "tr", "Turkish", "latin", canonical_db_code="tr", shopping_canonical_db_code="tr"),
    LanguageSpec("vietnamese", "vi", "Vietnamese", "latin", canonical_db_code="vi", shopping_canonical_db_code="vi"),
    LanguageSpec("malay", "ms", "Malay", "latin", canonical_db_code="ms", shopping_canonical_db_code="ms"),
    LanguageSpec("belarusian", "be", "Belarusian", "cyrillic", canonical_db_code="be", shopping_canonical_db_code="be"),
    LanguageSpec("eastern_panjabi", "pa", "Eastern Panjabi", "gurmukhi", canonical_db_code="pa", shopping_canonical_db_code="pa"),
    LanguageSpec("kazakh", "kk", "Kazakh", "cyrillic", canonical_db_code="kk", shopping_canonical_db_code="kk"),
    LanguageSpec("khmer", "km", "Khmer", "khmer", canonical_db_code="km", shopping_canonical_db_code="km"),
    LanguageSpec("burmese", "my", "Burmese", "burmese", canonical_db_code="my", shopping_canonical_db_code="my"),
    LanguageSpec("lao", "lo", "Lao", "lao", canonical_db_code="lo", shopping_canonical_db_code="lo"),
    LanguageSpec("tamil", "ta", "Tamil", "tamil", canonical_db_code="ta", shopping_canonical_db_code="ta"),
    LanguageSpec("telugu", "te", "Telugu", "telugu", canonical_db_code="te", shopping_canonical_db_code="te"),
]

_BY_SWITCH_KEY: Dict[str, LanguageSpec] = {lang.switch_key: lang for lang in _LANGUAGES}
_BY_CODE: Dict[str, LanguageSpec] = {lang.code: lang for lang in _LANGUAGES}

# Common aliases users may type or that legacy code already uses.
_ALIASES: Dict[str, str] = {
    # legacy zh/en codes used as the switch
    "zh": "chinese",
    "en": "english",
    # other common aliases
    "ja": "japanese",
    "fr": "french",
    "ru": "russian",
    "ar": "arabic",
    "es": "spanish",
    "ko": "korean",
    "id": "indonesian",
    "hi": "hindi",
    "th": "thai",
    "he": "hebrew",
    "iw": "hebrew",  # old ISO-639-1 alias
    "tr": "turkish",
    "vi": "vietnamese",
    "ms": "malay",
    "be": "belarusian",
    "pa": "eastern_panjabi",
    "punjabi": "eastern_panjabi",
    "kk": "kazakh",
    "km": "khmer",
    "my": "burmese",
    "myanmar": "burmese",
    "lo": "lao",
    "ta": "tamil",
    "te": "telugu",
}


class UnknownLanguage(ValueError):
    """Raised when the user requests a language not in the registry."""


def resolve_language(key: Optional[str]) -> Optional[LanguageSpec]:
    """Resolve a user-supplied language identifier to a LanguageSpec.

    Accepts switch_key, code, or alias (case-insensitive). Returns None for
    an empty/None input (caller decides what 'no language' means in context).

    Raises UnknownLanguage for unrecognized input.
    """
    if key is None:
        return None
    k = str(key).strip().lower().replace("-", "_").replace(" ", "_")
    if not k:
        return None
    # Direct match by switch_key
    if k in _BY_SWITCH_KEY:
        return _BY_SWITCH_KEY[k]
    # Code match (preferred over alias for explicit ISO codes)
    if k in _BY_CODE:
        return _BY_CODE[k]
    # Alias lookup
    if k in _ALIASES:
        return _BY_SWITCH_KEY[_ALIASES[k]]
    raise UnknownLanguage(
        f"Unknown language identifier: {key!r}. "
        f"Supported: {', '.join(sorted(_BY_SWITCH_KEY))}"
    )


def all_languages(include_baseline: bool = True) -> List[LanguageSpec]:
    """Return all registered language specs."""
    if include_baseline:
        return list(_LANGUAGES)
    return [lang for lang in _LANGUAGES if not lang.baseline]


def get_current_language() -> Optional[LanguageSpec]:
    """Read the active language from environment.

    Looks at DEEPPLANNING_LANGUAGE first, then BENCHMARK_LANGUAGE for
    compatibility with existing run.sh scripts. Returns None if neither is
    set or both are empty (callers fall back to baseline behavior).
    """
    for var in ("DEEPPLANNING_LANGUAGE", "BENCHMARK_LANGUAGE"):
        val = os.environ.get(var, "").strip()
        if val:
            return resolve_language(val)
    return None
