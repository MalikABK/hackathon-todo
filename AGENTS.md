# AGENTS.md — Agent Instructions for hackathon-todo

This file provides instructions for AI coding agents working on this project.

## Project Overview

CLI Todo App (Phase I) — a Python CLI application with in-memory storage supporting full CRUD operations and task completion. Zero third-party dependencies.

## Critical Rules

1. **Read the spec before coding** — `specs/001-cli-todo-app/spec.md` is the single source of truth.
2. **No code without a spec** — If a feature isn specified, STOP and ask for a spec.
3. **No gold plating** — Do not add features not in the spec.
4. **Follow the architecture** — `models.py` → `services.py` → `cli.py` → `main.py`. Do not add layers.
5. **Phase I is in-memory only** — No file I/O, no database, no network.

## Tech Stack

- **Language**: Python 3.10+
- **Package manager**: `uv`
- **Testing**: `pytest`
- **Dependencies**: stdlib only (`argparse`, `dataclasses`, `datetime`, `enum`)

## Code Conventions

- Type hints on all function signatures.
- Docstrings on all public functions and classes.
- Clear, descriptive names (no abbreviations, no single-letter variables except loop indices).
- Handle errors explicitly — no silent failures.
- Custom exceptions in `models.py` inherit from `TodoAppError`.
- CLI layer catches exceptions and prints user-friendly messages; services/models never print.

## Project Structure

```
src/
  ├── models.py        # Task, TaskList, exceptions, serialization hooks
  ├── services.py      # CRUD + complete functions (thin wrappers around TaskList)
  ├── cli.py           # argparse setup, dispatch_command, format_task_table
  └── main.py          # Entry point
tests/
  ├── test_models.py   # Model + collection tests
  ├── test_services.py # Service layer tests
  └── test_cli.py      # CLI argument parsing + output tests
```

## Running Commands

```bash
# Activate environment
source .venv/bin/activate

# Run app
python src/main.py create "Task"
python src/main.py list

# Run tests
.venv/bin/pytest tests/ -v

# Run single test
.venv/bin/pytest tests/ -v -k "test_create"
```

## Adding New Features

1. Create feature spec in `specs/NNN-feature-name/spec.md`
2. Run `/sp.plan` → `/sp.tasks` → `/sp.implement`
3. Write tests first (TDD), then implementation
4. Run full test suite before marking tasks complete
5. Update `tasks.md` checkboxes as you go

## Future Phases (Do NOT implement without a spec)

| Phase | Scope |
|-------|-------|
| Phase II | REST API + persistent database (PostgreSQL/SQLite) |
| Phase III | AI Agent integration |
| Phase IV | Kubernetes deployment |
| Phase V | Distributed system |

The `TaskList.to_dict()` / `from_dict()` methods in `models.py` are Phase II hooks — they exist but are not called in Phase I.
