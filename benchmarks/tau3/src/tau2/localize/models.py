"""Pydantic data models for all 5 stages of the deep localization pipeline."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Stage 1 – Discovery
# ---------------------------------------------------------------------------


class Candidate(BaseModel):
    """A discovered document from the web discovery stage."""

    candidate_id: str
    source_url: str
    carrier: str
    topic: str
    summary: str
    key_facts: list[str] = Field(default_factory=list)
    raw_content: str
    relevance_score: float = Field(ge=0.0, le=1.0)


class CandidateSet(BaseModel):
    """Collection of discovered candidates for a given language."""

    lang: str
    candidates: list[Candidate] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Stage 2 – Curation
# ---------------------------------------------------------------------------


class CurationAction(str, Enum):
    approved = "approved"
    rejected = "rejected"
    edited = "edited"
    merged = "merged"
    added = "added"


class CuratedCandidate(Candidate):
    """A candidate that has been through human or automated curation."""

    curation_action: CurationAction
    original_summary: Optional[str] = None
    merged_from: list[str] = Field(default_factory=list)


class ApprovedSet(BaseModel):
    """Collection of curated and approved candidates for a given language."""

    lang: str
    approved: list[CuratedCandidate] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Stage 3 – Diff Analyzer
# ---------------------------------------------------------------------------


class ChangeType(str, Enum):
    modify_policy = "modify_policy"
    modify_tool = "modify_tool"
    add_tool = "add_tool"
    remove_tool = "remove_tool"
    modify_data = "modify_data"
    modify_task = "modify_task"


class LocalizationDiff(BaseModel):
    """A single localization change derived from approved candidate documents."""

    id: str
    topic: str
    source_docs: list[str] = Field(default_factory=list)
    change_type: ChangeType
    target: str
    description: str
    whitelisted: bool = False
    requires_approval: bool = True
    approved: bool = False
    confidence: float = Field(ge=0.0, le=1.0)
    justification: Optional[str] = None


class DiffSet(BaseModel):
    """Collection of localization diffs for a given language."""

    lang: str
    diffs: list[LocalizationDiff] = Field(default_factory=list)
    deviation_score: float = Field(ge=0.0, le=1.0)


# ---------------------------------------------------------------------------
# Stage 4 – Generator
# ---------------------------------------------------------------------------


class Manifest(BaseModel):
    """Summary of everything generated for a localized environment."""

    base_commit: str
    lang: str
    generated_at: datetime
    tools_added: list[str] = Field(default_factory=list)
    tools_modified: list[str] = Field(default_factory=list)
    tools_removed: list[str] = Field(default_factory=list)
    policy_sections_modified: list[str] = Field(default_factory=list)
    policy_sections_added: list[str] = Field(default_factory=list)
    db_entities_replaced: dict[str, int] = Field(default_factory=dict)
    tasks_adapted: int = 0
    tasks_variant: int = 0
    tasks_new: int = 0
    tasks_flagged: int = 0
    deviation_score: float = Field(ge=0.0, le=1.0)


# ---------------------------------------------------------------------------
# Stage 5 – Validator
# ---------------------------------------------------------------------------


class TaskResult(BaseModel):
    """Result of running a single task during validation."""

    task_id: str
    passed: bool
    error: Optional[str] = None


class IssueType(str, Enum):
    replay_failed = "replay_failed"
    false_positive = "false_positive"
    false_negative = "false_negative"
    completeness_failed = "completeness_failed"


class EvalCriteriaIssue(BaseModel):
    """An issue discovered during eval criteria checking."""

    task_id: str
    issue: IssueType
    detail: str


class RecommendationLevel(str, Enum):
    PASS = "PASS"
    PASS_WITH_WARNINGS = "PASS_WITH_WARNINGS"
    FAIL = "FAIL"


class RegressionReport(BaseModel):
    """Summary of regression test results."""

    total: int
    passed: int
    failed: int
    flagged_skipped: int
    failures: list[TaskResult] = Field(default_factory=list)


class InvariantReport(BaseModel):
    """Summary of invariant check results."""

    total: int
    passed: int
    failed: int
    failures: list[dict] = Field(default_factory=list)


class EvalCriteriaReport(BaseModel):
    """Summary of eval criteria validation results."""

    total_tasks: int
    replay_passed: int
    replay_failed: int
    negative_replay_passed: int
    false_positive_detected: int
    false_negative_detected: int
    completeness_passed: int
    issues: list[EvalCriteriaIssue] = Field(default_factory=list)


class ValidationReport(BaseModel):
    """Top-level validation report combining all sub-reports."""

    lang: str
    regression: RegressionReport
    invariants: InvariantReport
    eval_criteria: EvalCriteriaReport
    recommendation: RecommendationLevel
