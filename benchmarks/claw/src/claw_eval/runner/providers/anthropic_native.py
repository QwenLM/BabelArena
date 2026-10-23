"""Anthropic-native Messages API provider (for models that require the /messages
endpoint rather than the OpenAI chat/completions shape — currently only needed
for real extended-thinking on claude-opus-4-8 via the gateway's anthropic protocol).

Why this exists: the gateway's OpenAI-compat path for claude-opus-4-8 silently
accepts `reasoning_effort` but never engages extended thinking (verified:
usage.output_tokens_details.thinking_tokens == 0 regardless of the value).
The model only supports thinking via the native Anthropic request shape:
  {"thinking": {"type": "adaptive"}, "output_config": {"effort": "max"}}
(the gateway's own 400 error message names this exact shape when you try the
standard `thinking: {"type": "enabled", "budget_tokens": N}` form instead).

Our internal Message/ContentBlock/ToolSpec models are already Anthropic-shaped
(see models/message.py, models/content.py, models/tool.py — ToolSpec.input_schema
maps directly), so this provider is mostly a thin pass-through plus:
  - splitting out the system-role Message into the top-level `system` field
  - merging consecutive same-role messages (Anthropic requires strict
    user/assistant alternation; our loop can emit two consecutive user
    messages — e.g. tool results then an injected media message)
  - round-tripping the `thinking` block (with its `signature`) on turns that
    are re-sent as history, since Claude requires it to be echoed back
    verbatim on any assistant turn that used extended thinking before a
    tool_use continuation
"""

from __future__ import annotations

import json
import random
import time
from typing import Any

import httpx

from ...models.content import AudioBlock, ImageBlock, TextBlock, ToolResultBlock, ToolUseBlock, VideoBlock
from ...models.message import Message
from ...models.tool import ToolSpec
from ...models.trace import TokenUsage

_ANTHROPIC_VERSION = "2023-06-01"
_REASONING_MARKER = "__anthropic_thinking__:"  # prefix so we only ever parse our own encoding


def _encode_reasoning(block: dict[str, Any]) -> str:
    """Pack a thinking/redacted_thinking block into Message.reasoning_content.

    JSON-encoded so the signature (required for a correct round-trip) survives;
    prefixed so we never misinterpret plain-string reasoning_content written by
    some other provider/path as ours.
    """
    return _REASONING_MARKER + json.dumps(block)


def _decode_reasoning(reasoning_content: str | None) -> dict[str, Any] | None:
    if not reasoning_content or not reasoning_content.startswith(_REASONING_MARKER):
        return None
    try:
        return json.loads(reasoning_content[len(_REASONING_MARKER):])
    except json.JSONDecodeError:
        return None


def _tool_spec_to_anthropic(spec: ToolSpec) -> dict[str, Any]:
    return {"name": spec.name, "description": spec.description, "input_schema": spec.input_schema}


def _blocks_to_anthropic_content(msg: Message) -> list[dict[str, Any]]:
    parts: list[dict[str, Any]] = []
    thinking_block = _decode_reasoning(msg.reasoning_content)
    if thinking_block is not None:
        parts.append(thinking_block)
    for block in msg.content:
        if block.type == "text":
            parts.append({"type": "text", "text": block.text})
        elif block.type == "tool_use":
            block = block if isinstance(block, ToolUseBlock) else ToolUseBlock.model_validate(block)
            parts.append({"type": "tool_use", "id": block.id, "name": block.name, "input": block.input})
        elif block.type == "tool_result":
            block = block if isinstance(block, ToolResultBlock) else ToolResultBlock.model_validate(block)
            parts.append({
                "type": "tool_result",
                "tool_use_id": block.tool_use_id,
                "content": [{"type": "text", "text": t.text} for t in block.content],
                "is_error": block.is_error,
            })
        elif block.type == "image":
            block = block if isinstance(block, ImageBlock) else ImageBlock.model_validate(block)
            parts.append({
                "type": "image",
                "source": {"type": "base64", "media_type": block.mime_type, "data": block.data},
            })
        elif block.type in ("audio", "video"):
            # Anthropic's Messages API has no native audio/video content block.
            # Fall back to a text marker (mirrors openai_compat.py's video handling).
            block = block if isinstance(block, (AudioBlock, VideoBlock)) else block
            parts.append({
                "type": "text",
                "text": f"[{block.type} attached: {getattr(block, 'source_path', None) or 'inline'} "
                        f"({block.mime_type}) — not supported as a native input block by this provider]",
            })
    if not parts:
        parts.append({"type": "text", "text": ""})
    return parts


