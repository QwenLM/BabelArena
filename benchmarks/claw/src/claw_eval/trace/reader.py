"""JSONL trace reader with type-based partitioning."""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from pathlib import Path

from ..models.trace import (
    AuditSnapshot,
    GradingResult,
    MediaLoad,
    ToolDispatch,
    TraceEnd,
    TraceMessage,
    TraceStart,
)
from ._frames import RehydrationContext, rehydrate_event_dict

_EVENT_MAP = {
    "trace_start": TraceStart,
    "message": TraceMessage,
    "tool_dispatch": ToolDispatch,
    "audit_snapshot": AuditSnapshot,
    "media_load": MediaLoad,
    "trace_end": TraceEnd,
    "grading_result": GradingResult,
}

_OPT_OUT_ENV = "CLAW_EVAL_NO_REHYDRATE"


def _rehydrate_enabled(explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    return os.environ.get(_OPT_OUT_ENV, "").lower() not in ("1", "true", "yes")


def read_events(
    path: str | Path,
    *,
    rehydrate: bool | None = None,
) -> Iterator[TraceStart | TraceMessage | ToolDispatch | AuditSnapshot | MediaLoad | TraceEnd]:
    """Parse each JSONL line by its ``type`` discriminator field.

    Stripped ReadMedia frames are transparently rehydrated unless ``rehydrate=False``
    (or ``CLAW_EVAL_NO_REHYDRATE=1``) — useful for tooling that only needs metadata.
    """
    do_rehydrate = _rehydrate_enabled(rehydrate)
    ctx = RehydrationContext.from_trace_path(path) if do_rehydrate else None

    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            event_type = raw.get("type")
            cls = _EVENT_MAP.get(event_type)
            if cls is None:
                raise ValueError(f"Unknown trace event type: {event_type!r}")
            if do_rehydrate:
                raw = rehydrate_event_dict(raw, ctx)
            yield cls.model_validate(raw)


def load_trace(
    path: str | Path,
    *,
    rehydrate: bool | None = None,
) -> tuple[TraceStart, list[TraceMessage], list[ToolDispatch], list[MediaLoad], TraceEnd | None, dict[str, dict]]:
    """Load a full trace file and partition by event type.

    Returns (start, messages, dispatches, media_events, end, audit_data).
    audit_data is keyed by service_name from AuditSnapshot events.
    GradingResult events are silently skipped (they are post-hoc additions).
    """
    start: TraceStart | None = None
    messages: list[TraceMessage] = []
    dispatches: list[ToolDispatch] = []
    media_events: list[MediaLoad] = []
    end: TraceEnd | None = None
    audit_data: dict[str, dict] = {}

    for event in read_events(path, rehydrate=rehydrate):
        match event:
            case TraceStart():
                start = event
            case TraceMessage():
                messages.append(event)
            case ToolDispatch():
                dispatches.append(event)
            case AuditSnapshot():
                audit_data[event.service_name] = event.audit_data
            case MediaLoad():
                media_events.append(event)
            case TraceEnd():
                end = event
            case GradingResult():
                pass  # post-hoc grading data; not needed for re-grading

    if start is None:
        raise ValueError(f"No TraceStart event found in {path}")
    return start, messages, dispatches, media_events, end, audit_data
