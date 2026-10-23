"""Simulated user agent — LLM-driven user for multi-turn dialogue evaluation."""

from __future__ import annotations

import random
import time

from openai import OpenAI

from ..models.message import Message
from ..utils.language import LanguageInfo, get_runtime_language


_SYSTEM_PROMPT = """\
你是一个模拟用户。你的任务是根据以下人设与AI助手进行对话。

## 你的人设
{persona}

## 规则
1. 始终保持人设角色，用自然口语回复，不要暴露你是AI
2. 根据助手的提问如实回答（基于你的人设信息）
3. 如果助手问了你人设中没有的信息，说"不太清楚具体数字"或类似自然回复
4. 如果助手已经给出了完整的计算结果和建议，且你没有更多问题，输出 [DONE]
5. 如果你对回答满意或助手已充分回答了你的问题，输出 [DONE]
6. 回复要简短自然，像真实用户一样（1-3句话）
"""


def _reply_language_directive(info: LanguageInfo) -> str:
    """Prominent instruction that the simulated user must speak the target language.

    The scaffolding above (``_SYSTEM_PROMPT``, the transcript labels, and the
    per-turn instruction) is hardcoded Chinese; without this directive the
    model replies in Chinese even on target-language runs — round-7 finding
    F9a. The caller resolves ``info`` from ``CLAW_EVAL_LANGUAGE`` via
    ``get_runtime_language()`` (exported by the CLI after ``--language``),
    mirroring how ``system_prompt._language_directive`` picks up the language
    from the environment without further threading. The ``[DONE]`` sentinel
    must stay in Latin letters or ``generate_response``'s stop check breaks.
    """
    return (
        f"**Language requirement: you are role-playing a user who speaks "
        f"{info.display}. Write every one of your messages entirely in "
        f"{info.display}. The persona and the entire conversation are in "
        f"{info.display}; never reply in Chinese or any other language. "
        f"Output the sentinel [DONE] in Latin letters exactly as written.**"
    )


def _format_transcript(messages: list[Message]) -> str:
    """Format conversation messages into a readable transcript."""
    lines = []
    for msg in messages:
        if msg.role == "system":
            continue
        text = msg.text
        if not text:
            continue
        if msg.role == "user":
            if text.startswith("[user_agent]"):
                text = text[len("[user_agent]"):].strip()
            lines.append(f"[用户]: {text}")
        elif msg.role == "assistant":
            lines.append(f"[助手]: {text}")
    return "\n".join(lines)


class UserAgent:
    """Simulated user that generates responses via an LLM."""

    def __init__(
        self,
        model_id: str,
        api_key: str,
        base_url: str = "https://openrouter.ai/api/v1",
        extra_body: dict | None = None,
        api_format: str = "openai",
    ) -> None:
        self.model_id = model_id
        self.api_key = api_key
        self.base_url = (base_url or "").rstrip("/")
        self.extra_body = extra_body or {}
        self.api_format = api_format
        # OpenAI SDK client only needed for the openai path.
        self.client = OpenAI(api_key=api_key, base_url=base_url) if api_format != "vertex" else None

    def _call_vertex(self, system: str, user_msg: str) -> str:
        """Call the Gemini-native vertex route (generateContent).

        Used when the OpenAI-compat route for the Gemini model is dead (our
        gateway 500s on gemini-3.5-flash via /protocol/openai/v1). URL carries the model
        name; auth is x-goog-api-key; body is Gemini contents/parts.
        thinking_budget=0 (non-think) is passed via generationConfig.
        """
        import httpx
        url = f"{self.base_url}/models/{self.model_id}:generateContent"
        gen_cfg: dict = {"temperature": 0.7, "maxOutputTokens": 8192}
        # Carry a thinking_budget from extra_body.google.thinking_config into the
        # native generationConfig.thinkingConfig (0 => non-think user-sim).
        tb = (((self.extra_body or {}).get("google") or {}).get("thinking_config") or {}).get("thinking_budget")
        if tb is not None:
            gen_cfg["thinkingConfig"] = {"thinkingBudget": tb}
        body = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user_msg}]}],
            "generationConfig": gen_cfg,
        }
        r = httpx.post(
            url,
            headers={"x-goog-api-key": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=body,
            timeout=120.0,
        )
        if r.status_code >= 400:
            raise RuntimeError(f"vertex HTTP {r.status_code}: {r.text[:300]}")
        data = r.json()
        parts = (data.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
        return "".join(p.get("text", "") for p in parts).strip()

    def generate_response(
        self,
        persona: str,
        conversation_messages: list[Message],
    ) -> str | None:
        """Generate a simulated user reply.

        Returns the reply text, or None if the user is satisfied ([DONE]).
        """
        info = get_runtime_language()
        system = _SYSTEM_PROMPT.format(persona=persona)
        if info is not None:
            system = _reply_language_directive(info) + "\n\n" + system
        transcript = _format_transcript(conversation_messages)
        user_msg = (
            f"以下是到目前为止的对话：\n\n{transcript}\n\n"
            "请根据你的人设回复助手的最新消息。如果你满意了就输出 [DONE]。"
        )
        if info is not None:
            user_msg += (
                f"\n\n(Reminder: reply entirely in {info.display}; "
                "output [DONE] verbatim if you are satisfied.)"
            )

        max_retries = 30
        for attempt in range(max_retries):
            try:
                if self.api_format == "vertex":
                    text = self._call_vertex(system, user_msg)
                else:
                    create_kwargs = dict(
                        model=self.model_id,
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user", "content": user_msg},
                        ],
                        temperature=0.7,
                        max_tokens=65536,
                    )
                    if self.extra_body:
                        from .providers.openai_compat import wrap_extra_body_for_gateway
                        create_kwargs["extra_body"] = wrap_extra_body_for_gateway(self.extra_body)
                    resp = self.client.chat.completions.create(**create_kwargs)
                    text = (resp.choices[0].message.content or "").strip()
                if "[DONE]" in text:
                    return None
                if text:
                    return text
                return None
            except Exception as exc:
                delay = min(2 ** (attempt + 1), 16) + random.uniform(0, 1)
                print(
                    f"[user-agent-retry] {type(exc).__name__}, "
                    f"attempt {attempt + 1}/{max_retries}, waiting {delay:.1f}s ..."
                )
                time.sleep(delay)

        # All retries exhausted — gracefully end the conversation
        return None
