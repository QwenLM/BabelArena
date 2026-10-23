import hashlib
import json
import random
import re
import threading
import time
from typing import Any, Optional

from loguru import logger
import requests


from vita.config import (
    models,
    DEFAULT_MAX_RETRIES,
)
from vita.data_model.message import (
    AssistantMessage,
    Message,
    SystemMessage,
    ToolCall,
    ToolMessage,
    UserMessage,
)
from vita.environment.tool import Tool


# ---- Request-level response cache ------------------------------------------
# run.py's failure retry rebuilds and reruns a whole task from turn 0, so LLM
# calls that already succeeded (and were already billed) get replayed with a
# byte-identical request body -- about a third of billed calls. Cache successful
# responses keyed on the final request body: a rerun within the same task reuses
# the cached response instead of hitting the API. temperature=0 plus locally
# deterministic tool execution means an identical conversation prefix rebuilds an
# identical request body, so a replayed trajectory matches the original exactly.
# If the prefix does change, the lookup simply misses and a real request goes out.
#
# The cache must be thread-local: evaluation runs tasks concurrently in a
# ThreadPoolExecutor, each task entirely inside one worker thread. A single
# global dict would let one task's reset evict entries another task is using.
_RESPONSE_CACHE_ENABLED = True
_response_cache_tls = threading.local()


def _get_response_cache() -> dict:
    cache = getattr(_response_cache_tls, "cache", None)
    if cache is None:
        cache = {}
        _response_cache_tls.cache = cache
    return cache


def reset_response_cache() -> None:
    """Clear this thread's request-level cache. Called before each task starts,
    which is what keeps the cache scoped per task."""
    _response_cache_tls.cache = {}


