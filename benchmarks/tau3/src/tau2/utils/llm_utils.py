import ast
import hashlib
import json
import logging
import random
import re
import threading
import time
import uuid
from contextvars import ContextVar
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import requests
import yaml
from loguru import logger

from tau2.config import (
    DEFAULT_MAX_RETRIES,
    models,
)
from tau2.data_model.message import (
    AssistantMessage,
    Message,
    ParticipantMessageBase,
    SystemMessage,
    ToolCall,
    ToolMessage,
    UserMessage,
)
from tau2.environment.tool import Tool

# =============================================================================
# Gateway request backend (ported from vita/utils/llm_utils.py)
# =============================================================================
#
# Every LLM call (agent / user simulator / NL-assertion judge) funnels through
# generate() below. The model's routing (base_url, headers) and per-model API
# params come from tau2.config.models (loaded from models.yaml). We POST raw
# JSON to the model gateway and normalize the three response shapes we see:
#   - OpenAI chat        {"choices": [...]}
#   - Anthropic native   {"type": "message", "content": [...]}
#   - Responses API      {"object": "response", "output": [...]}

# Context variable to store the directory where LLM debug logs should be written
llm_log_dir: ContextVar[Optional[Path]] = ContextVar("llm_log_dir", default=None)

# Context variable to store the LLM logging mode ("all" or "latest")
llm_log_mode: ContextVar[str] = ContextVar("llm_log_mode", default="latest")

logging.getLogger("LiteLLM").setLevel(logging.WARNING)


# ---- Request-level response cache -----------------------------------------
# Ported from vita but DISABLED by default here: tau2 has no per-task
# reset_response_cache() hook, and correctness must not depend on caching.
# Flip _RESPONSE_CACHE_ENABLED to True (and call reset_response_cache() per
# task) to dedup identical request bodies during whole-task retries.
_RESPONSE_CACHE_ENABLED = False
_response_cache_tls = threading.local()


def _get_response_cache() -> dict:
    cache = getattr(_response_cache_tls, "cache", None)
    if cache is None:
        cache = {}
        _response_cache_tls.cache = cache
    return cache


def reset_response_cache() -> None:
    """Clear the current thread's request-level cache (call per task)."""
    _response_cache_tls.cache = {}


def _response_cache_key(data: dict) -> Optional[str]:
    try:
        blob = json.dumps(data, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        return None
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _response_is_cacheable(response: dict) -> bool:
    """A normalized response is cacheable iff it is a valid assistant turn
    (has text content OR at least one named tool_call)."""
    try:
        msg = response["choices"][0]["message"]
    except (KeyError, IndexError, TypeError):
        return False
    content = msg.get("content")
    has_text = bool(content and str(content).strip())
    has_named_tool = any(
        (tc.get("function") or {}).get("name")
        for tc in (msg.get("tool_calls") or [])
    )
    return has_text or has_named_tool


# ---- Response normalization ------------------------------------------------


def _normalize_anthropic_response(response: dict) -> dict:
    """Convert an Anthropic-format response to OpenAI-compatible format if needed."""
    if not (response.get("type") == "message" and isinstance(response.get("content"), list)):
        return response

    content_text = ""
    tool_calls = []
    for block in response.get("content", []):
        if block.get("type") == "text":
            content_text += block.get("text", "")
        elif block.get("type") == "tool_use":
            tool_calls.append(
                {
                    "id": block.get("id"),
                    "type": "function",
                    "function": {
                        "name": block.get("name"),
                        "arguments": json.dumps(block.get("input", {})),
                    },
                }
            )

    message = {"role": response.get("role", "assistant"), "content": content_text or None}
    if tool_calls:
        message["tool_calls"] = tool_calls

    usage = response.get("usage", {})
    otd = usage.get("output_tokens_details") or {}
    thinking_tokens = otd.get("thinking_tokens") or usage.get("thinking_tokens") or 0
    openai_usage = {
        "prompt_tokens": usage.get("input_tokens", usage.get("prompt_tokens", 0)),
        "completion_tokens": usage.get("output_tokens", usage.get("completion_tokens", 0)),
        "reasoning_tokens": thinking_tokens,
        "completion_tokens_details": {"reasoning_tokens": thinking_tokens},
    }

    return {
        "id": response.get("id", ""),
        "model": response.get("model", ""),
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": response.get("stop_reason", "stop"),
            }
        ],
        "usage": openai_usage,
    }


