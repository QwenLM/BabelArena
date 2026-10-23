"""Content-hash fingerprint of the files that define a VitaBench benchmark run.

A "benchmark" here is determined by:
  - The task data files (data/vita/domains/{domain}/tasks_{language}.json)
  - The tool definitions (src/vita/domains/{domain}/tools.py and tools_schema.py)
  - The shared environment/policy/evaluator code
  - The prompt templates (src/vita/prompts/*.yaml)

`git_commit` alone is unreliable because it captures only the last commit, not
uncommitted working-tree edits. The hash here is computed from the live file
contents at run time so two sims with the same `benchmark_hash` are guaranteed
to have used identical benchmark inputs.
"""

import hashlib
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Static files that affect benchmark behavior regardless of domain/language.
_STATIC_RELPATHS = [
    "src/vita/environment/toolkit.py",
    "src/vita/environment/environment.py",
    "src/vita/environment/policy.py",
    "src/vita/environment/toolkit_schema.py",
    "src/vita/evaluator/evaluator.py",
]

# Globs under PROJECT_ROOT that should be hashed in their entirety.
_PROMPT_DIR = "src/vita/prompts"


def _hash_file(path: Path) -> Optional[str]:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except (FileNotFoundError, IsADirectoryError):
        return None


def _task_file_relpath(domain: str, language: str) -> str:
    """Return the relative path to the task file for (domain, language).

    Uses vita's own TASK_FILE_SUFFIX mapping so we always look up the same
    file that vita will actually load at run time. Chinese (the source
    language) has no suffix.
    """
    # Import lazily to avoid a hard dependency cycle when this module is
    # imported as a standalone CLI.
    try:
        from vita.utils.utils import TASK_FILE_SUFFIX
        suffix = TASK_FILE_SUFFIX.get(language, "")
    except ImportError:
        # Standalone usage without vita on path; fall back to the conventional
        # 2-letter code via a minimal table covering the languages we ship.
        suffix = {
            "chinese": "", "english": "_en", "arabic": "_ar", "french": "_fr",
            "japanese": "_ja", "russian": "_ru", "spanish": "_es", "thai": "_th",
            "hindi": "_hi",
        }.get(language, "")
    return f"data/vita/domains/{domain}/tasks{suffix}.json"


def _gather_paths(domain: str, language: str) -> list[str]:
    """Return ordered, deduped list of relative paths that define this benchmark run."""
    domains = [d.strip() for d in domain.split(",") if d.strip()]
    paths: list[str] = []

    for rel in _STATIC_RELPATHS:
        paths.append(rel)

    # Prompts (sorted for determinism)
    for p in sorted((PROJECT_ROOT / _PROMPT_DIR).glob("*.yaml")):
        paths.append(str(p.relative_to(PROJECT_ROOT)))

    for d in domains:
        paths.append(f"src/vita/domains/{d}/tools.py")
        paths.append(f"src/vita/domains/{d}/tools_schema.py")
        paths.append(_task_file_relpath(d, language))

    # Cross-domain task data is used when more than one domain is active.
    if len(domains) > 1:
        paths.append(_task_file_relpath("cross_domain", language))

    seen = set()
    ordered = []
    for rp in paths:
        if rp not in seen:
            seen.add(rp)
            ordered.append(rp)
    return ordered


def compute_benchmark_hash(domain: str, language: str) -> dict:
    """Compute a content fingerprint over all files contributing to a benchmark.

    Returns a dict with:
        combined_hash: 64-char sha256 hex over (relpath=sha256;)* of every contributing file
        files: dict mapping relative file path -> per-file sha256 hex
    """
    combined = hashlib.sha256()
    files: dict[str, str] = {}
    for relpath in _gather_paths(domain, language):
        h = _hash_file(PROJECT_ROOT / relpath)
        if h is None:
            continue
        files[relpath] = h
        combined.update(f"{relpath}={h};".encode())
    return {"combined_hash": combined.hexdigest(), "files": files}


def benchmark_version_tag(domain: str, language: str, length: int = 12) -> str:
    """Short tag suitable for filesystem path use (default 12 hex chars)."""
    return compute_benchmark_hash(domain, language)["combined_hash"][:length]


# Named-version registry
# A `.benchmark_version` file at PROJECT_ROOT, if present, declares the human-readable
# name (e.g. "v2") used in result paths. Without it we fall back to the short hash tag.
_VERSION_FILE = PROJECT_ROOT / ".benchmark_version"


def current_version_name(domain: Optional[str] = None, language: Optional[str] = None) -> str:
    """Return the version name to use for output paths.

    Priority:
      1. Contents of `.benchmark_version` (stripped) if the file exists and is non-empty.
      2. Short content-hash tag computed from (domain, language) if both are given.
      3. The literal string "unversioned" as a last resort.
    """
    if _VERSION_FILE.exists():
        name = _VERSION_FILE.read_text(encoding="utf-8").strip()
        if name:
            return name
    if domain and language:
        return benchmark_version_tag(domain, language)
    return "unversioned"


if __name__ == "__main__":
    import argparse
    import json
    p = argparse.ArgumentParser(description="Compute VitaBench benchmark hash.")
    p.add_argument("--domain", required=True, help="Domain (or comma-separated for cross-domain).")
    p.add_argument("--language", required=True)
    p.add_argument("--manifest", action="store_true", help="Print per-file hash manifest.")
    p.add_argument("--version-name", action="store_true", help="Print the declared version name (from .benchmark_version) or short hash tag.")
    args = p.parse_args()
    result = compute_benchmark_hash(args.domain, args.language)
    if args.version_name:
        print(current_version_name(args.domain, args.language))
    elif args.manifest:
        print(json.dumps(result, indent=2))
    else:
        print(result["combined_hash"])
        print(f"tag: {result['combined_hash'][:12]}")
        print(f"version_name: {current_version_name(args.domain, args.language)}")
