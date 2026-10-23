import json
import os
from functools import lru_cache
from pathlib import Path


def _resolve_prompt_override_name() -> str:
    explicit_name = os.getenv("TAU2_PROMPTS_FILE", "").strip()
    if explicit_name:
        return explicit_name

    language = os.getenv("TAU2_LANGUAGE", "").strip()
    if language and language.lower() != "english":
        return f"prompts_{language}.json"

    return ""


@lru_cache(maxsize=1)
def load_prompts() -> dict:
    base_file = Path(__file__).resolve().parent.parent / "prompts.json"
    with open(base_file, "r", encoding="utf-8") as f:
        base_prompts = json.load(f)

    override_name = _resolve_prompt_override_name()
    if not override_name or override_name == "prompts.json":
        return base_prompts

    override_file = Path(__file__).resolve().parent.parent / override_name
    if not override_file.exists():
        # Fail fast like the data loaders: a missing prompts override would
        # silently run the agent with English prompts in a localized eval.
        raise FileNotFoundError(
            f"Prompt override file missing: {override_file}. "
            f"Set TAU2_PROMPTS_FILE to an existing prompts_<Language>.json "
            f"(or unset TAU2_LANGUAGE for an English run)."
        )

    with open(override_file, "r", encoding="utf-8") as f:
        override_prompts = json.load(f)

    merged = {**base_prompts, **override_prompts}
    return merged