def _normalize_responses_api(response: dict) -> dict:
    """Responses API response ({"object":"response","output":[...]}) -> OpenAI choices."""
    content_text = ""
    tool_calls = []
    reasoning_text = ""
    for item in response.get("output", []) or []:
        it = item.get("type")
        if it == "message":
            for part in item.get("content", []) or []:
                if part.get("type") in ("output_text", "text"):
                    content_text += part.get("text", "")
        elif it == "function_call":
            args = item.get("arguments")
            if not isinstance(args, str):
                args = json.dumps(args or {})
            tool_calls.append(
                {
                    "id": item.get("call_id") or item.get("id"),
                    "type": "function",
                    "function": {"name": item.get("name"), "arguments": args},
                }
            )
        elif it == "reasoning":
            for s in item.get("summary", []) or []:
                if isinstance(s, dict):
                    reasoning_text += s.get("text", "")
                elif isinstance(s, str):
                    reasoning_text += s

    message = {"role": "assistant", "content": content_text or None}
    if tool_calls:
        message["tool_calls"] = tool_calls
    if reasoning_text:
        message["reasoning"] = reasoning_text

    usage = response.get("usage", {}) or {}
    otd = usage.get("output_tokens_details") or {}
    rt = otd.get("reasoning_tokens") or 0
    openai_usage = {
        "prompt_tokens": usage.get("input_tokens", usage.get("prompt_tokens", 0)),
        "completion_tokens": usage.get("output_tokens", usage.get("completion_tokens", 0)),
        "reasoning_tokens": rt,
        "completion_tokens_details": {"reasoning_tokens": rt},
    }
    return {
        "id": response.get("id", ""),
        "model": response.get("model", ""),
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": response.get("finish_reason") or "stop",
            }
        ],
        "usage": openai_usage,
    }


# ---- Cost / usage ----------------------------------------------------------


def get_response_cost(usage: Optional[dict], model: str) -> float:
    """Cost in dollars from models.yaml `cost_1m_token_dollar` (0 if unpriced)."""
    if not usage:
        return 0.0
    num_prompt_token = usage.get("prompt_tokens", 0)
    num_completion_token = usage.get("completion_tokens", 0)
    price = models.get(model, {}).get("cost_1m_token_dollar", {})
    prompt_price = price.get("prompt_price", 0)
    completion_price = price.get("completion_price", 0)
    if prompt_price and completion_price:
        return (
            prompt_price * num_prompt_token + completion_price * num_completion_token
        ) / 1_000_000
    return 0.0


def get_response_usage(response: dict) -> Optional[dict]:
    usage = response.get("usage", {})
    if usage is None:
        return None
    ctd = usage.get("completion_tokens_details") or {}
    reasoning_tokens = usage.get("reasoning_tokens") or ctd.get("reasoning_tokens") or 0
    return {
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "reasoning_tokens": reasoning_tokens,
    }


# ---- Message formatting ----------------------------------------------------


def to_tau2_messages(
    messages: list[dict], ignore_roles: set[str] = set()
) -> list[Message]:
    """Convert a list of dict messages to Tau2 messages."""
    tau2_messages = []
    for message in messages:
        role = message["role"]
        if role in ignore_roles:
            continue
        if role == "user":
            tau2_messages.append(UserMessage(**message))
        elif role == "assistant":
            tau2_messages.append(AssistantMessage(**message))
        elif role == "tool":
            tau2_messages.append(ToolMessage(**message))
        elif role == "system":
            tau2_messages.append(SystemMessage(**message))
        else:
            raise ValueError(f"Unknown message type: {role}")
    return tau2_messages