def _messages_to_anthropic(messages: list[Message], strip_stale_thinking: bool = False) -> tuple[str | None, list[dict[str, Any]]]:
    """Split out the system message and merge consecutive same-role turns."""
    system_text_parts: list[str] = []
    converted: list[dict[str, Any]] = []
    for msg in messages:
        if msg.role == "system":
            system_text_parts.append(msg.text)
            continue
        content = _blocks_to_anthropic_content(msg)
        if converted and converted[-1]["role"] == msg.role:
            converted[-1]["content"].extend(content)
        else:
            converted.append({"role": msg.role, "content": content})
    # By DEFAULT keep the full thinking round-trip (best quality — stripping the
    # thinking history degrades opus-5's general/multi_turn agentic scores, verified:
    # general+multi_turn ~0.79 with full round-trip vs ~0.48 when stripped).
    # Only when a prior attempt hit HTTP 400 "Invalid signature" do we strip thinking
    # from all-but-the-last assistant turn (fallback) — stale signatures from earlier
    # turns are what opus-5 rejects. So most tasks keep full thinking; only the ones
    # that actually 400 fall back to stripping instead of failing.
    if strip_stale_thinking:
        asst_positions = [i for i, m in enumerate(converted) if m["role"] == "assistant"]
        for i in asst_positions[:-1]:
            stripped = [
                b for b in converted[i]["content"]
                if not (isinstance(b, dict) and b.get("type") in ("thinking", "redacted_thinking"))
            ]
            converted[i]["content"] = stripped or [{"type": "text", "text": ""}]
    system_text = "\n\n".join(system_text_parts) if system_text_parts else None
    return system_text, converted


# 401/408 added: on this gateway the SAME key intermittently 401s under load
# (transient auth/overload hiccup, not a bad key — most requests succeed), so retry
# rather than fail the task. 4xx that are genuinely deterministic (e.g. a real
# signature error) are handled upstream by not re-sending stale thinking blocks.
_RETRYABLE_STATUS = {401, 408, 429, 500, 502, 503, 504, 522, 524, 529}


