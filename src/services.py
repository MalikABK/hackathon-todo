"""Business logic (CRUD operations) for the Todo App."""

from src.models import Task, TaskList


def create_task(task_list: TaskList, title: str) -> Task:
    """Create a new task with the given title."""
    return task_list.add(title)


def list_tasks(task_list: TaskList) -> list[Task]:
    """Return all tasks in insertion order."""
    return task_list.list_all()


def complete_task(task_list: TaskList, task_id: int) -> Task:
    """Mark a task as completed."""
    return task_list.complete(task_id)


def update_task(task_list: TaskList, task_id: int, new_title: str) -> Task:
    """Update a task's title."""
    return task_list.update(task_id, new_title)


def delete_task(task_list: TaskList, task_id: int) -> None:
    """Delete a task by ID."""
    return task_list.delete(task_id)
