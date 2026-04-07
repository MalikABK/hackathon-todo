# Implementation Plan: CLI Todo App (Phase I)

**Branch**: `001-cli-todo-app` | **Date**: 2026-04-07 | **Spec**: [specs/001-cli-todo-app/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

## Summary

Build a Python CLI Todo application (Phase I) with in-memory storage supporting full CRUD operations and task completion. The app uses `argparse` for CLI argument parsing, a clean layered architecture (`models.py` → `services.py` → `cli.py` → `main.py`), and validates all inputs per the constitution. The design is intentionally minimal to allow evolution to Phase II (API + DB) without structural changes.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `argparse` (stdlib) for CLI parsing, `dataclasses` (stdlib) for Task model, `datetime` (stdlib) for timestamps. No third-party packages in Phase I.
**Storage**: In-memory list/dictionary. No persistence beyond process lifetime.
**Testing**: `pytest` for unit tests. `unittest` (stdlib) acceptable if pytest unavailable.
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows terminal)
**Project Type**: Single-project CLI application
**Performance Goals**: Each operation (create, list, update, delete, complete) completes in under 1 second for 100+ tasks.
**Constraints**: Single process, no network I/O, no external dependencies, no file persistence.
**Scale/Scope**: Single user, session-scoped data, 100+ tasks in memory.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Constitution Principle | Status | Notes |
|------|----------------------|--------|-------|
| Spec exists | I. Spec-First Development | ✅ PASS | spec.md complete before planning |
| No code yet | I. Spec-First Development | ✅ PASS | Plan precedes implementation |
| In-memory only | IV. Simplicity First, Architecture Constraints | ✅ PASS | No DB, no file storage in Phase I |
| Python 3.10+ | Language & Tools constraint | ✅ PASS | Confirmed in Technical Context |
| 4-file structure | V. Separation of Concerns, Project Structure | ✅ PASS | models.py, services.py, cli.py, main.py |
| Type hints | Coding Standards | ✅ PASS | All function signatures will have type hints |
| No gold plating | Forbidden Actions | ✅ PASS | Scope limited to CRUD + complete per spec |
| Task-based execution | III. Task-Based Execution | ⏳ PENDING | Will be satisfied by /sp.tasks output |

**Gate Result: PASS** — All constitution gates satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models.py        # Task dataclass, TaskStatus enum, TaskList collection
├── services.py      # CRUD + complete business logic, input validation
├── cli.py           # argparse setup, command dispatch, output formatting
└── main.py          # Entry point — parses sys.argv, calls cli.py

tests/
├── test_models.py   # Unit tests for Task, TaskList
├── test_services.py # Unit tests for CRUD + complete operations
└── test_cli.py      # Unit tests for CLI argument parsing and output
```

**Structure Decision**: Single-project Python CLI (Option 1 from template). The constitution mandates exactly 4 source files in `src/`. Tests sit in a parallel `tests/` directory. This structure cleanly separates concerns and allows Phase II to add a `backend/` or `api/` layer without restructuring `src/`.

## Complexity Tracking

> No constitution violations to justify. The 4-file structure is constitution-mandated and minimal.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
