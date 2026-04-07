"""Data models for the Todo App."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TodoAppError(Exception):
    """Base exception for the Todo App."""


class EmptyTitleError(TodoAppError):
    """Raised when a task title is empty or whitespace-only."""


class TaskNotFoundError(TodoAppError):
    """Raised when a referenced task ID does not exist."""


class TaskAlreadyCompletedError(TodoAppError):
    """Raised when attempting to complete an already-completed task."""


class TaskStatus(Enum):
    """Possible states for a task."""

    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class Task:
    """Represents a single todo item."""

    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class TaskList:
    """In-memory collection managing all Task objects."""

    tasks: list[Task] = field(default_factory=list)
    _next_id: int = field(default=1, init=False)

    def add(self, title: str) -> Task:
        """Create a new task, assign sequential ID, append to list."""
        trimmed = title.strip()
        if not trimmed:
            raise EmptyTitleError("Title cannot be empty.")
        task = Task(id=self._next_id, title=trimmed)
        self._next_id += 1
        self.tasks.append(task)
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        """Find a task by ID, return None if not found."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_all(self) -> list[Task]:
        """Return all tasks in insertion order."""
        return list(self.tasks)

    def update(self, task_id: int, new_title: str) -> Task:
        """Update a task's title."""
        task = self.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        trimmed = new_title.strip()
        if not trimmed:
            raise EmptyTitleError("Title cannot be empty.")
        task.title = trimmed
        return task

    def complete(self, task_id: int) -> Task:
        """Mark a task as completed."""
        task = self.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        if task.status == TaskStatus.COMPLETED:
            raise TaskAlreadyCompletedError(
                f"Task {task_id} is already completed."
            )
        task.status = TaskStatus.COMPLETED
        return task

    def delete(self, task_id: int) -> None:
        """Remove a task from the list."""
        task = self.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        self.tasks.remove(task)

    def to_dict(self) -> list[dict]:
        """Serialize all tasks to a list of dicts (Phase II hook)."""
        return [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status.value,
                "created_at": t.created_at.isoformat(),
            }
            for t in self.tasks
        ]

    @classmethod
    def from_dict(cls, data: list[dict]) -> "TaskList":
        """Deserialize tasks from a list of dicts (Phase II hook)."""
        task_list = cls()
        max_id = 0
        for item in data:
            task = Task(
                id=item["id"],
                title=item["title"],
                status=TaskStatus(item.get("status", "pending")),
                created_at=datetime.fromisoformat(item["created_at"]),
            )
            task_list.tasks.append(task)
            max_id = max(max_id, task.id)
        task_list._next_id = max_id + 1
        return task_list
