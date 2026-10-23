from enum import Enum
from typing import Annotated, Any, Callable, ClassVar, Dict, Optional, TypeVar

from loguru import logger
from pydantic import BaseModel, Field

from tau2.environment.db import DB
from tau2.environment.tool import Tool, as_tool
from tau2.utils import get_dict_hash, update_pydantic_model_with_dict
from tau2.utils.utils import DATA_DIR

TOOL_ATTR = "__tool__"
TOOL_TYPE_ATTR = "__tool_type__"
MUTATES_STATE_ATTR = "__mutates_state__"
DISCOVERABLE_ATTR = "__discoverable__"


T = TypeVar("T", bound=DB)


class ToolKitType(type):
    """Metaclass for ToolKit classes."""

    def __init__(cls, name, bases, attrs):
        func_tools = {}
        for name, method in attrs.items():
            if isinstance(method, property):
                method = method.fget
            if hasattr(method, TOOL_ATTR):
                func_tools[name] = method

        @property
        def _func_tools(self) -> Dict[str, Callable]:
            """Get the tools available in the ToolKit."""
            all_func_tools = func_tools.copy()
            try:
                all_func_tools.update(super(cls, self)._func_tools)
            except AttributeError:
                pass
            return all_func_tools

        cls._func_tools = _func_tools


class ToolType(str, Enum):
    """Conceptual classification of a tool.

    This describes what a tool *does* from the user/agent perspective and is
    used for metrics, prompt construction, and display.  It does **not**
    control evaluation-replay behaviour -- see the ``mutates_state`` parameter
    on :func:`is_tool` for that.

    Members:
        READ: Queries / retrieves data without side-effects.
        WRITE: Creates, updates, or deletes data.
        THINK: Pure reasoning -- no new information, no side-effects.
        GENERIC: Utility that doesn't fit the other categories.
    """

    READ = "read"
    WRITE = "write"
    THINK = "think"
    GENERIC = "generic"


def is_tool(
    tool_type: ToolType = ToolType.READ,
    mutates_state: Optional[bool] = None,
):
    """Decorator to mark a function as a tool.

    Args:
        tool_type: Conceptual classification (READ, WRITE, THINK, GENERIC).
        mutates_state: Whether this tool mutates environment / DB state.
            When ``None`` (the default) the value is **inferred** from
            *tool_type*: ``True`` for WRITE, ``False`` otherwise.  Override
            explicitly for edge-cases such as a WRITE tool that signals an
            action but does not modify the database (e.g.
            ``transfer_to_human_agents``).

            During evaluation replay (``set_state``), only tools with
            ``mutates_state=True`` are re-executed; all others are skipped.
    """
    if mutates_state is None:
        mutates_state = tool_type == ToolType.WRITE

    def decorator(func):
        setattr(func, TOOL_ATTR, True)
        setattr(func, TOOL_TYPE_ATTR, tool_type)
        setattr(func, MUTATES_STATE_ATTR, mutates_state)
        return func

    return decorator


def is_discoverable_tool(
    tool_type: ToolType = ToolType.READ,
    mutates_state: Optional[bool] = None,
):
    """Decorator to mark a function as a discoverable tool.

    Discoverable tools are tools that exist and can be called, but are not
    included in the agent's system prompt by default. The agent must discover
    these tools through the knowledge base and unlock them before calling.

    The docstring of the decorated function serves as the tool definition:
    - First paragraph: tool description
    - Args section: parameter definitions (parsed for name, type hint, and description)
    - The function name is the tool name

    Args:
        tool_type: Conceptual classification (READ, WRITE, THINK, GENERIC).
        mutates_state: Whether this tool mutates environment / DB state.
            See :func:`is_tool` for details.
    """
    if mutates_state is None:
        mutates_state = tool_type == ToolType.WRITE

    def decorator(func):
        setattr(func, TOOL_ATTR, True)
        setattr(func, TOOL_TYPE_ATTR, tool_type)
        setattr(func, MUTATES_STATE_ATTR, mutates_state)
        setattr(func, DISCOVERABLE_ATTR, True)
        return func

    return decorator


import json as _json
import os as _os
from pathlib import Path as _Path