def _response_cache_key(data: dict) -> Optional[str]:
    """Stable key derived from the final request body; None when it is not
    serialisable, which degrades to not caching."""
    try:
        blob = json.dumps(data, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        return None
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _response_is_cacheable(response: dict) -> bool:
    """Whether a normalised response is a valid, reusable assistant turn.

    Reasoning models occasionally emit an "empty turn": thinking only, with no
    content and no named tool_call. Downstream AssistantMessage.validate()
    rejects it and raises. Such a response must never enter the cache -- if it
    did, every retry of that task would hit the cache and replay the same dead
    turn, so all retries would fail identically and the (task, trial) would
    never land. Leaving it uncached lets a retry resample just that turn while
    the successful prefix still hits the cache, so no tokens are wasted.
    """
    try:
        msg = response['choices'][0]['message']
    except (KeyError, IndexError, TypeError):
        return False
    content = msg.get('content')
    has_text = bool(content and str(content).strip())
    has_named_tool = any(
        (tc.get('function') or {}).get('name')
        for tc in (msg.get('tool_calls') or [])
    )
    return has_text or has_named_tool


class DictToObject:
    """
    Convert dictionary to object with attribute access
    Usage:
    response_obj = DictToObject(response)
    print(response_obj.choices[0].message.content)  # Instead of response["choices"][0]["message"]["content"]
    """
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DictToObject(value))
            elif isinstance(value, list):
                setattr(self, key, [DictToObject(item) if isinstance(item, dict) else item for item in value])
            else:
                setattr(self, key, value)

    def to_dict(self):
        """Convert object back to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, DictToObject):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [item.to_dict() if isinstance(item, DictToObject) else item for item in value]
            else:
                result[key] = value
        return result


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
            tool_calls.append({
                "id": block.get("id"),
                "type": "function",
                "function": {
                    "name": block.get("name"),
                    "arguments": json.dumps(block.get("input", {})),
                },
            })

    message = {
        "role": response.get("role", "assistant"),
        "content": content_text or None,
    }
    if tool_calls:
        message["tool_calls"] = tool_calls

    usage = response.get("usage", {})
    # Claude (adaptive think) reports thinking volume under
    # output_tokens_details.thinking_tokens; pass it through as reasoning_tokens
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
        "choices": [{"index": 0, "message": message, "finish_reason": response.get("stop_reason", "stop")}],
        "usage": openai_usage,
    }


def get_response_cost(usage, model) -> float:
    num_prompt_token = usage["prompt_tokens"]
    num_completion_token = usage["completion_tokens"]
    prompt_price = models.get(model, {}).get("cost_1m_token_dollar",{}).get("prompt_price", 0)
    completion_price = models.get(model, {}).get("cost_1m_token_dollar",{}).get("completion_price", 0)
    if prompt_price and completion_price:
        return (prompt_price * num_prompt_token + completion_price * num_completion_token) / 1000000
    else:
        return 0.0


def get_response_usage(response) -> Optional[dict]:
    usage = response.get("usage", {})
    if usage is None:
        return None
    # Keep reasoning_tokens (present only on thinking models) so a run can be
    # audited afterwards for whether the model actually reasoned.
    ctd = usage.get("completion_tokens_details") or {}
    reasoning_tokens = usage.get("reasoning_tokens") or ctd.get("reasoning_tokens") or 0
    return {
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "reasoning_tokens": reasoning_tokens,
    }


def format_messages(messages: list[Message]) -> list[dict]:
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
            # add interleaved thinking content if exists
            if message.raw_data is not None and message.raw_data.get("message") is not None:
                reasoning_content = message.raw_data["message"].get("reasoning_content")
                if reasoning_content:
                    messages_formatted[-1]["reasoning_content"] = reasoning_content
        elif isinstance(message, ToolMessage):
            messages_formatted.append(
                {
                    "role": "tool",
                    "content": message.content,
                    "tool_call_id": message.id,
                    "name": message.name,
                }
            )
        elif isinstance(message, SystemMessage):
            messages_formatted.append({"role": "system", "content": message.content})
    return messages_formatted


def to_claude_think_official(messages_formatted: list[dict], messages: list[Message]) -> list[dict]:
    try:
        for i, (formatted_msg, original_msg) in enumerate(zip(messages_formatted, messages)):
            if formatted_msg.get("role") != "assistant":
                continue

            if not hasattr(original_msg, 'raw_data') or original_msg.raw_data is None:
                continue

            raw_message = original_msg.raw_data.get("message", {})

            # Extract reasoning content and signature
            reasoning_content = raw_message.get("reasoning_content") or raw_message.get("reasoning")
            signature = raw_message.get("signature")
            if reasoning_content:
                messages_formatted[i]["reasoning_content"] = reasoning_content
            if signature:
                messages_formatted[i]["signature"] = signature

    except Exception as e:
        import traceback
        traceback.print_exc()

    return messages_formatted


def to_deepseek_think_official(messages_formatted: list[dict], messages: list[Message]) -> list[dict]:
    try:
        for i, (formatted_msg, original_msg) in enumerate(zip(messages_formatted, messages)):
            if formatted_msg.get("role") != "assistant":
                continue

            if not hasattr(original_msg, 'raw_data') or original_msg.raw_data is None:
                continue

            reasoning_content = original_msg.raw_data.get("message", {}).get("reasoning_content", None) or \
                               original_msg.raw_data.get("message", {}).get("reasoning", None)

            if reasoning_content:
                messages_formatted[i]["reasoning_content"] = reasoning_content

    except Exception as e:
        import traceback
        traceback.print_exc()

    return messages_formatted


def _openai_tools_to_anthropic(tools: list) -> list:
    """OpenAI tool schema -> Anthropic tool schema (name/description/input_schema)。"""
    out = []
    for t in tools or []:
        fn = t.get("function", t)  # tolerate an already-bare function body
        out.append({
            "name": fn.get("name"),
            "description": fn.get("description", ""),
            "input_schema": fn.get("parameters") or {"type": "object", "properties": {}},
        })
    return out


def _openai_messages_to_anthropic(messages_formatted: list) -> list:
    """OpenAI-format messages -> Anthropic messages (content-block form).

    - system has already been lifted to the top-level system parameter, so skip it;
    - assistant tool_calls -> tool_use blocks; a reasoning_content/signature pair
      (thinking models) additionally emits a thinking block;
    - role=tool results -> tool_result blocks inside the following user message
      (consecutive results merge into one user message).
    """
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
            for tc in (m.get("tool_calls") or []):
                fn = tc.get("function", {})
                raw_args = fn.get("arguments")
                try:
                    parsed = json.loads(raw_args) if isinstance(raw_args, str) else (raw_args or {})
                except Exception:
                    parsed = {}
                blocks.append({
                    "type": "tool_use",
                    "id": tc.get("id"),
                    "name": fn.get("name") or tc.get("name"),
                    "input": parsed,
                })
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
    """OpenAI chat tool schema -> Responses API tool schema (name/description/
    parameters flattened)."""
    out = []
    for t in tools or []:
        fn = t.get("function", t)  # tolerate an already-bare function body
        out.append({
            "type": "function",
            "name": fn.get("name"),
            "description": fn.get("description", ""),
            "parameters": fn.get("parameters") or {"type": "object", "properties": {}},
        })
    return out


def _openai_messages_to_responses(messages_formatted: list) -> tuple:
    """OpenAI-format messages -> (instructions, Responses input list).

    - system -> top-level instructions (several are concatenated);
    - user   -> {"role":"user","content":...};
    - assistant text -> {"role":"assistant","content":...};
      assistant.tool_calls -> {"type":"function_call","call_id","name","arguments"(str)};
    - role=tool -> {"type":"function_call_output","call_id","output"}。
    Multi-turn is stateless in practice: the reasoning item does not need to be
    echoed back for the conversation to continue.
    """
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
            for tc in (m.get("tool_calls") or []):
                fn = tc.get("function", {})
                args = fn.get("arguments")
                if not isinstance(args, str):
                    args = json.dumps(args or {})
                inp.append({
                    "type": "function_call",
                    "call_id": tc.get("id"),
                    "name": fn.get("name") or tc.get("name"),
                    "arguments": args,
                })
        elif role == "tool":
            out_content = m.get("content")
            if not isinstance(out_content, str):
                out_content = json.dumps(out_content) if out_content is not None else ""
            inp.append({
                "type": "function_call_output",
                "call_id": m.get("tool_call_id"),
                "output": out_content,
            })
    instructions = "\n\n".join(instructions_parts) if instructions_parts else None
    return instructions, inp


def _build_responses_request(data: dict, enable_think: bool) -> dict:
    """Convert an OpenAI chat request body into a Responses API request body.

    Sent to the same /chat/completions URL; the gateway routes to the Responses
    backend based on the model name and the shape of the body.
    Thinking is controlled by reasoning.effort. Reasoning models reject a
    non-default temperature, so temperature is omitted.
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


