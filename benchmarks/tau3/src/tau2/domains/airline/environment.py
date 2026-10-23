# Copyright Sierra
import importlib.util
from pathlib import Path
from typing import Optional

from tau2.data_model.tasks import Task
from tau2.domains.airline.data_model import FlightDB
from tau2.domains.airline.tools import AirlineTools
from tau2.domains.airline.utils import (
    AIRLINE_TASK_SET_PATH,
    LANGUAGE,
    get_db_path,
    get_localized_paths,
    get_policy_path,
    get_tasks_path,
)
from tau2.environment.environment import Environment
from tau2.utils import load_file


def get_environment(
    db: Optional[FlightDB] = None,
    solo_mode: bool = False,
    localized: bool = False,
    language: Optional[str] = None,
) -> Environment:
    if solo_mode:
        raise ValueError("Airline domain does not support solo mode")

    if localized and language is not None:
        paths = get_localized_paths(language)
        missing = [name for name, path in paths.items() if not path.exists()]
        if missing:
            raise FileNotFoundError(
                f"Localized files for language '{language}' not found. "
                f"Missing: {missing}. "
                f"Expected under: {paths['policy'].parent}"
            )
        with open(paths["policy"], "r") as fp:
            policy = fp.read()

        # If a generated data_model_ext.py exists, load FlightDBLocalized from
        # it; otherwise fall back to the base FlightDB.
        ext_path = paths["policy"].parent / "data_model_ext.py"
        db_class = FlightDB
        if ext_path.exists():
            try:
                ext_spec = importlib.util.spec_from_file_location(
                    f"localized_data_model_ext_{language}", ext_path
                )
                if ext_spec and ext_spec.loader:
                    ext_mod = importlib.util.module_from_spec(ext_spec)
                    ext_spec.loader.exec_module(ext_mod)
                    db_class = getattr(ext_mod, "FlightDBLocalized", FlightDB)
            except Exception:
                # Fall back to base if extension cannot be loaded
                db_class = FlightDB

        loc_db = db_class.load(paths["db"])
        spec = importlib.util.spec_from_file_location("localized_tools", paths["tools"])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        tools = module.AirlineTools(loc_db)
        return Environment(
            domain_name="airline",
            policy=policy,
            tools=tools,
        )

    lang = language or (LANGUAGE or None)
    if db is None:
        db = FlightDB.load(get_db_path(lang))
    tools = AirlineTools(db)
    with open(get_policy_path(lang), "r") as fp:
        policy = fp.read()
    return Environment(
        domain_name="airline",
        policy=policy,
        tools=tools,
    )


def get_tasks(
    task_split_name: Optional[str] = "base",
    language: Optional[str] = None,
) -> list[Task]:
    lang = language or (LANGUAGE or None)
    tasks = load_file(get_tasks_path(lang))
    tasks = [Task.model_validate(task) for task in tasks]
    if task_split_name is None:
        return tasks
    task_splits = get_tasks_split()
    if task_split_name not in task_splits:
        raise ValueError(
            f"Invalid task split name: {task_split_name}. Valid splits are: {task_splits.keys()}"
        )
    return [task for task in tasks if task.id in task_splits[task_split_name]]


def get_tasks_split() -> dict[str, list[str]]:
    split_file = (
        Path(AIRLINE_TASK_SET_PATH).parent
        / f"split_{Path(AIRLINE_TASK_SET_PATH).stem}.json"
    )
    return load_file(split_file)