def _resolve_overlay_language() -> Optional[str]:
    lang = (_os.getenv("TAU2_LANGUAGE") or "").strip()
    if not lang or lang.lower() == "english":
        return None
    return lang


def _resolve_overlay_path(domain: str, language: str) -> _Path:
    return DATA_DIR / "tau2" / "domains" / domain / f"tools_{language}.json"


def _load_overlay(domain: str, language: str) -> Dict[str, Dict[str, Any]]:
    path = _resolve_overlay_path(domain, language)
    if not path.exists() or path.stat().st_size == 0:
        raise FileNotFoundError(
            f"Translated tool descriptions missing for domain {domain!r}, "
            f"language {language!r}: {path}. Re-fetch the task data (`./bench fetch-data`)."
        )
    return _json.loads(path.read_text())


def _apply_translation(
    tool: Tool,
    entry: Optional[Dict[str, Any]],
    *,
    domain: str,
    language: str,
) -> None:
    if entry is None:
        raise FileNotFoundError(
            f"Tool {tool.name!r} missing from tools_{language}.json for domain "
            f"{domain!r}. Re-fetch the task data (`./bench fetch-data`)."
        )
    tool.short_desc = entry.get("short_desc", tool.short_desc)
    tool.long_desc = entry.get("long_desc", tool.long_desc)
    translated_params = entry.get("params", {}) or {}
    for param_name, field in tool.params.model_fields.items():
        new_desc = translated_params.get(param_name)
        if new_desc is None:
            logger.warning(
                f"Tool {tool.name!r} parameter {param_name!r} has no "
                f"translation in tools_{language}.json for domain {domain!r}; "
                f"using English description."
            )
            continue
        field.description = new_desc
    tool.params.model_rebuild(force=True)


