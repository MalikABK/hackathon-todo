<!--
  SYNC IMPACT REPORT
  ====================
  Version change: 0.0.0 (none) → 1.0.0 (initial ratification)
  Bump rationale: Initial constitution — MAJOR version 1.0.0 for first adoption.

  Modified principles: N/A (first version)

  Added sections:
    - Core Principles (5 principles: Spec-First, Single Source of Truth, Task-Based Execution,
      Simplicity First, Separation of Concerns)
    - Architecture Constraints (in-memory storage, Python 3.10+, project structure)
    - Coding Standards
    - Error Handling Rules
    - Validation Rules
    - Evolution Rule (Phase I → V roadmap)
    - Agent Behavior Rules
    - Definition of Done
    - Forbidden Actions
    - Governance

  Templates requiring updates:
    - .specify/templates/plan-template.md — Constitution Check section: ⚠ pending (will be populated by /sp.plan)
    - .specify/templates/spec-template.md — No changes needed; aligns with spec-first principle ✅
    - .specify/templates/tasks-template.md — Task-based execution principle reflected ✅

  Follow-up TODOs:
    - TODO(RATIFICATION_DATE): Set formal ratification date once constitution is approved (currently set to today as provisional).
-->

# hackathon-todo Constitution

## Core Principles

### I. Spec-First Development (NON-NEGOTIABLE)
No code is written without a specification. Specs must be complete before implementation begins. If a spec is unclear or ambiguous, STOP and refine it before proceeding. Code without a corresponding spec is forbidden.

### II. Single Source of Truth
Specifications are the single source of truth for all implementation work. Code must match specs exactly — no assumptions, no deviations, no implicit behavior. Any discrepancy between code and spec is a defect.

### III. Task-Based Execution
Every unit of implementation must map to a defined task in the tasks document. No "random coding" — each function, module, or feature must trace back to a spec requirement through a task. Tasks are the bridge between spec and code.

### IV. Simplicity First
Start simple. Phase I uses in-memory storage only — no databases, no unnecessary complexity. Avoid over-engineering. YAGNI (You Aren't Gonna Need It) applies: do not build for future phases until the current phase is complete and validated.

### V. Separation of Concerns
CLI interface logic must be separate from business logic. Data handling must be separate from UI/presentation. The project structure must be modular: `models.py`, `services.py`, `cli.py`, `main.py` — each with a single, clear responsibility.

## Architecture Constraints

### Data Storage
Phase I MUST use in-memory storage (list or dictionary). No external databases, file-based persistence, or caching layers are permitted until Phase II.

### Language & Tools
- Python 3.10+
- Type hints required where applicable
- Code generated via AI agent (Claude Code / Qwen Code) following spec-driven workflow

### Project Structure
```
src/
  ├── models.py        # Task data model
  ├── services.py      # Business logic (CRUD operations)
  ├── cli.py           # CLI interface (user interaction)
  └── main.py          # Entry point
```

## Coding Standards

- Use clear, descriptive function and variable names.
- Use type hints on all function signatures where possible.
- Handle errors explicitly — no silent failures.
- Avoid duplicated logic — extract shared behavior into reusable functions.
- Keep functions focused on a single responsibility.

## Error Handling Rules

The system MUST handle the following gracefully (no crashes, clear error messages):
- Invalid task IDs
- Empty or missing input
- Operations on non-existent tasks
- Any unexpected user input

## Validation Rules

Before any operation is processed, the system MUST validate:
- Task title must not be empty.
- Task ID must exist before update/delete/complete operations.
- All user inputs must be validated before processing.

## Evolution Rule

This system is designed to evolve across phases. Design decisions MUST remain extendable:

| Phase | Scope |
|-------|-------|
| Phase I | CLI + in-memory storage |
| Phase II | API + persistent database |
| Phase III | AI Agent integration |
| Phase IV | Kubernetes deployment |
| Phase V | Distributed system |

Architecture for Phase I must not preclude evolution to later phases.

## Agent Behavior Rules (NON-NEGOTIABLE)

AI agents operating in this project MUST:
- Read the spec before writing any code.
- Refuse to code if a spec does not exist or is incomplete.
- Follow the architecture defined in the plan strictly.
- Keep code modular and separable.
- Not add features, endpoints, or behavior not specified in the spec.
- Not skip task breakdown — every change maps to a task.

## Definition of Done

A feature is considered complete ONLY when ALL of the following are true:
- Implementation matches the specification exactly.
- All functional requirements from the spec are satisfied.
- All architecture constraints are followed.
- Code is clean, readable, and modular.
- Error handling covers edge cases defined in the spec.

## Forbidden Actions

The following are explicitly forbidden:
- Writing code without a corresponding spec.
- Skipping the task breakdown step.
- Adding features not requested in the spec ("gold plating").
- Changing architecture without updating the plan and spec first.
- Hardcoding secrets, tokens, or credentials.

## Governance

This constitution supersedes all other development practices in this project. Amendments require:
1. A proposed change documented with rationale.
2. Version bump following semantic versioning (MAJOR for breaking governance changes, MINOR for new principles, PATCH for clarifications).
3. Review and approval by the project owner.
4. Propagation of changes to dependent templates (`plan-template.md`, `spec-template.md`, `tasks-template.md`).

All PR reviews MUST verify constitution compliance before merge. Complexity introduced in code MUST be justified against the Simplicity First principle.

**Version**: 1.0.0 | **Ratified**: 2026-04-07 | **Last Amended**: 2026-04-07