def format_messages(messages: list[Message]) -> list[dict]:
    """Convert Tau2 messages to OpenAI-chat dict messages (gateway request body)."""
    messages_formatted = []
    for message in messages:
        if isinstance(message, UserMessage):
            messages_formatted.append({"role": "user", "content": message.content})
        elif isinstance(message, AssistantMessage):
            tool_calls = None
            if message.is_tool_call():
                tool_calls = [
                    {
                        "id": tc.id,
                        "name": tc.name,
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments),
                        },
                        "type": "function",
                    }
                    for tc in message.tool_calls
                ]
            messages_formatted.append(
                {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": tool_calls,
                }
            )
            # interleaved thinking content, if the model produced any
            if message.raw_data is not None and message.raw_data.get("message") is not None:
                reasoning_content = message.raw_data["message"].get("reasoning_content")
                if reasoning_content:
                    messages_formatted[-1]["reasoning_content"] = reasoning_content
        elif isinstance(message, ToolMessage):
            # tau2 ToolMessage has no `name` field (only id); mirror the
            # historical to_litellm_messages shape.
            messages_formatted.append(
                {
                    "role": "tool",
                    "content": message.content,
                    "tool_call_id": message.id,
                }
            )
        elif isinstance(message, SystemMessage):
            messages_formatted.append({"role": "system", "content": message.content})
    return messages_formatted


# Backwards-compatible alias (older call sites used the litellm-era name).
to_litellm_messages = format_messages


def to_claude_think_official(
    messages_formatted: list[dict], messages: list[Message]
) -> list[dict]:
    try:
        for i, (formatted_msg, original_msg) in enumerate(
            zip(messages_formatted, messages)
        ):
            if formatted_msg.get("role") != "assistant":
                continue
            if not hasattr(original_msg, "raw_data") or original_msg.raw_data is None:
                continue
            raw_message = original_msg.raw_data.get("message", {})
            reasoning_content = raw_message.get("reasoning_content") or raw_message.get(
                "reasoning"
            )
            signature = raw_message.get("signature")
            if reasoning_content:
                messages_formatted[i]["reasoning_content"] = reasoning_content
            if signature:
                messages_formatted[i]["signature"] = signature
    except Exception:
        import traceback

        traceback.print_exc()
    return messages_formatted


def to_deepseek_think_official(
    messages_formatted: list[dict], messages: list[Message]
) -> list[dict]:
    try:
        for i, (formatted_msg, original_msg) in enumerate(
            zip(messages_formatted, messages)
        ):
            if formatted_msg.get("role") != "assistant":
                continue
            if not hasattr(original_msg, "raw_data") or original_msg.raw_data is None:
                continue
            reasoning_content = original_msg.raw_data.get("message", {}).get(
                "reasoning_content", None
            ) or original_msg.raw_data.get("message", {}).get("reasoning", None)
            if reasoning_content:
                messages_formatted[i]["reasoning_content"] = reasoning_content
    except Exception:
        import traceback

        traceback.print_exc()
    return messages_formatted


# ---- OpenAI -> Anthropic / Responses request adapters ----------------------


def _openai_tools_to_anthropic(tools: list) -> list:
    out = []
    for t in tools or []:
        fn = t.get("function", t)
        out.append(
            {
                "name": fn.get("name"),
                "description": fn.get("description", ""),
                "input_schema": fn.get("parameters")
                or {"type": "object", "properties": {}},
            }
        )
    return out


