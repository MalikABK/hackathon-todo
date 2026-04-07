# Data Model: CLI Todo App (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2026-04-07

## Entities

### Task

Represents a single todo item.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `id` | `int` | Unique sequential identifier | Auto-assigned, read-only |
| `title` | `str` | User-provided task description | Non-empty, trimmed whitespace |
| `status` | `TaskStatus` | Current state | Enum: `pending` \| `completed` |
| `created_at` | `datetime` | Creation timestamp | Auto-set on creation |

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
```

### TaskList

In-memory collection managing all Task objects.

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `add(title)` | `str` | `Task` | Creates task, assigns ID, appends to list |
| `get_by_id(id)` | `int` | `Task \| None` | Finds task by ID |
| `list_all()` | — | `list[Task]` | Returns all tasks in insertion order |
| `update(id, new_title)` | `int, str` | `Task` | Updates task title |
| `complete(id)` | `int` | `Task` | Sets status to completed |
| `delete(id)` | `int` | `None` | Removes task from list |
| `to_dict()` | — | `list[dict]` | Serializes all tasks (Phase II hook) |
| `from_dict(data)` | `list[dict]` | `TaskList` | Deserializes tasks (Phase II hook) |

```python
@dataclass
class TaskList:
    tasks: list[Task] = field(default_factory=list)
    _next_id: int = field(default=1, init=False)

    # CRUD + complete methods defined here
```

## State Transitions

```
  ┌─────────┐  complete(id)  ┌───────────┐
  │ PENDING │ ──────────────► │ COMPLETED │
  └─────────┘                 └───────────┘
     ▲                              │
     │                              │ (no reverse transition in Phase I)
     └──────────────────────────────┘
```

- `PENDING → COMPLETED` via `complete(id)` — irreversible in Phase I
- Creating a task always starts at `PENDING`
- No `COMPLETED → PENDING` transition (can be added in Phase II if needed)

## Validation Rules

Derived from spec functional requirements:

| Rule | Source | Enforcement |
|------|--------|-------------|
| Title must not be empty or whitespace-only | FR-007 | `Task.__post_init__` or `TaskList.add()` |
| Title must be trimmed | Edge Cases spec | `TaskList.add()` / `TaskList.update()` |
| ID must exist before update/delete/complete | FR-008 | `TaskList.get_by_id()` returns `None` → raise `TaskNotFoundError` |
| IDs are sequential starting from 1 | FR-002 | `TaskList._next_id` counter |
| No crashes on invalid input | FR-009 | Exception handling at CLI boundary |

## Exceptions

| Exception | Raised When |
|-----------|-------------|
| `EmptyTitleError` | Title is empty or whitespace-only on create/update |
| `TaskNotFoundError` | Referenced ID does not exist for update/delete/complete |
| `TaskAlreadyCompletedError` | Complete called on a task already in COMPLETED status |

All exceptions inherit from a common `TodoAppError` base for clean catching at the CLI layer.
