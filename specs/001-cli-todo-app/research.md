# Research: CLI Todo App (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2026-04-07

## Decision: CLI Argument Parser

**Chosen**: `argparse` (Python standard library)

**Rationale**: 
- Built into Python 3.10+, zero dependencies
- Supports subcommands naturally (`todo create`, `todo list`, etc.)
- Auto-generates `--help` output
- Handles type coercion, required/optional arguments
- Well-documented, stable API

**Alternatives considered**:
- `click`: Third-party, richer features but violates Simplicity First (Phase I has no need for decorators, callbacks, or plugins)
- `typer`: Modern, type-hint driven, but adds dependency
- Manual `sys.argv` parsing: Too error-prone, duplicates argparse functionality

## Decision: Data Model Representation

**Chosen**: `dataclasses.dataclass` for Task model

**Rationale**:
- Python 3.10+ native support
- Auto-generates `__init__`, `__repr__`, `__eq__`
- Supports type hints natively
- Clear, readable, and testable
- Extensible — adding fields for Phase II (e.g., `due_date`, `priority`) is trivial

**Alternatives considered**:
- Plain dict: Less structured, no type safety, harder to validate
- `namedtuple`: Immutable, no default values, less flexible
- Pydantic BaseModel: Third-party dependency, overkill for Phase I

## Decision: In-Memory Storage Structure

**Chosen**: `list[Task]` with sequential integer ID assignment

**Rationale**:
- Simplest possible structure matching spec requirements
- Sequential IDs map directly to list indices (or a counter)
- Easy to iterate for listing, easy to search by ID
- No external dependencies

**Alternatives considered**:
- `dict[int, Task]`: Slightly faster lookups (O(1) vs O(n)), but list is sufficient for 100+ tasks and easier to maintain insertion order for listing
- Custom collection class: Adds complexity without Phase I benefit

## Decision: Error Handling Strategy

**Chosen**: Custom exception classes + try/except at CLI boundary

**Rationale**:
- Business logic (`services.py`) raises typed exceptions (`TaskNotFoundError`, `EmptyTitleError`)
- CLI layer (`cli.py`) catches exceptions and prints user-friendly messages
- Clean separation: services don't know about output formatting
- Matches Separation of Concerns principle

**Alternatives considered**:
- Return codes/error strings: Less Pythonic, harder to distinguish error types
- Print errors directly in services: Violates separation of concerns

## Decision: CLI Command Design

**Chosen**: Subcommand pattern — `todo <command> [args]`

| Command | Arguments | Description |
|---------|-----------|-------------|
| `create` | `<title>` | Create a new task |
| `list` | _(none)_ | List all tasks |
| `complete` | `<id>` | Mark task as completed |
| `update` | `<id> <new_title>` | Update task title |
| `delete` | `<id>` | Delete a task |

**Rationale**: Matches standard CLI conventions (git, docker, kubectl). Each subcommand maps 1:1 to a service method.

**Alternatives considered**:
- Flag-based: `todo --create --title "..."` — more verbose, less intuitive
- Interactive mode: Requires readline/curses, adds complexity, not in spec

## Decision: Output Formatting

**Chosen**: Plain text with aligned columns for `list` command

```
ID  STATUS    TITLE
1   pending   Buy groceries
2   completed Write spec
```

**Rationale**: Human-readable, no dependencies, sufficient for Phase I. Easy to replace with JSON output (`--json` flag) in Phase II.

**Alternatives considered**:
- Rich/table: Third-party dependency
- JSON output only: Not human-friendly for CLI use

## Decision: Phase II Extensibility Hook

**Chosen**: The `TaskList` class in `models.py` will expose a `to_dict()` and `from_dict()` method (even if unused in Phase I). This prepares for JSON serialization in Phase II (API + DB) without adding any runtime persistence.

**Rationale**: Zero cost in Phase I (methods defined but not called), eliminates a breaking change in Phase II.

## Resolved NEEDS CLARIFICATION

All technical context values were resolved from the constitution and spec — no outstanding clarifications.
