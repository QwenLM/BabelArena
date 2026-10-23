#!/usr/bin/env python3
"""Print a named task subset's case IDs as CSV (prints nothing for 'full').

Used by the domain run.sh scripts to translate BENCHMARK_TASK_SUBSET into the
existing strict --task-ids/--rerun-ids selector plumbing. Exit code 2 with a
message on stderr for any resolution failure (unknown subset, bad file, ...).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from task_selection import (  # noqa: E402
    DEFAULT_TASK_SUBSET,
    SUBSET_DOMAIN_KEYS,
    effective_task_subset_name,
    resolve_task_subset,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("domain_key", choices=SUBSET_DOMAIN_KEYS)
    parser.add_argument(
        "--name",
        default=None,
        help=f"Subset name (default: $BENCHMARK_TASK_SUBSET or '{DEFAULT_TASK_SUBSET}')",
    )
    args = parser.parse_args(argv)

    try:
        ids = resolve_task_subset(
            effective_task_subset_name(args.name), args.domain_key
        )
    except ValueError as exc:
        print(f"resolve_task_subset: {exc}", file=sys.stderr)
        return 2
    if ids:
        print(",".join(ids))
    return 0


if __name__ == "__main__":
    sys.exit(main())
