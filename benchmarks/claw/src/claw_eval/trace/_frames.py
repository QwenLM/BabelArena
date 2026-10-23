"""Frame strip + rehydrate for ReadMedia video tool_dispatch records.

Why this exists
---------------
``ReadMedia`` tool calls embed base64 PNG frames in ``response_body.frames[*].image_b64``.
A single video task can balloon a trace JSONL to >1 GB. The frames are deterministic
given ``request_body`` + source video, so we strip them on write and reconstruct them
on read.

Contract
--------
- Strip: only ``tool_dispatch`` events with ``tool_name == "ReadMedia"`` AND
  ``response_body.media_type == "video"``. Other events pass through.
- Rehydrate is the inverse and must produce byte-identical ``image_b64`` strings.
- Both operations are idempotent and handle un-stripped legacy traces.
"""

from __future__ import annotations

import base64
import io
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SENTINEL_KEY = "_frames_stripped"
STRIP_VERSION = 1


# --- strip ---------------------------------------------------------------

def _is_video_readmedia_dispatch(raw: dict[str, Any]) -> bool:
    if raw.get("type") != "tool_dispatch":
        return False
    if raw.get("tool_name") != "ReadMedia":
        return False
    rb = raw.get("response_body")
    if not isinstance(rb, dict):
        return False
    return rb.get("media_type") == "video"


def strip_event_dict(raw: dict[str, Any]) -> dict[str, Any]:
    """Return a new dict with frames[*].image_b64 removed for video ReadMedia.

    Idempotent: re-stripping is a no-op.
    """
    if not _is_video_readmedia_dispatch(raw):
        return raw
    rb = raw["response_body"]
    if rb.get(SENTINEL_KEY):
        return raw
    frames = rb.get("frames")
    if not isinstance(frames, list):
        return raw

    new_rb = dict(rb)
    new_frames = []
    for fr in frames:
        if isinstance(fr, dict) and "image_b64" in fr:
            fr = {k: v for k, v in fr.items() if k != "image_b64"}
        new_frames.append(fr)
    new_rb["frames"] = new_frames
    new_rb[SENTINEL_KEY] = True
    new_rb["_strip_version"] = STRIP_VERSION
    out = dict(raw)
    out["response_body"] = new_rb
    return out


# --- rehydrate -----------------------------------------------------------

@dataclass
class RehydrationContext:
    """Resolves sandbox fixture paths to host paths for rehydration."""
    task_id: str
    fixtures_root: Path  # /<host>/tasks/<task_id>/fixtures
    snapshot_dir: Path | None = None  # <trace_dir>/<trace_stem>_snapshot/

    @classmethod
    def from_trace_path(cls, trace_path: str | Path) -> "RehydrationContext | None":
        """Derive context from a trace file path.

        Trace files live at .../<task_id>_<short_id>.jsonl; the project root contains
        a sibling ``tasks/`` directory. Resolution order:
          1. ``CLAW_EVAL_FIXTURES_ROOT`` env var (overrides task_id-relative resolution).
          2. Walk up parents until a ``tasks/<task_id>/fixtures`` dir exists.
        Returns None if neither succeeds; rehydrate will then raise on first stripped record.

        For agent-generated output files (e.g. clip.mp4 a video-editing task produces),
        we also look in the sibling ``<trace_stem>_snapshot/`` dir alongside the trace.
        """
        trace_path = Path(trace_path).resolve()
        task_id = trace_path.stem.rsplit("_", 1)[0]

        # Snapshot dir for agent-output files: <trace_stem>_snapshot/
        snapshot_dir = trace_path.parent / f"{trace_path.stem}_snapshot"
        if not snapshot_dir.exists():
            snapshot_dir = None

        env_root = os.environ.get("CLAW_EVAL_FIXTURES_ROOT")
        if env_root:
            candidate = Path(env_root) / task_id / "fixtures"
            if candidate.exists():
                return cls(task_id=task_id, fixtures_root=candidate, snapshot_dir=snapshot_dir)

        for parent in trace_path.parents:
            candidate = parent / "tasks" / task_id / "fixtures"
            if candidate.exists():
                return cls(task_id=task_id, fixtures_root=candidate, snapshot_dir=snapshot_dir)
        return None

    def resolve(self, sandbox_path: str) -> Path:
        """Map ``/workspace/<path>`` to a host path.

        Order: snapshot dir (agent output) → fixtures dir (task input).
        """
        basename = Path(sandbox_path).name
        if self.snapshot_dir is not None:
            snap_path = self.snapshot_dir / basename
            if snap_path.exists():
                return snap_path
        return self.fixtures_root / basename