def _openai_messages_to_anthropic(messages_formatted: list) -> list:
    out = []
    for m in messages_formatted:
        role = m.get("role")
        if role == "system":
            continue
        if role == "user":
            out.append({"role": "user", "content": m.get("content") or ""})
        elif role == "assistant":
            blocks = []
            reasoning = m.get("reasoning_content")
            if reasoning:
                tb = {"type": "thinking", "thinking": reasoning}
                if m.get("signature"):
                    tb["signature"] = m["signature"]
                blocks.append(tb)
            content = m.get("content")
            if content:
                blocks.append({"type": "text", "text": content})
            for tc in m.get("tool_calls") or []:
                fn = tc.get("function", {})
                raw_args = fn.get("arguments")
                try:
                    parsed = (
                        json.loads(raw_args)
                        if isinstance(raw_args, str)
                        else (raw_args or {})
                    )
                except Exception:
                    parsed = {}
                blocks.append(
                    {
                        "type": "tool_use",
                        "id": tc.get("id"),
                        "name": fn.get("name") or tc.get("name"),
                        "input": parsed,
                    }
                )
            if not blocks:
                blocks = [{"type": "text", "text": ""}]
            out.append({"role": "assistant", "content": blocks})
        elif role == "tool":
            block = {
                "type": "tool_result",
                "tool_use_id": m.get("tool_call_id"),
                "content": m.get("content") or "",
            }
            if out and out[-1]["role"] == "user" and isinstance(out[-1]["content"], list):
                out[-1]["content"].append(block)
            else:
                out.append({"role": "user", "content": [block]})
    return out


def _openai_tools_to_responses(tools: list) -> list:
    out = []
    for t in tools or []:
        fn = t.get("function", t)
        out.append(
            {
                "type": "function",
                "name": fn.get("name"),
                "description": fn.get("description", ""),
                "parameters": fn.get("parameters")
                or {"type": "object", "properties": {}},
            }
        )
    return out


def _openai_messages_to_responses(messages_formatted: list) -> tuple:
    instructions_parts = []
    inp = []
    for m in messages_formatted:
        role = m.get("role")
        if role == "system":
            if m.get("content"):
                instructions_parts.append(m["content"])
        elif role == "user":
            inp.append({"role": "user", "content": m.get("content") or ""})
        elif role == "assistant":
            if m.get("content"):
                inp.append({"role": "assistant", "content": m["content"]})
            for tc in m.get("tool_calls") or []:
                fn = tc.get("function", {})
                args = fn.get("arguments")
                if not isinstance(args, str):
                    args = json.dumps(args or {})
                inp.append(
                    {
                        "type": "function_call",
                        "call_id": tc.get("id"),
                        "name": fn.get("name") or tc.get("name"),
                        "arguments": args,
                    }
                )
        elif role == "tool":
            out_content = m.get("content")
            if not isinstance(out_content, str):
                out_content = json.dumps(out_content) if out_content is not None else ""
            inp.append(
                {
                    "type": "function_call_output",
                    "call_id": m.get("tool_call_id"),
                    "output": out_content,
                }
            )
    instructions = "\n\n".join(instructions_parts) if instructions_parts else None
    return instructions, inp


def _build_responses_request(data: dict, enable_think: bool) -> dict:
    """OpenAI chat request body -> Responses API body (gpt-5 think+tools path).

    think is controlled via reasoning.effort; gpt-5 reasoning models reject a
    non-default temperature, so we do not send one.
    """
    instructions, inp = _openai_messages_to_responses(data.get("messages", []))
    new_data = {"model": data["model"], "input": inp, "stream": False}
    if instructions:
        new_data["instructions"] = instructions
    effort = data.pop("reasoning_effort", None) or "medium"
    if enable_think:
        new_data["reasoning"] = {"effort": effort}
    if data.get("tools"):
        new_data["tools"] = _openai_tools_to_responses(data["tools"])
        tc = data.get("tool_choice")
        if isinstance(tc, str) and tc in ("auto", "required", "none"):
            new_data["tool_choice"] = tc
    mx = data.get("max_tokens") or data.get("max_output_tokens")
    if mx:
        new_data["max_output_tokens"] = mx
    return new_data


def _is_responses_model(model: str, api_format: Optional[str]) -> bool:
    if api_format == "responses":
        return True
    return bool(re.search(r"(openai|azure)\.gpt-5\.5", model or ""))


