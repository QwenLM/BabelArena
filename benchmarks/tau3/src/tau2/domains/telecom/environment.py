# Copyright Sierra
from functools import partial
from pathlib import Path
from typing import Optional

from tau2.data_model.tasks import Task
from tau2.domains.telecom.data_model import LineStatus, TelecomDB
from tau2.domains.telecom.tools import TelecomTools
from tau2.domains.telecom.user_data_model import PaymentRequest, TelecomUserDB
from tau2.domains.telecom.user_tools import TelecomUserTools
from tau2.domains.telecom.utils import (
    LANGUAGE,
    TELECOM_TASK_SET_PATH,
    get_db_path,
    get_main_policy_path,
    get_tasks_path,
    get_tech_support_manual_path,
    get_tech_support_workflow_path,
    get_user_db_path,
)
from tau2.environment.environment import Environment
from tau2.utils import load_file


class TelecomEnvironment(Environment):
    tools: TelecomTools
    user_tools: TelecomUserTools

    def __init__(
        self,
        domain_name: str,
        policy: str,
        tools: TelecomTools,
        user_tools: TelecomUserTools,
    ):
        super().__init__(domain_name, policy, tools, user_tools)

    def sync_tools(self):
        """
        Sync the tools with the user's surroundings.
        If the line is roaming enabled, then the user is allowed to roam.
        """
        if self.user_tools.db.surroundings.phone_number is None:
            return
        phone_number = self.user_tools.db.surroundings.phone_number
        line = self.tools._get_line_by_phone(phone_number)
        if line is None:
            raise ValueError(
                f"Wrong scenario, line not found for phone number: {phone_number}"
            )
        # Check if the line is active
        if line.status == LineStatus.ACTIVE:
            self.user_tools.db.surroundings.line_active = True
        else:
            self.user_tools.db.surroundings.line_active = False

        # Check if the line is roaming enabled
        if line.roaming_enabled:
            self.user_tools.db.surroundings.roaming_allowed = True
        else:
            self.user_tools.db.surroundings.roaming_allowed = False

        # Check if the user has exceeded their data usage limit
        plan = self.tools._get_plan_by_id(line.plan_id)
        if plan is None:
            raise ValueError(
                f"Wrong scenario, invalid plan id ({line.plan_id}) for the phone number {phone_number}"
            )
        if line.data_used_gb >= plan.data_limit_gb + line.data_refueling_gb:
            self.user_tools.db.surroundings.mobile_data_usage_exceeded = True
        else:
            self.user_tools.db.surroundings.mobile_data_usage_exceeded = False

        # Check if the user has paid a bill
        current_payment_request = self.user_tools.db.surroundings.payment_request
        if current_payment_request is not None:
            if current_payment_request.paid:
                self.tools._set_bill_to_paid(current_payment_request.bill_id)
                self.user_tools.db.surroundings.payment_request = None

        # Check if the user has a payment request
        current_payment_request = self.user_tools.db.surroundings.payment_request
        if (
            current_payment_request is None
        ):  # If there already is a payment request, do nothing
            customer = self.tools.get_customer_by_phone(phone_number)
            bills = self.tools._get_bills_awaiting_payment(customer)
            if len(bills) != 0:
                bill = bills[0]
                self.user_tools.db.surroundings.payment_request = PaymentRequest(
                    bill_id=bill.bill_id, amount_due=bill.total_due
                )


def get_environment(
    db: Optional[TelecomDB] = None,
    user_db: Optional[TelecomUserDB] = None,
    solo_mode: bool = False,
    policy_type: str = "manual",  # "manual" or "workflow"
    language: Optional[str] = None,
) -> TelecomEnvironment:
    lang = language or (LANGUAGE or None)
    if db is None:
        db = TelecomDB.load(get_db_path(lang))
    tools = TelecomTools(db)
    if user_db is None:
        user_db = TelecomUserDB.load(get_user_db_path(lang))
    user_tools = TelecomUserTools(user_db)
    if policy_type not in ("manual", "workflow"):
        raise ValueError(f"Invalid policy type: {policy_type}")
    policy_path = get_main_policy_path(solo_mode=solo_mode, language=lang)
    if policy_type == "manual":
        tech_support_policy_path = get_tech_support_manual_path(
            solo_mode=solo_mode, language=lang
        )
    else:
        tech_support_policy_path = get_tech_support_workflow_path(
            solo_mode=solo_mode, language=lang
        )
    main_policy = load_file(policy_path)
    tech_support_policy = load_file(tech_support_policy_path)
    policy = (
        "<main_policy>\n"
        + main_policy
        + "\n</main_policy>\n"
        + "<tech_support_policy>\n"
        + tech_support_policy
        + "\n</tech_support_policy>"
    )
    if policy_type == "manual":
        domain_name = "telecom"
    else:
        domain_name = "telecom-workflow"
    env = TelecomEnvironment(
        domain_name=domain_name,
        policy=policy,
        tools=tools,
        user_tools=user_tools,
    )
    if solo_mode:
        env.set_solo_mode(True)
    return env


get_environment_manual_policy = partial(get_environment, policy_type="manual")
get_environment_workflow_policy = partial(get_environment, policy_type="workflow")


def load_tasks(path: str) -> list[Task]:
    """Load tasks from a data file, could be json, yaml or toml file."""
    tasks = load_file(path)
    if isinstance(tasks, dict) and "tasks" in tasks:
        tasks = tasks["tasks"]
    return [Task.model_validate(task) for task in tasks]


def load_tasks_split(path: str) -> Optional[dict[str, list[str]]]:
    """Load tasks split from a data file, could be json, yaml or toml file."""
    split_file = Path(path).parent / f"split_{Path(path).stem}.json"
    if split_file.exists():
        tasks_split = load_file(split_file)
        return tasks_split
    return None


def get_tasks(
    task_split_name: Optional[str] = "base",
    language: Optional[str] = None,
) -> list[Task]:
    lang = language or (LANGUAGE or None)
    tasks = load_tasks(get_tasks_path(lang))
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
    # Split file is based on English tasks.json; task IDs are stable across
    # translations.
    return load_tasks_split(TELECOM_TASK_SET_PATH)


# Legacy functions for backward compatibility
def get_tasks_full(task_split_name: Optional[str] = None) -> list[Task]:
    """Load the legacy fixed full task set, ignoring split selection."""
    return get_tasks("full")


def get_tasks_small(task_split_name: Optional[str] = None) -> list[Task]:
    """Load the legacy fixed small task set, ignoring split selection."""
    return get_tasks("small")


if __name__ == "__main__":
    env = get_environment()
    # print(env.get_tools())
    for tool in env.get_user_tools():
        print(tool.name)