def _normalize_responses_api(response: dict) -> dict:
    """Responses API reply ({"object":"response","output":[...]}) -> OpenAI
    choices form."""
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
            tool_calls.append({
                "id": item.get("call_id") or item.get("id"),
                "type": "function",
                "function": {"name": item.get("name"), "arguments": args},
            })
        elif it == "reasoning":
            # Reasoning models usually return no CoT (summary=[]); when they do,
            # join it so it can be inspected in raw_data.
            for s in item.get("summary", []) or []:
                if isinstance(s, dict):
                    reasoning_text += s.get("text", "")
                elif isinstance(s, str):
                    reasoning_text += s

    message = {"role": "assistant", "content": content_text or None}
    if tool_calls:
        message["tool_calls"] = tool_calls
    if reasoning_text:
        message["reasoning"] = reasoning_text  # cot_dump reads raw_data.message.reasoning

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
        "choices": [{"index": 0, "message": message,
                     "finish_reason": response.get("finish_reason") or "stop"}],
        "usage": openai_usage,
    }


def _is_responses_model(model: str, api_format: Optional[str]) -> bool:
    """Whether to use the Responses API: either api_format=responses is set
    explicitly, or the model name matches a known Responses-backed alias."""
    if api_format == "responses":
        return True
    return bool(re.search(r"(openai|azure)\.gpt-5\.5", model or ""))


def kwargs_adapter(data: dict, enable_think: False, messages: list, api_format: Optional[str] = None) -> dict:
    if _is_responses_model(data.get("model", ""), api_format):
        return _build_responses_request(data, enable_think)
    # Channel-prefixed claude models (e.g. "aws.claude-*") use Anthropic's native
    # API format via DashScope and need system extracted to a top-level parameter.
    # Bare claude models (e.g. "claude-opus-4-5-*") go through DashScope's
    # OpenAI-compatible endpoint and keep system in the messages array.
    # Some deployments front Anthropic directly and return OpenAI-compatible
    # {"choices":...}, which takes the openai-compat branch below. Those must not
    # go through the Anthropic-native conversion, whose thinking.adaptive /
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
        # This channel controls thinking with thinking.adaptive +
        # output_config.effort rather than thinking.enabled/budget_tokens; a
        # top-level reasoning_effort is silently ignored. Default effort medium.
        claude_effort = data.pop("reasoning_effort", None) or "medium"
        if not enable_think:
            data["thinking"] = {"type": "disabled"}
        else:
            data["thinking"] = {"type": "adaptive"}
            data["output_config"] = {"effort": claude_effort}
            data["messages"] = to_claude_think_official(data["messages"], messages)
        # OpenAI -> Anthropic native: messages become content blocks, tools become
        # input_schema, tool_choice becomes an object.
        data["messages"] = _openai_messages_to_anthropic(data["messages"])
        if data.get("tools"):
            data["tools"] = _openai_tools_to_anthropic(data["tools"])
        else:
            data.pop("tools", None)
        tc = data.get("tool_choice")
        if isinstance(tc, str):
            mapped = {"auto": {"type": "auto"}, "required": {"type": "any"}, "any": {"type": "any"}}.get(tc)
            if mapped:
                data["tool_choice"] = mapped
            else:
                data.pop("tool_choice", None)
        # This channel rejects temperature outright (reasoning_effort was popped above)
        data.pop("temperature", None)
    elif "deepseek" in data["model"]:
        if enable_think:
            data["messages"] = to_deepseek_think_official(data["messages"], messages)
    else:
        # A bare reasoning model on the openai-compat path rejects temperature
        # ("deprecated for this model"), so drop it; reasoning_effort is kept.
        if "claude" in data["model"]:
            data.pop("temperature", None)
        if not enable_think:
            if data.get("model", "") == "gpt-5":
                data["reasoning_effort"] = "minimal"
            elif "reasoning_effort" in data:
                data.pop("reasoning_effort")
    return data