def kwargs_adapter(
    data: dict,
    enable_think: bool,
    messages: list,
    api_format: Optional[str] = None,
) -> dict:
    if _is_responses_model(data.get("model", ""), api_format):
        return _build_responses_request(data, enable_think)
    # Channel-prefixed claude models (e.g. "aws.claude-*") use Anthropic's native
    # API format and need system extracted to a top-level parameter. Bare claude
    # models keep system in the messages array. `anthropic.claude-*` = gateway
    # direct-to-Anthropic returning OpenAI-chat {"choices":...} -> openai-compat.
    is_channel_claude = (
        "claude" in data["model"]
        and "." in data["model"].split("claude")[0]
        and not data["model"].startswith("anthropic.")
    )
    if is_channel_claude:
        system_msgs = [m for m in data["messages"] if m.get("role") == "system"]
        if system_msgs:
            data["system"] = system_msgs[0]["content"]
            data["messages"] = [m for m in data["messages"] if m.get("role") != "system"]
        claude_effort = data.pop("reasoning_effort", None) or "medium"
        if not enable_think:
            data["thinking"] = {"type": "disabled"}
        else:
            data["thinking"] = {"type": "adaptive"}
            data["output_config"] = {"effort": claude_effort}
            data["messages"] = to_claude_think_official(data["messages"], messages)
        data["messages"] = _openai_messages_to_anthropic(data["messages"])
        if data.get("tools"):
            data["tools"] = _openai_tools_to_anthropic(data["tools"])
        else:
            data.pop("tools", None)
        tc = data.get("tool_choice")
        if isinstance(tc, str):
            mapped = {
                "auto": {"type": "auto"},
                "required": {"type": "any"},
                "any": {"type": "any"},
            }.get(tc)
            if mapped:
                data["tool_choice"] = mapped
            else:
                data.pop("tool_choice", None)
        data.pop("temperature", None)
    elif "deepseek" in data["model"]:
        if enable_think:
            data["messages"] = to_deepseek_think_official(data["messages"], messages)
    else:
        # bare claude on openai-compat: reasoning model rejects temperature.
        if "claude" in data["model"]:
            data.pop("temperature", None)
        if not enable_think:
            if data.get("model", "") == "gpt-5":
                data["reasoning_effort"] = "minimal"
            elif "reasoning_effort" in data:
                data.pop("reasoning_effort")
    return data


# ---- Message validation (tau2-specific) ------------------------------------


def validate_message(message: Message) -> None:
    """Validate the message."""

    def has_text_content(message: Message) -> bool:
        return message.content is not None and bool(message.content.strip())

    def has_content_or_tool_calls(message: ParticipantMessageBase) -> bool:
        return message.has_content() or message.is_tool_call()

    if isinstance(message, SystemMessage):
        assert has_text_content(message), (
            f"System message must have content. got {message}"
        )
    if isinstance(message, ParticipantMessageBase):
        assert has_content_or_tool_calls(message), (
            f"Message must have content or tool calls. got {message}"
        )


def validate_message_history(messages: list[Message]) -> None:
    """Validate the message history."""
    for message in messages:
        validate_message(message)


# ---- Debug logging (tau2-specific) -----------------------------------------


def set_llm_log_dir(log_dir: Optional[Path | str]) -> None:
    """Set the directory where LLM debug logs should be written."""
    if isinstance(log_dir, str):
        log_dir = Path(log_dir)
    llm_log_dir.set(log_dir)


def set_llm_log_mode(mode: str) -> None:
    """Set the LLM debug logging mode ('all' or 'latest')."""
    if mode not in ("all", "latest"):
        raise ValueError(f"Invalid LLM log mode: {mode}. Must be 'all' or 'latest'")
    llm_log_mode.set(mode)


def _format_messages_for_logging(messages: list[dict]) -> list[dict]:
    """Split message content on newlines for readable debug logs."""
    formatted = []
    for msg in messages:
        msg_copy = msg.copy()
        if "content" in msg_copy and isinstance(msg_copy["content"], str):
            content_lines = msg_copy["content"].split("\n")
            if len(content_lines) > 1:
                msg_copy["content"] = content_lines
        formatted.append(msg_copy)
    return formatted


