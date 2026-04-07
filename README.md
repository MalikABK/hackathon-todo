# CLI Todo App (Phase I)

A minimal, spec-driven CLI todo application built with Python 3.10+ and zero third-party dependencies.

## Quick Start

```bash
# Install dependencies (uv)
uv venv .venv
source .venv/bin/activate
uv pip install pytest

# Run the app
python src/main.py create "Buy groceries"
python src/main.py list
python src/main.py complete 1
python src/main.py update 1 "Buy groceries and cook dinner"
python src/main.py delete 1
python src/main.py --help

# Run tests
.venv/bin/pytest tests/ -v
```

## Features

| Command | Description | Example |
|---------|-------------|---------|
| `create <title>` | Create a new task | `python src/main.py create "Task"` |
| `list` | List all tasks | `python src/main.py list` |
| `complete <id>` | Mark a task as completed | `python src/main.py complete 1` |
| `update <id> <title>` | Update a task's title | `python src/main.py update 1 "New"` |
| `delete <id>` | Delete a task | `python src/main.py delete 1` |

## Architecture

```
main.py ──► cli.py (argparse, dispatch)
              │
              ▼
           services.py (CRUD logic, validation)
              │
              ▼
           models.py (Task, TaskList, exceptions)
```

| Layer | File | Responsibility |
|-------|------|----------------|
| Entry point | `src/main.py` | Creates TaskList, dispatches commands |
| CLI interface | `src/cli.py` | Argument parsing, output formatting, error handling |
| Business logic | `src/services.py` | CRUD + complete operations |
| Data model | `src/models.py` | Task dataclass, TaskList collection, exceptions |

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── models.py        # Task, TaskList, exceptions
│   ├── services.py      # CRUD + complete functions
│   ├── cli.py           # argparse, dispatch, formatting
│   └── main.py          # Entry point
├── tests/
│   ├── __init__.py
│   ├── test_models.py   # 29 tests
│   ├── test_services.py # 10 tests
│   └── test_cli.py      # 17 tests
├── specs/001-cli-todo-app/
│   ├── spec.md          # Feature specification
│   ├── plan.md          # Implementation plan
│   ├── tasks.md         # Task breakdown (73 tasks, all complete)
│   ├── research.md      # Technical research
│   ├── data-model.md    # Data model design
│   ├── quickstart.md    # Quick start guide
│   ├── contracts/       # CLI command contracts
│   └── checklists/      # Quality checklists
├── pyproject.toml       # pytest configuration
├── .gitignore
├── .venv/               # Virtual environment (uv)
└── README.md
```

## Requirements

- Python 3.10+
- `uv` (package manager) — or `pip install pytest` manually

## Development Workflow

This project follows **Spec-Driven Development (SDD)**:

1. **Constitution** → Principles at `.specify/memory/constitution.md`
2. **Specification** → `specs/001-cli-todo-app/spec.md`
3. **Plan** → `specs/001-cli-todo-app/plan.md`
4. **Tasks** → `specs/001-cli-todo-app/tasks.md`
5. **Implementation** → This code

No code is written without a spec. Every change maps to a task.

## Phase Roadmap

| Phase | Scope | Status |
|-------|-------|--------|
| **Phase I** | CLI + in-memory storage | ✅ Complete |
| **Phase II** | API + persistent database | Planned |
| **Phase III** | AI Agent integration | Planned |
| **Phase IV** | Kubernetes deployment | Planned |
| **Phase V** | Distributed system | Planned |

## Test Results

```
56 passed in 4.29s
```

- `tests/test_models.py`: 29 tests (Task, TaskList CRUD, serialization)
- `tests/test_services.py`: 10 tests (CRUD + complete service layer)
- `tests/test_cli.py`: 17 tests (argparse, dispatch, output, exit codes)
