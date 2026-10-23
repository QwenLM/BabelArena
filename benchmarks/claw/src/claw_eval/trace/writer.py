"""Append-only JSONL trace writer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import IO

from ..models.trace import (
    AuditSnapshot,
    MediaLoad,
    TraceEnd,
    TraceMessage,
    TraceStart,
    ToolDispatch,
)
from ._frames import strip_event_dict


class TraceWriter:
    """Writes trace events as JSONL (one JSON object per line).

    ReadMedia video frames are auto-stripped on write; see ``trace._frames``.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh: IO[str] | None = None

    def _ensure_open(self) -> IO[str]:
        if self._fh is None or self._fh.closed:
            self._fh = open(self.path, "a")
        return self._fh

    def write_event(self, event: TraceStart | TraceMessage | ToolDispatch | AuditSnapshot | MediaLoad | TraceEnd) -> None:
        fh = self._ensure_open()
        # Round-trip via dict so strip can rewrite response_body without mutating
        # the caller's pydantic event object.
        raw = event.model_dump(mode="json")
        raw = strip_event_dict(raw)
        fh.write(json.dumps(raw, ensure_ascii=False, separators=(",", ":")) + "\n")
        fh.flush()

    def close(self) -> None:
        if self._fh and not self._fh.closed:
            self._fh.close()

    def __enter__(self) -> "TraceWriter":
        return self

    def __exit__(self, *exc) -> None:
        self.close()