def _write_llm_log(
    request_data: dict, response_data: dict, call_name: Optional[str] = None
) -> None:
    """Write an LLM call log to file if a log directory is set."""
    log_dir = llm_log_dir.get()
    if log_dir is None:
        return
    log_dir.mkdir(parents=True, exist_ok=True)
    current_log_mode = llm_log_mode.get()
    if current_log_mode == "latest" and call_name:
        pattern = f"*_{call_name}_*.json"
        for existing_file in list(log_dir.glob(pattern)):
            try:
                existing_file.unlink()
            except FileNotFoundError:
                pass
    call_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    if call_name:
        log_file = log_dir / f"{timestamp}_{call_name}_{call_id}.json"
    else:
        log_file = log_dir / f"{timestamp}_{call_id}.json"
    call_data = {
        "call_id": call_id,
        "call_name": call_name,
        "timestamp": datetime.now().isoformat(),
        "request": request_data,
        "response": response_data,
    }
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(call_data, f, indent=2)


def _parse_tool_call_arguments(arguments: Optional[str]) -> dict[str, Any]:
    """Parse provider-returned tool arguments into a dictionary."""
    if arguments is None or not str(arguments).strip():
        return {}
    if isinstance(arguments, dict):
        return arguments

    parsers = (json.loads, ast.literal_eval, yaml.safe_load)
    errors: list[str] = []
    for parser in parsers:
        try:
            parsed = parser(arguments)
        except Exception as exc:
            errors.append(f"{parser.__module__}.{parser.__name__}: {exc}")
            continue
        if parsed is None:
            return {}
        if isinstance(parsed, dict):
            return parsed
        errors.append(
            f"{parser.__module__}.{parser.__name__}: expected dict, "
            f"got {type(parsed).__name__}"
        )

    snippet = str(arguments)[:200].replace("\n", "\\n")
    raise ValueError(
        "Could not parse tool call arguments as a dict. "
        f"arguments={snippet!r}; errors={errors}"
    )


# ---- The single collection point for every LLM call ------------------------