class ToolKitBase(metaclass=ToolKitType):
    """Base class for ToolKit classes."""

    domain_name: ClassVar[Optional[str]] = None

    def __init__(self, db: Optional[T] = None):
        self.db: Optional[T] = db

    @property
    def tools(self) -> Dict[str, Callable]:
        """Get the tools available in the ToolKit."""
        return {name: getattr(self, name) for name in self._func_tools.keys()}

    def use_tool(self, tool_name: str, **kwargs) -> str:
        """Use a tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return self.tools[tool_name](**kwargs)

    def get_tools(self, include: Optional[list[str]] = None) -> Dict[str, Tool]:
        """Get the non-discoverable tools available in the ToolKit.

        Discoverable tools are excluded — they should not appear in the
        agent's system prompt. Use `get_discoverable_tools()` to access them.

        Args:
            include: If provided, only return tools whose names are in this list.
                If None, return all non-discoverable tools (no filtering).

        Returns:
            A dictionary of non-discoverable tools available in the ToolKit.
        """
        # NOTE: as_tool needs to get the function (self.foo), not the `foo(self, ...)`
        # Otherwise, the `self` will exists in the arguments.
        # Therefore, it needs to be called with getattr(self, name)
        tools = {
            name: as_tool(tool)
            for name, tool in self.tools.items()
            if not getattr(tool, DISCOVERABLE_ATTR, False)
        }
        if include is not None:
            allowed = set(include)
            unknown = allowed - set(tools.keys())
            if unknown:
                available = sorted(tools.keys())
                raise ValueError(
                    f"Tool(s) not found: {sorted(unknown)}. Available: {available}"
                )
            tools = {name: tool for name, tool in tools.items() if name in allowed}

        lang = _resolve_overlay_language()
        if lang is not None and self.domain_name:
            overlay = _load_overlay(self.domain_name, lang)
            for name, tool in tools.items():
                _apply_translation(
                    tool, overlay.get(name), domain=self.domain_name, language=lang
                )
        return tools

    def has_tool(self, tool_name: str) -> bool:
        """Check if a tool exists in the ToolKit."""
        return tool_name in self.tools

    def is_discoverable(self, tool_name: str) -> bool:
        """Check if a tool is a discoverable tool."""
        if tool_name not in self.tools:
            return False
        return getattr(self.tools[tool_name], DISCOVERABLE_ATTR, False)

    def get_discoverable_tools(self) -> Dict[str, Callable]:
        """Get all discoverable tool methods on this toolkit."""
        return {
            name: tool
            for name, tool in self.tools.items()
            if getattr(tool, DISCOVERABLE_ATTR, False)
        }

    def has_discoverable_tool(self, tool_name: str) -> bool:
        """Check if a discoverable tool exists."""
        return tool_name in self.get_discoverable_tools()

    def tool_type(self, tool_name: str) -> ToolType:
        """Get the type of a tool."""
        return getattr(self.tools[tool_name], TOOL_TYPE_ATTR)

    def tool_mutates_state(self, tool_name: str) -> bool:
        """Check whether a tool mutates environment state.

        Falls back to ``True`` (safe default: assume mutation) if the
        attribute is missing -- e.g. for tools decorated before the
        ``mutates_state`` parameter was introduced.
        """
        return getattr(self.tools[tool_name], MUTATES_STATE_ATTR, True)

    def get_statistics(self) -> dict[str, Any]:
        """Get the statistics of the ToolKit."""
        num_tools = len(self.tools)
        num_read_tools = sum(
            self.tool_type(name) == ToolType.READ for name in self.tools
        )
        num_write_tools = sum(
            self.tool_type(name) == ToolType.WRITE for name in self.tools
        )
        num_think_tools = sum(
            self.tool_type(name) == ToolType.THINK for name in self.tools
        )
        num_generic_tools = sum(
            self.tool_type(name) == ToolType.GENERIC for name in self.tools
        )
        return {
            "num_tools": num_tools,
            "num_read_tools": num_read_tools,
            "num_write_tools": num_write_tools,
            "num_think_tools": num_think_tools,
            "num_generic_tools": num_generic_tools,
        }

    def update_db(self, update_data: Optional[dict[str, Any]] = None):
        """Update the database of the ToolKit."""
        if update_data is None:
            update_data = {}
        if self.db is None:
            raise ValueError("Database has not been initialized.")
        self.db = update_pydantic_model_with_dict(self.db, update_data)

    def get_db_hash(self) -> str:
        """Get the hash of the database."""
        return get_dict_hash(self.db.model_dump())


class ToolSignature(BaseModel):
    """A signature of a tool."""

    name: Annotated[str, Field(description="The name of the tool")]
    doc: Annotated[str, Field(description="The documentation of the tool")]
    params: Annotated[
        Optional[dict],
        Field(description="JSON schema of the parameters of the tool", default=None),
    ]
    returns: Annotated[
        Optional[dict],
        Field(description="JSON schema of the return of the tool", default=None),
    ]


def get_tool_signatures(tools: ToolKitBase) -> dict[str, ToolSignature]:
    """Get all the tool signatures from a tool kit.

    Returns:
        A dictionary of tool signatures.
    """
    signatures = {}
    for name, tool in tools.get_tools().items():
        signatures[name] = ToolSignature(
            name=name,
            doc=str(tool),
            params=tool._serialize_params(tool.params),
            returns=tool._serialize_returns(tool.returns),
        )
    return signatures


def get_tool_types(tools: ToolKitBase) -> dict[str, ToolType]:
    """Get the type of a tool.

    Returns:
        A dictionary of tool types.
    """
    return {name: tools.tool_type(name) for name in tools.get_tools().keys()}


class GenericToolKit(ToolKitBase):
    """Defines some generic tools.
    - Think
    - Calculate
    """

    @is_tool(ToolType.THINK)
    def think(self, thought: str) -> str:
        """
        Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning is needed.

        Args:
            thought: A thought to think about.

        Returns:
            Empty string
        """
        return ""

    @is_tool(ToolType.GENERIC)
    def calculate(self, expression: str) -> str:
        """
        Calculate the result of a mathematical expression.

        Args:
            expression: The mathematical expression to calculate, such as '2 + 2'. The expression can contain numbers, operators (+, -, *, /), parentheses, and spaces.

        Returns:
            The result of the mathematical expression.

        Raises:
            ValueError: If the expression is invalid.
        """
        if not all(char in "0123456789+-*/(). " for char in expression):
            raise ValueError("Invalid characters in expression")
        return str(round(float(eval(expression, {"__builtins__": None}, {})), 2))