class AnthropicNativeProvider:
    """Calls the Anthropic Messages API shape directly (e.g. a gateway's /protocol/anthropic/v1)."""

    def __init__(
        self,
        model_id: str,
        api_key: str | None = None,
        base_url: str | None = None,
        extra_body: dict | None = None,
        temperature: float | None = None,
        reasoning_effort: str | None = None,
    ) -> None:
        self.model_id = model_id
        self.extra_body = extra_body or {}
        # Anthropic requires temperature to be unset/1.0 whenever `thinking` is
        # enabled; only forward an explicit non-null value, and never alongside
        # a thinking config we were asked to send.
        self.temperature = temperature
        # reasoning_effort is accepted-but-inert on this endpoint (verified via
        # thinking_tokens==0); real control is extra_body.thinking / .output_config.
        # Kept as a constructor param only for interface parity with the other
        # provider so cli.py's call sites don't need per-provider branching.
        self.reasoning_effort = reasoning_effort
        base = (base_url or "").rstrip("/")
        self._url = f"{base}/messages"
        self._headers = {
            "x-api-key": api_key or "",
            "anthropic-version": _ANTHROPIC_VERSION,
            "Content-Type": "application/json",
        }
        # 600s (not 300): opus-5 at effort=max can take 300s+ on a single call.
        self._client = httpx.Client(timeout=httpx.Timeout(600.0, connect=20.0))

    def chat(
        self,
        messages: list[Message],
        tools: list[ToolSpec] | None = None,
    ) -> tuple[Message, TokenUsage]:
        # Full thinking round-trip by default; only strip stale thinking after a
        # signature-400 (set below). Rebuildable so we can switch on that fallback.
        strip_thinking = False

        def _build_body() -> dict[str, Any]:
            system_text, anthropic_messages = _messages_to_anthropic(messages, strip_stale_thinking=strip_thinking)
            b: dict[str, Any] = {
                "model": self.model_id,
                "max_tokens": 8192,
                "messages": anthropic_messages,
            }
            if system_text:
                b["system"] = system_text
            if tools:
                b["tools"] = [_tool_spec_to_anthropic(t) for t in tools]
            # extra_body keys (thinking, output_config, max_tokens, ...) merge straight
            # into the top-level request body — this IS the native body, no wrapper.
            b.update(dict(self.extra_body))
            if self.temperature is not None and "thinking" not in b:
                b["temperature"] = self.temperature
            return b

        body = _build_body()

        has_multimodal_input = any(
            b.type in {"image", "audio", "video"} for m in messages for b in m.content
        )

        max_retries = 10
        last_exc: Exception | None = None
        for attempt in range(max_retries + 1):
            try:
                resp = self._client.post(self._url, headers=self._headers, json=body)
                if resp.status_code >= 400:
                    txt_low = resp.text.lower()
                    # Signature-400 fallback: opus-5 rejects stale thinking-block
                    # signatures from earlier turns. Rather than fail (or strip
                    # thinking for everyone, which degrades quality), rebuild THIS
                    # task's request with stale thinking stripped and retry.
                    if (resp.status_code == 400 and "signature" in txt_low
                            and not strip_thinking and attempt < max_retries):
                        strip_thinking = True
                        body = _build_body()
                        last_exc = RuntimeError("HTTP 400 invalid signature (retry w/ stale thinking stripped)")
                        time.sleep(random.uniform(1, 2))
                        continue
                    exc = RuntimeError(f"HTTP {resp.status_code}: {resp.text[:500]}")
                    if resp.status_code in _RETRYABLE_STATUS and attempt < max_retries:
                        raise exc
                    if resp.status_code not in _RETRYABLE_STATUS:
                        if has_multimodal_input:
                            raise RuntimeError(
                                f"Model endpoint rejected multimodal input (HTTP {resp.status_code}: "
                                f"{resp.text[:300]}). Check provider support for image/audio/video "
                                "message parts, or set media.strict_mode=false to allow skips."
                            ) from exc
                        raise exc
                    raise exc
                return self._parse_response(resp.json())
            except Exception as exc:  # noqa: BLE001 - broad: retry loop needs to see any transient failure
                last_exc = exc
                exc_str = str(exc).lower()
                status = getattr(exc, "status_code", None)
                retryable = (
                    status in _RETRYABLE_STATUS
                    or "timeout" in exc_str
                    or "timed out" in exc_str
                    or "connect" in exc_str
                    or any(f"http {c}" in exc_str for c in _RETRYABLE_STATUS)
                    # Transient gateway auth/routing hiccups on opus-5 (intermittent —
                    # most requests succeed): "API key is not scoped to a workspace",
                    # and the gateway's "AllModelsFailed" wrapper. Retry rather than fail.
                    or "not scoped to a workspace" in exc_str
                    or "allmodelsfailed" in exc_str
                )
                if not retryable or attempt == max_retries:
                    raise
                delay = random.uniform(2, 4)
                print(f"[retry] Anthropic API error ({type(exc).__name__}), "
                      f"attempt {attempt + 1}/{max_retries}, waiting {delay:.1f}s ...")
                time.sleep(delay)

        raise last_exc or RuntimeError("All retries exhausted")

    def _parse_response(self, data: dict[str, Any]) -> tuple[Message, TokenUsage]:
        content_blocks: list[Any] = []
        reasoning: str | None = None
        for b in data.get("content", []):
            btype = b.get("type")
            if btype == "text":
                content_blocks.append(TextBlock(text=b.get("text", "")))
            elif btype == "tool_use":
                content_blocks.append(ToolUseBlock(id=b["id"], name=b["name"], input=b.get("input", {})))
            elif btype in ("thinking", "redacted_thinking"):
                # Preserve verbatim (incl. signature) for round-trip on the next turn.
                reasoning = _encode_reasoning(b)
            # ignore other/unknown block types rather than erroring

        usage = data.get("usage", {})
        token_usage = TokenUsage(
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
        )
        return Message(role="assistant", content=content_blocks, reasoning_content=reasoning), token_usage