def generate(
    model: str,
    messages: list[Message],
    tools: Optional[list[Tool]] = None,
    tool_choice: Optional[str] = None,
    call_name: Optional[str] = None,
    enable_think: bool = False,
    **kwargs: Any,
) -> UserMessage | AssistantMessage:
    """Generate a response from *model* via the model gateway.

    Args:
        model: The model name (must exist in tau2.config.models / models.yaml).
        messages: The messages to send.
        tools: The tools to expose.
        tool_choice: The tool choice ("auto" by default when tools are present).
        call_name: Optional label used for debug-log filenames.
        enable_think: Whether to enable think mode. Only the agent passes True;
            the user simulator and NL-assertion judge leave it False (non-think).
        **kwargs: Additional arguments. Only `temperature` is forwarded to the
            request body (all other per-model params come from models.yaml).
    """
    validate_message_history(messages)
    if kwargs.get("num_retries") is None:
        kwargs["num_retries"] = DEFAULT_MAX_RETRIES

    messages_formatted = format_messages(messages)
    tools_schema = [tool.openai_schema for tool in tools] if tools else None
    if tools_schema and tool_choice is None:
        tool_choice = "auto"

    # Prepare request data for logging (before adapter mutates the body)
    formatted_messages_for_log = _format_messages_for_logging(messages_formatted)
    request_data = {
        "model": model,
        "messages": formatted_messages_for_log,
        "tools": tools_schema,
        "tool_choice": tool_choice,
        "enable_think": enable_think,
        "kwargs": {
            k: str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v
            for k, v in kwargs.items()
        },
    }
    request_timestamp = datetime.now().isoformat()
    start_time = time.perf_counter()

    if model not in models:
        raise KeyError(
            f"Model '{model}' not found in models.yaml. Available: "
            f"{list(models.keys())}. Set TAU2_MODEL_CONFIG_PATH to your config."
        )

    data = {
        "model": model,
        "messages": messages_formatted,
        "stream": False,
        "temperature": kwargs.get("temperature"),
        "tools": tools_schema,
        "tool_choice": tool_choice,
    }
    model_config = models[model]
    base_url = model_config["base_url"]
    headers = model_config["headers"]
    api_config = {
        k: v
        for k, v in model_config.items()
        if k not in ("base_url", "headers", "max_input_tokens", "name", "api_format")
    }
    api_format = model_config.get("api_format")
    data.update(api_config)
    data = kwargs_adapter(data, enable_think, messages, api_format)

    # Optional request-level cache (disabled by default)
    cache_key = _response_cache_key(data) if _RESPONSE_CACHE_ENABLED else None
    _resp_cache = _get_response_cache() if cache_key is not None else None
    cached_response = _resp_cache.get(cache_key) if cache_key is not None else None

    response = None
    max_retries = 9
    retry_delay_base = 2
    try:
        for attempt in range(max_retries + 1):
            retry_delay = min(60.0, retry_delay_base * (2**attempt)) * (
                0.5 + random.random() * 0.5
            )
            if cached_response is not None:
                response = cached_response
                break
            try:
                http_response = requests.post(
                    base_url, json=data, headers=headers, timeout=(10, 600)
                )
                if http_response.status_code == 200:
                    try:
                        body = http_response.json()
                    except ValueError:
                        body = None
                    if not isinstance(body, dict):
                        if attempt < max_retries:
                            logger.warning(
                                f"200 but empty/invalid JSON body, retry "
                                f"{attempt + 1}/{max_retries + 1} in {retry_delay:.1f}s..."
                            )
                            time.sleep(retry_delay)
                            continue
                        raise ValueError(
                            f"200 but empty/invalid JSON body after {max_retries} retries"
                        )
                    if isinstance(body, dict) and (
                        "choices" in body
                        or body.get("type") == "message"
                        or body.get("object") == "response"
                    ):
                        if body.get("object") == "response":
                            response = _normalize_responses_api(body)
                        else:
                            response = _normalize_anthropic_response(body)
                        break
                    if attempt < max_retries:
                        logger.warning(
                            f"200 OK but no 'choices' (likely proxy-wrapped upstream "
                            f"error), attempt {attempt + 1}/{max_retries + 1}, retrying "
                            f"in {retry_delay:.1f}s. Body keys: "
                            f"{list(body.keys()) if isinstance(body, dict) else type(body)}"
                        )
                        time.sleep(retry_delay)
                        continue
                    raise ValueError(
                        f"200 OK but no 'choices' after {max_retries} retries. Body: {body}"
                    )
                # 4xx client errors (except 408/429) are deterministic.
                if (
                    400 <= http_response.status_code < 500
                    and http_response.status_code not in (408, 429)
                ):
                    _rt = http_response.text.lower()
                    _routing_miss = any(
                        s in _rt
                        for s in (
                            "access to bedrock",
                            "error 002",
                            "claude on azure",
                            "deployment request could not be completed",
                            "555420",
                        )
                    )
                    if (
                        not _routing_miss
                        and "claude" in data.get("model", "")
                        and "routify_response" in _rt
                        and '"success":false' in _rt
                    ):
                        _routing_miss = True
                    if _routing_miss and attempt < max_retries:
                        logger.warning(
                            f"gateway backend-access {http_response.status_code}, retry "
                            f"{attempt + 1}/{max_retries + 1} in {retry_delay:.1f}s..."
                        )
                        time.sleep(retry_delay)
                        continue
                    logger.error(
                        f"Non-retryable {http_response.status_code}: "
                        f"{http_response.text[:300]}"
                    )
                    raise ValueError(
                        f"Non-retryable HTTP {http_response.status_code}: "
                        f"{http_response.text[:300]}"
                    )
                if attempt < max_retries:
                    logger.warning(
                        f"API returned {http_response.status_code}, attempt "
                        f"{attempt + 1}/{max_retries + 1}, retrying in {retry_delay:.1f}s..."
                    )
                    time.sleep(retry_delay)
                else:
                    http_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                if attempt < max_retries:
                    logger.warning(
                        f"Request exception, attempt {attempt + 1}/{max_retries + 1}, "
                        f"retrying in {retry_delay:.1f}s... Error: {e}"
                    )
                    time.sleep(retry_delay)
                else:
                    raise e
        if cache_key is not None and response is not None and _response_is_cacheable(
            response
        ):
            _resp_cache[cache_key] = response
    except Exception as e:
        logger.error(e)
        raise e

    generation_time_seconds = time.perf_counter() - start_time
    usage = get_response_usage(response)
    cost = get_response_cost(usage, model)

    try:
        response_choice = response["choices"][0]
    except (KeyError, IndexError, TypeError) as e:
        logger.error(
            f"Full response: "
            f"{json.dumps(response, ensure_ascii=False, indent=2) if isinstance(response, dict) else response}"
        )
        raise ValueError(f"Invalid API response format: {e}") from e

    finish_reason = response_choice.get("finish_reason")
    if finish_reason == "length":
        logger.warning("Output might be incomplete due to token limit!")

    assert response_choice["message"]["role"] == "assistant", (
        "The response should be an assistant message"
    )
    content = response_choice["message"].get("content")
    raw_tool_calls = response_choice["message"].get("tool_calls") or []
    # Skip nameless tool calls (reasoning models occasionally emit them).
    tool_calls = [
        ToolCall(
            id=tc.get("id"),
            name=tc.get("function", {}).get("name"),
            arguments=_parse_tool_call_arguments(tc.get("function", {}).get("arguments")),
        )
        for tc in raw_tool_calls
        if tc.get("function", {}).get("name")
    ]
    tool_calls = tool_calls or None

    message = AssistantMessage(
        role="assistant",
        content=content,
        tool_calls=tool_calls,
        cost=cost,
        usage=usage,
        raw_data=response_choice,
        generation_time_seconds=generation_time_seconds,
    )

    response_data = {
        "timestamp": datetime.now().isoformat(),
        "content": content,
        "tool_calls": [tc.model_dump() for tc in tool_calls] if tool_calls else None,
        "cost": cost,
        "usage": usage,
        "generation_time_seconds": generation_time_seconds,
    }
    request_data["timestamp"] = request_timestamp
    _write_llm_log(request_data, response_data, call_name=call_name)

    return message