def generate(
    model: str,
    messages: list[Message],
    tools: Optional[list[Tool]] = None,
    tool_choice: Optional[str] = None,
    enable_think: bool = False,
    **kwargs: Any,
) -> UserMessage | AssistantMessage:
    """
    Generate a response from the model.

    Args:
        model: The model to use.
        messages: The messages to send to the model.
        tools: The tools to use.
        tool_choice: The tool choice to use.
        enable_think: Whether to enable think mode for the agent.
        **kwargs: Additional arguments to pass to the model.

    Returns: A tuple containing the message and the cost.
    """
    try:
        if kwargs.get("num_retries") is None:
            kwargs["num_retries"] = DEFAULT_MAX_RETRIES
        messages_formatted = format_messages(messages)
        tools = [tool.openai_schema for tool in tools] if tools else None
        if tools and tool_choice is None:
            tool_choice = "auto"
        try:
            data = {
                "model": model,
                "messages": messages_formatted,
                "stream": False,
                "temperature": kwargs.get("temperature"),
                "tools": tools,
                "tool_choice": tool_choice,
            }
            model_config = models[model]
            # Extract fields used for routing but not sent to the API
            base_url = model_config["base_url"]
            headers = model_config["headers"]
            api_config = {k: v for k, v in model_config.items()
                          if k not in ("base_url", "headers", "max_input_tokens", "name", "api_format")}
            api_format = model_config.get("api_format")
            data.update(api_config)
            data = kwargs_adapter(data, enable_think, messages, api_format)
            # print("============", data)
            # Request-level cache: on a whole-task rerun the already-successful
            # calls have an unchanged body, so reuse the response and skip the API.
            cache_key = _response_cache_key(data) if _RESPONSE_CACHE_ENABLED else None
            _resp_cache = _get_response_cache() if cache_key is not None else None
            cached_response = _resp_cache.get(cache_key) if cache_key is not None else None
            response = None
            max_retries = 9
            retry_delay_base = 2
            retry_delay = retry_delay_base
            for attempt in range(max_retries + 1):
                # Exponential backoff with jitter: spreads the lock-step retries of
                # concurrent threads (429 thundering herd) and lets the bucket refill.
                retry_delay = min(60.0, retry_delay_base * (2 ** attempt)) * (0.5 + random.random() * 0.5)
                # Break out only on a *real* cache hit. `response is not None` will
                # not do: a raw requests.Response left over from a retry path would
                # be mistaken for a hit and fed to get_response_usage.
                if cached_response is not None:
                    response = cached_response
                    break  # cache hit -- skip the request entirely
                try:
                    response = requests.post(base_url, json=data, headers=headers, timeout=(10, 600))
                    if response.status_code == 200:
                        try:
                            body = response.json()
                        except ValueError:
                            body = None
                        # A 200 with an empty or malformed JSON body is upstream
                        # flakiness, not a real answer -- retry it.
                        if not isinstance(body, dict):
                            if attempt < max_retries:
                                logger.warning(f"200 with empty/invalid JSON body, retry {attempt + 1}/{max_retries+1} in {retry_delay}s...")
                                time.sleep(retry_delay)
                                continue
                            raise ValueError(f"200 but empty/invalid JSON body after {max_retries} retries")
                        # A success can arrive in two shapes: OpenAI {"choices":...}
                        # or Anthropic-native {"type":"message","content":[...]}.
                        # _normalize_anthropic_response passes the former through and
                        # converts the latter. Anything else is an upstream error.
                        if isinstance(body, dict) and ("choices" in body or body.get("type") == "message" or body.get("object") == "response"):
                            if body.get("object") == "response":
                                response = _normalize_responses_api(body)
                            else:
                                response = _normalize_anthropic_response(body)
                            break
                        if attempt < max_retries:
                            logger.warning(f"200 OK but no 'choices' (likely proxy-wrapped upstream error), attempt {attempt + 1}/{max_retries+1}, retrying in {retry_delay}s. Body keys: {list(body.keys()) if isinstance(body, dict) else type(body)}")
                            time.sleep(retry_delay)
                            continue
                        raise ValueError(f"200 OK but no 'choices' after {max_retries} retries. Body: {body}")
                    # 4xx client errors (except 408/429) are deterministic — retrying
                    # just wastes 120s per stuck request. Raise as ValueError so the
                    # outer RequestException retry handler can't swallow it.
                    if 400 <= response.status_code < 500 and response.status_code not in (408, 429):
                        # Gateways that poll several backends may land on one this
                        # "Error 002 Access to Bedrock" / Azure "555420 ... Claude on Azure /
                        # account cannot use ("deployment request could not be
                        # completed"). That is bad luck in routing, not a fatal 4xx --
                        _rt = response.text.lower()
                        _routing_miss = any(s in _rt for s in (
                            "access to bedrock", "error 002", "claude on azure",
                            "deployment request could not be completed", "555420"))
                        # The same class of failure can arrive as a 400 whose
                        # error_message the gateway has masked, so keyword matching
                        # cannot see it. Retry rather than give up.
                        if (not _routing_miss and "claude" in data.get("model", "")
                                and "routify_response" in _rt and '"success":false' in _rt):
                            _routing_miss = True
                        if _routing_miss and attempt < max_retries:
                            logger.warning(f"gateway backend-access {response.status_code} (hit an unavailable backend), retry {attempt + 1}/{max_retries+1} in {retry_delay}s...")
                            time.sleep(retry_delay)
                            continue
                        logger.error(f"Non-retryable {response.status_code}: {response.text[:300]}")
                        raise ValueError(f"Non-retryable HTTP {response.status_code}: {response.text[:300]}")
                    if attempt < max_retries:
                        logger.warning(f"API returned {response.status_code}, attempt {attempt + 1}/{max_retries+1}, retrying in {retry_delay}s...")
                        time.sleep(retry_delay)
                    else:
                        response.raise_for_status()

                except requests.exceptions.RequestException as e:
                    if attempt < max_retries:
                        logger.warning(f"Request exception, attempt {attempt + 1}/{max_retries+1}, retrying in {retry_delay}s... Error: {e}")
                        time.sleep(retry_delay)
                    else:
                        raise e
            # Cache the successful response for later reruns of this task.
            # An "empty turn" is an HTTP 200 that downstream validation still
            # rejects. Keep it out of the cache so a retry resamples it.
            if (cache_key is not None and response is not None
                    and _response_is_cacheable(response)):
                _resp_cache[cache_key] = response
        except Exception as e:
            logger.error(e)
            raise e
        usage = get_response_usage(response)
        cost = get_response_cost(usage, model)
        try:
            response = response['choices'][0]
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Full response: {json.dumps(response, ensure_ascii=False, indent=2) if isinstance(response, dict) else response}")
            raise ValueError(f"Invalid API response format: {e}") from e
        assert response['message']['role'] == "assistant", (
            "The response should be an assistant message"
        )
        content = response['message'].get('content')
        tool_calls = response['message'].get('tool_calls') or []
        # Reasoning models occasionally return an empty tool_call whose
        # function.name is null: it cannot be executed and would crash ToolCall
        # validation, so skip unnamed calls and keep the rest.
        tool_calls = [
            ToolCall(
                id=tool_call.get('id'),
                name=tool_call.get('function', {}).get('name'),
                arguments=json.loads(tool_call.get('function', {}).get('arguments')) if tool_call.get('function', {}).get('arguments') else {},
            )
            for tool_call in tool_calls
            if tool_call.get('function', {}).get('name')
        ]
        tool_calls = tool_calls or None
        message = AssistantMessage(
            role="assistant",
            content=content,
            tool_calls=tool_calls,
            cost=cost,
            usage=usage,
            raw_data=response,
        )
        return message
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(e)


def get_cost(messages: list[Message]) -> tuple[float, float] | None:
    """
    Get the cost of the interaction between the agent and the user.
    Returns None if any message has no cost.
    """
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
