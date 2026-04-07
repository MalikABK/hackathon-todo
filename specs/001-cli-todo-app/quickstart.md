# Quickstart: CLI Todo App (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2026-04-07

## Prerequisites

- Python 3.10+ installed and on PATH
- Terminal access (Linux, macOS, or Windows)

## Setup

```bash
# Navigate to project root
cd hackathon-todo

# Verify Python version
python3 --version  # Must be 3.10+

# (Optional) Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

## Run the Application

```bash
# Create a task
python3 src/main.py create "Buy groceries"

# Create another task
python3 src/main.py create "Write documentation"

# List all tasks
python3 src/main.py list

# Mark a task as completed
python3 src/main.py complete 1

# List again to verify status change
python3 src/main.py list

# Update a task title
python3 src/main.py update 2 "Write project documentation"

# Delete a task
python3 src/main.py delete 1

# Final list
python3 src/main.py list

# Show help
python3 src/main.py --help
```

## Expected Output

```
$ python3 src/main.py create "Buy groceries"
Task created: 1 - "Buy groceries"

$ python3 src/main.py create "Write documentation"
Task created: 2 - "Write documentation"

$ python3 src/main.py list
ID  STATUS    TITLE
1   pending   Buy groceries
2   pending   Write documentation

$ python3 src/main.py complete 1
Task 1 marked as completed.

$ python3 src/main.py list
ID  STATUS    TITLE
1   completed Buy groceries
2   pending   Write documentation
```

## Run Tests

```bash
# Install pytest (if not already installed)
pip install pytest

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` | Running from wrong directory | Run from project root, ensure `src/` is accessible |
| `python3: command not found` | Python not on PATH | Use `python` instead, or install Python 3.10+ |
| Tasks disappear between runs | Expected behavior | Phase I is in-memory only — data is lost when process exits |

## Architecture Overview

```
main.py ──► cli.py (argparse, dispatch)
              │
              ▼
           services.py (CRUD logic, validation)
              │
              ▼
           models.py (Task, TaskList, exceptions)
```

Each layer depends only on the layer below it. No circular dependencies.