def get_cost(messages: list[Message]) -> tuple[float, float] | None:
    """Get the (agent, user) cost of the interaction. None if any cost missing."""
    agent_cost = 0
    user_cost = 0
    for message in messages:
        if isinstance(message, ToolMessage):
            continue
        if message.cost is not None:
            if isinstance(message, AssistantMessage):
                agent_cost += message.cost
            elif isinstance(message, UserMessage):
                user_cost += message.cost
        else:
            logger.warning(f"Message {message.role}: {message.content} has no cost")
            return None
    return agent_cost, user_cost


def get_token_usage(messages: list[Message]) -> dict:
    """Get token usage of the interaction between the agent and the user."""
    usage = {"completion_tokens": 0, "prompt_tokens": 0}
    for message in messages:
        if isinstance(message, ToolMessage):
            continue
        if message.usage is None:
            logger.warning(f"Message {message.role}: {message.content} has no usage")
            continue
        usage["completion_tokens"] += message.usage["completion_tokens"]
        usage["prompt_tokens"] += message.usage["prompt_tokens"]
    return usage


def extract_json_from_llm_response(response: str) -> str:
    """Extract JSON from an LLM response, handling markdown code blocks."""
    pattern = r"```(?:json)?\s*([\s\S]*?)```"
    match = re.search(pattern, response)
    if match:
        return match.group(1).strip()
    start = response.find("{")
    end = response.rfind("}")
    if start != -1 and end != -1 and end > start:
        return response[start : end + 1]
    return response