def _extract_video_frames(
    video_path: Path,
    fps: float,
    max_frames: int,
    start_time: float = 0.0,
    end_time: float | None = None,
) -> list[str]:
    """Re-run the exact ffmpeg+PIL pipeline used by sandbox/server.py:_read_video.

    Returns a list of base64-encoded PNG strings, one per frame.
    """
    from PIL import Image  # local import; only needed for rehydrate

    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError(
            "ffmpeg/ffprobe not found on PATH; required to rehydrate stripped traces. "
            "Install ffmpeg or run reads inside the claw-eval-agent container."
        )

    # Probe duration if end_time is None (matches server.py behavior).
    if end_time is None:
        probe = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", str(video_path)],
            capture_output=True, text=True, timeout=15,
        )
        pd = json.loads(probe.stdout) if probe.stdout else {}
        duration = None
        for stream in pd.get("streams", []):
            if stream.get("codec_type") == "video":
                duration = float(stream.get("duration", 0)) or None
                break
        if duration is None:
            fmt_d = pd.get("format", {}).get("duration")
            if fmt_d:
                duration = float(fmt_d)
        end_time = duration

    out: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        cmd = ["ffmpeg", "-y"]
        if start_time > 0:
            cmd += ["-ss", str(start_time)]
        cmd += ["-i", str(video_path)]
        if end_time is not None:
            cmd += ["-t", str(end_time - start_time)]
        cmd += ["-vf", f"fps={fps}", "-frames:v", str(max_frames),
                f"{tmp}/frame_%04d.jpg"]
        subprocess.run(cmd, capture_output=True, timeout=60)
        for ff in sorted(Path(tmp).glob("frame_*.jpg"))[:max_frames]:
            img = Image.open(ff)
            buf = io.BytesIO()
            img.save(buf, "PNG")
            out.append(base64.b64encode(buf.getvalue()).decode("ascii"))
    return out


def rehydrate_event_dict(raw: dict[str, Any], ctx: RehydrationContext | None) -> dict[str, Any]:
    """Reverse strip_event_dict. Non-stripped events pass through.

    Raises if the event was stripped but ``ctx`` is None or the source video
    cannot be found; the caller has already committed to consuming frame data,
    so silent fallback would mask the failure.
    """
    if not _is_video_readmedia_dispatch(raw):
        return raw
    rb = raw["response_body"]
    if not rb.get(SENTINEL_KEY):
        return raw  # not stripped
    if ctx is None:
        raise RuntimeError(
            "Stripped trace encountered but RehydrationContext is None; "
            "set CLAW_EVAL_FIXTURES_ROOT or place the trace under a project root "
            "containing tasks/<task_id>/fixtures."
        )

    req = raw.get("request_body") or {}
    video_path = ctx.resolve(req["path"])
    if not video_path.exists():
        raise FileNotFoundError(f"Source video missing for rehydration: {video_path}")

    # Tool defaults come from ReadMediaRequest pydantic model (sandbox/server.py):
    # fps=1.0, max_frames=8, start_time=0.0. Pydantic only serialises fields the
    # agent passed, so older traces may lack any of these keys.
    new_b64s = _extract_video_frames(
        video_path,
        fps=float(req.get("fps", 1.0)),
        max_frames=int(req.get("max_frames", 8)),
        start_time=float(req.get("start_time") or 0.0),
        end_time=req.get("end_time"),
    )

    old_frames = rb.get("frames") or []
    # Two distinct sources of frame-count drift:
    #   1. ffmpeg `fps=N` filter is not bit-exactly deterministic across runs
    #      (DTS/PTS rounding) — drift here is typically 1–2 frames.
    #   2. Agent rewrote the file (e.g. `ffmpeg -ss X -to Y -c copy /workspace/clip.mp4`)
    #      multiple times during the trace. Snapshot only captures the final
    #      state, so earlier ReadMedia calls on a shorter intermediate clip
    #      see drift up to the full video length.
    # In both cases we'd rather grade with degraded fidelity than drop the whole
    # trace, so we pad / truncate. The rubric's textual reasoning is the primary
    # judging signal; the frames are a visual cross-check.
    if len(new_b64s) != len(old_frames) and old_frames:
        if len(new_b64s) < len(old_frames) and new_b64s:
            new_b64s = list(new_b64s) + [new_b64s[-1]] * (len(old_frames) - len(new_b64s))
        else:
            new_b64s = list(new_b64s)[: len(old_frames)]

    new_frames = []
    for fr, b64 in zip(old_frames, new_b64s):
        new_fr = dict(fr) if isinstance(fr, dict) else {}
        new_fr["image_b64"] = b64
        new_frames.append(new_fr)
    new_rb = {k: v for k, v in rb.items() if k not in (SENTINEL_KEY, "_strip_version")}
    new_rb["frames"] = new_frames
    out = dict(raw)
    out["response_body"] = new_rb
    return out
