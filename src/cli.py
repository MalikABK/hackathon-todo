"""CLI interface (argument parsing and command dispatch) for the Todo App."""

import argparse
import sys
from pathlib import Path

# Allow running as `python src/main.py`
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models import (
    EmptyTitleError,
    Task,
    TaskAlreadyCompletedError,
    TaskList,
    TaskNotFoundError,
)
from src import services


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple CLI todo application.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create <title>
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("title", type=str, help="Task title")

    # list
    subparsers.add_parser("list", help="List all tasks")

    # complete <id>
    complete_parser = subparsers.add_parser(
        "complete", help="Mark a task as completed"
    )
    complete_parser.add_argument("id", type=int, help="Task ID")

    # update <id> <new_title>
    update_parser = subparsers.add_parser("update", help="Update a task's title")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("new_title", type=str, help="New task title")

    # delete <id>
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    return parser


def format_task_table(tasks: list[Task]) -> str:
    """Return a formatted table with ID, STATUS, TITLE columns."""
    if not tasks:
        return "No tasks found."

    lines = []
    header = f"{'ID':<4}{'STATUS':<12}{'TITLE'}"
    lines.append(header)
    for task in tasks:
        line = f"{task.id:<4}{task.status.value:<12}{task.title}"
        lines.append(line)
    return "\n".join(lines)


def dispatch_command(args: list[str], task_list: TaskList) -> int:
    """Parse arguments, dispatch to the appropriate service, print output.

    Returns exit code: 0 for success, 1 for application errors.
    """
    parser = create_parser()
    parsed = parser.parse_args(args)

    if parsed.command is None:
        parser.print_help()
        return 0

    try:
        if parsed.command == "create":
            task = services.create_task(task_list, parsed.title)
            print(f'Task created: {task.id} - "{task.title}"')
            return 0

        elif parsed.command == "list":
            tasks = services.list_tasks(task_list)
            print(format_task_table(tasks))
            return 0

        elif parsed.command == "complete":
            task = services.complete_task(task_list, parsed.id)
            print(f"Task {task.id} marked as completed.")
            return 0

        elif parsed.command == "update":
            task = services.update_task(task_list, parsed.id, parsed.new_title)
            print(f"Task {task.id} updated.")
            return 0

        elif parsed.command == "delete":
            services.delete_task(task_list, parsed.id)
            print(f"Task {parsed.id} deleted.")
            return 0

        else:
            parser.print_help()
            return 0

    except EmptyTitleError as e:
        print(f"Error: {e}")
        return 1
    except TaskNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except TaskAlreadyCompletedError as e:
        print(f"Error: {e}")
        return 1
