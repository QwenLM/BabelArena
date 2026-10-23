"""Tau2 conversational agent benchmark framework.

Public exports are loaded lazily so importing a lightweight submodule does not
initialize optional voice providers, runner state, or LLM integrations.
"""

from __future__ import annotations

import importlib
import warnings
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import tau2.runner as runner
    from tau2.agent.base.llm_config import LLMConfigMixin
    from tau2.agent.base_agent import FullDuplexAgent, HalfDuplexAgent
    from tau2.agent.llm_agent import LLMAgent, LLMSoloAgent
    from tau2.data_model.simulation import (
        BaseRunConfig,
        RunConfig,
        SimulationRun,
        TextRunConfig,
        VoiceRunConfig,
    )
    from tau2.data_model.tasks import Task
    from tau2.environment.environment import Environment
    from tau2.evaluator.evaluator import EvaluationType, evaluate_simulation
    from tau2.orchestrator.modes import CommunicationMode
    from tau2.orchestrator.orchestrator import Orchestrator
    from tau2.registry import Registry, registry
    from tau2.run import run_domain
    from tau2.user.user_simulator import UserSimulator
    from tau2.user.user_simulator_base import FullDuplexUser, HalfDuplexUser
    from tau2.user.user_simulator_streaming import VoiceStreamingUserSimulator
    from tau2.utils.display import ConsoleDisplay, MarkdownDisplay

_LAZY_IMPORTS: dict[str, tuple[str, str | None]] = {
    "runner": ("tau2.runner", None),
    "LLMConfigMixin": ("tau2.agent.base.llm_config", "LLMConfigMixin"),
    "FullDuplexAgent": ("tau2.agent.base_agent", "FullDuplexAgent"),
    "HalfDuplexAgent": ("tau2.agent.base_agent", "HalfDuplexAgent"),
    "LLMAgent": ("tau2.agent.llm_agent", "LLMAgent"),
    "LLMSoloAgent": ("tau2.agent.llm_agent", "LLMSoloAgent"),
    "BaseRunConfig": ("tau2.data_model.simulation", "BaseRunConfig"),
    "RunConfig": ("tau2.data_model.simulation", "RunConfig"),
    "SimulationRun": ("tau2.data_model.simulation", "SimulationRun"),
    "TextRunConfig": ("tau2.data_model.simulation", "TextRunConfig"),
    "VoiceRunConfig": ("tau2.data_model.simulation", "VoiceRunConfig"),
    "Task": ("tau2.data_model.tasks", "Task"),
    "Environment": ("tau2.environment.environment", "Environment"),
    "EvaluationType": ("tau2.evaluator.evaluator", "EvaluationType"),
    "evaluate_simulation": ("tau2.evaluator.evaluator", "evaluate_simulation"),
    "CommunicationMode": ("tau2.orchestrator.modes", "CommunicationMode"),
    "Orchestrator": ("tau2.orchestrator.orchestrator", "Orchestrator"),
    "Registry": ("tau2.registry", "Registry"),
    "registry": ("tau2.registry", "registry"),
    "run_domain": ("tau2.run", "run_domain"),
    "UserSimulator": ("tau2.user.user_simulator", "UserSimulator"),
    "FullDuplexUser": ("tau2.user.user_simulator_base", "FullDuplexUser"),
    "HalfDuplexUser": ("tau2.user.user_simulator_base", "HalfDuplexUser"),
    "VoiceStreamingUserSimulator": (
        "tau2.user.user_simulator_streaming",
        "VoiceStreamingUserSimulator",
    ),
    "ConsoleDisplay": ("tau2.utils.display", "ConsoleDisplay"),
    "MarkdownDisplay": ("tau2.utils.display", "MarkdownDisplay"),
}

_DEPRECATED_ALIASES = {
    "BaseAgent": "HalfDuplexAgent",
    "LocalAgent": "HalfDuplexAgent",
    "BaseStreamingAgent": "FullDuplexAgent",
    "BaseUser": "HalfDuplexUser",
    "BaseStreamingUser": "FullDuplexUser",
}


def __getattr__(name: str) -> Any:
    """Resolve public exports on first access."""
    if name in _DEPRECATED_ALIASES:
        replacement = _DEPRECATED_ALIASES[name]
        warnings.warn(
            f"{name} is deprecated, use {replacement} instead",
            DeprecationWarning,
            stacklevel=2,
        )
        value = __getattr__(replacement)
        globals()[name] = value
        return value

    target = _LAZY_IMPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attribute_name = target
    module = importlib.import_module(module_name)
    value = module if attribute_name is None else getattr(module, attribute_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Include lazy and deprecated exports in module introspection."""
    return sorted(set(globals()) | set(__all__))


__all__ = [
    "Orchestrator",
    "LLMAgent",
    "LLMSoloAgent",
    "LLMConfigMixin",
    "UserSimulator",
    "HalfDuplexAgent",
    "FullDuplexAgent",
    "HalfDuplexUser",
    "FullDuplexUser",
    "Environment",
    "Registry",
    "registry",
    "SimulationRun",
    "Task",
    "evaluate_simulation",
    "EvaluationType",
    "BaseRunConfig",
    "TextRunConfig",
    "VoiceRunConfig",
    "RunConfig",
    "run_domain",
    "runner",
    "CommunicationMode",
    "VoiceStreamingUserSimulator",
    "ConsoleDisplay",
    "MarkdownDisplay",
    "BaseAgent",
    "LocalAgent",
    "BaseStreamingAgent",
    "BaseUser",
    "BaseStreamingUser",
]
