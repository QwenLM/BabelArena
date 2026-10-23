"""Shared deterministic grading for image QA tasks with oracle answers."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from claw_eval.graders.base import AbstractGrader
from claw_eval.models.task import TaskDefinition
from claw_eval.models.trace import DimensionScores, MediaLoad, ToolDispatch, TraceMessage


class ImageQAOracleMixin:
    """Grade image QA tasks against a task-local oracle answer spec."""

    def grade(
        self,
        messages: list[TraceMessage],
        dispatches: list[ToolDispatch],
        task: TaskDefinition,
        audit_data: dict[str, dict] | None = None,
        judge: Any | None = None,
        media_events: list[MediaLoad] | None = None,
        env_snapshot: dict | None = None,
    ) -> DimensionScores:
        del audit_data, judge, env_snapshot

        scores = DimensionScores()
        scores.safety = 1.0

        final_text = self._get_final_assistant_text(messages)
        oracle = self._load_oracle(task)

        image_loaded = 0.0
        if media_events:
            image_loaded = 1.0 if any(
                event.modality == "image" and event.status == "loaded"
                for event in media_events
            ) else 0.0

        answer_score = self._score_answer(final_text, oracle)
        scores.completion = round(min(0.30 * image_loaded + 0.70 * answer_score, 1.0), 2)
        scores.robustness = self.compute_robustness(dispatches)
        # scores.communication = self._score_communication(final_text, answer_score)
        scores.efficiency_turns = len(
            [message for message in messages if message.message.role == "assistant"]
        )
        return scores

    def _load_oracle(self, task: TaskDefinition) -> dict[str, Any]:
        if not task.task_file:
            raise ValueError("TaskDefinition.task_file is required for oracle loading.")

        task_dir = Path(task.task_file).resolve().parent
        oracle_path = task_dir / "fixtures" / "oracle.json"
        with open(oracle_path, encoding="utf-8") as fh:
            oracle = json.load(fh)

        # Language-aware union: when a translated sidecar oracle exists, accept
        # BOTH the source-language and the localized renderings. The canonical
        # answer comes from the sidecar (it matches the language the agent is
        # instructed to respond in); every source alias / required-entity
        # alternative is kept so a source-language answer still scores.
        from ..utils.language import get_runtime_language

        info = get_runtime_language()
        if info is not None:
            sidecar_path = task_dir / f"fixtures_{info.suffix}" / "oracle.json"
            if sidecar_path.is_file():
                with open(sidecar_path, encoding="utf-8") as fh:
                    localized = json.load(fh)
                merged: dict[str, Any] = dict(localized)
                aliases = [localized.get("canonical_answer", ""), *(localized.get("aliases") or [])]
                for alias in [oracle.get("canonical_answer", ""), *(oracle.get("aliases") or [])]:
                    if alias and alias not in aliases:
                        aliases.append(alias)
                merged["aliases"] = [a for a in aliases[1:] if a]
                src_req = oracle.get("required_entities") or []
                loc_req = localized.get("required_entities") or []
                if src_req and loc_req and len(src_req) == len(loc_req):
                    # pairwise alternatives: entity i counts if either rendering appears
                    merged["required_entities"] = loc_req
                    merged["required_entity_alternatives"] = src_req
                return merged
        return oracle

    def _score_answer(self, final_text: str, oracle: dict[str, Any]) -> float:
        if not final_text.strip():
            return 0.0

        normalized_text = self._normalize(final_text)
        aliases = [
            oracle.get("canonical_answer", ""),
            *(oracle.get("aliases") or []),
        ]
        required_entities = oracle.get("required_entities") or []

        if any(self._contains(normalized_text, alias) for alias in aliases):
            return 1.0

        if required_entities:
            alternatives = oracle.get("required_entity_alternatives") or [None] * len(required_entities)
            matched_entities = sum(
                1
                for entity, alt in zip(required_entities, alternatives)
                if self._contains(normalized_text, entity)
                or (alt and self._contains(normalized_text, alt))
            )
            return round(matched_entities / len(required_entities), 2)

        return 0.0

    def _score_communication(self, final_text: str, answer_score: float) -> float:
        if not final_text.strip():
            return 0.0

        concise = len(final_text.strip()) <= 240
        if answer_score >= 1.0:
            return 0.9 if concise else 0.82
        if answer_score >= 0.5:
            return 0.7 if concise else 0.62
        return 0.35 if concise else 0.3

    @staticmethod
    def _normalize(text: str) -> str:
        text = unicodedata.normalize("NFKC", text).lower()
        return re.sub(r"[\W_]+", "", text, flags=re.UNICODE)

    def _contains(self, normalized_text: str, candidate: str) -> bool:
        normalized_candidate = self._normalize(candidate)
        return bool(normalized_candidate) and normalized_candidate in normalized_text


class _ProtocolCheck(ImageQAOracleMixin, AbstractGrader):
    """Internal type-check helper; task graders should subclass the mixin directly."""

