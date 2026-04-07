# Tasks: CLI Todo App (Phase I)

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-contract.md, research.md, quickstart.md

**Tests**: Tests ARE included — the constitution mandates Test-First (Red-Green-Refactor) and all functional requirements must be verifiable.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Source: `src/models.py`, `src/services.py`, `src/cli.py`, `src/main.py`
- Tests: `tests/test_models.py`, `tests/test_services.py`, `tests/test_cli.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `src/` and `tests/` directories at repository root
- [x] T002 [P] Create empty `src/__init__.py` and `tests/__init__.py`
- [x] T003 [P] Create `pytest.ini` or `pyproject.toml` with pytest configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 [P] Define `TodoAppError` base exception in `src/models.py`
- [x] T005 [P] Define `EmptyTitleError`, `TaskNotFoundError`, `TaskAlreadyCompletedError` exceptions in `src/models.py`
- [x] T006 [P] Define `TaskStatus` enum (PENDING, COMPLETED) in `src/models.py`
- [x] T007 Create `Task` dataclass with `id`, `title`, `status`, `created_at` fields in `src/models.py`
- [x] T008 Create `TaskList` class with `tasks` list and `_next_id` counter in `src/models.py`
- [x] T009 Implement `TaskList.__init__()` with empty tasks list and ID counter = 1
- [x] T010 Create `create_task(title)` stub in `src/services.py` — accepts title, returns Task
- [x] T011 Create `list_tasks()` stub in `src/services.py` — returns list[Task]
- [x] T012 Create `complete_task(id)` stub in `src/services.py` — accepts ID, returns Task
- [x] T013 Create `update_task(id, new_title)` stub in `src/services.py` — accepts ID + title, returns Task
- [x] T014 Create `delete_task(id)` stub in `src/services.py` — accepts ID, returns None
- [x] T015 Implement `create_parser()` in `src/cli.py` — argparse setup with subcommands (create, list, complete, update, delete)
- [x] T016 Implement `dispatch_command(args)` stub in `src/cli.py` — parses subcommand, calls appropriate service
- [x] T017 Implement `format_task_table(tasks)` in `src/cli.py` — returns formatted string with ID, STATUS, TITLE columns
- [x] T018 Implement `main()` entry point in `src/main.py` — creates TaskList, calls create_parser, calls dispatch_command

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Create and List Tasks (Priority: P1) 🎯 MVP

**Goal**: User can create tasks with titles and list all tasks with ID, status, and title. This is the core loop.

**Independent Test**: Create multiple tasks via CLI, list them, verify all appear with correct titles. Empty title is rejected.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T019 [P] [US1] Test `Task` creation with valid title in `tests/test_models.py`
- [x] T020 [P] [US1] Test `Task` auto-assigns PENDING status and datetime in `tests/test_models.py`
- [x] T021 [P] [US1] Test `TaskList.add()` assigns sequential IDs starting from 1 in `tests/test_models.py`
- [x] T022 [P] [US1] Test `TaskList.add()` raises `EmptyTitleError` for empty/whitespace title in `tests/test_models.py`
- [x] T023 [P] [US1] Test `TaskList.list_all()` returns all tasks in insertion order in `tests/test_models.py`
- [x] T024 [US1] Test `create_task` service calls `TaskList.add()` and returns created Task in `tests/test_services.py`
- [x] T025 [US1] Test `list_tasks` service calls `TaskList.list_all()` and returns list[Task] in `tests/test_services.py`
- [x] T026 [US1] Test `create_parser` recognizes `create <title>` subcommand in `tests/test_cli.py`
- [x] T027 [US1] Test `create_parser` recognizes `list` subcommand in `tests/test_cli.py`
- [x] T028 [US1] Test CLI prints `Task created: [ID] - "title"` on successful create in `tests/test_cli.py`
- [x] T029 [US1] Test CLI prints `Error: Title cannot be empty.` for empty title in `tests/test_cli.py`
- [x] T030 [US1] Test CLI prints formatted table for `list` with tasks in `tests/test_cli.py`
- [x] T031 [US1] Test CLI prints `No tasks found.` when list is empty in `tests/test_cli.py`

### Implementation for User Story 1

- [x] T032 [US1] Implement `TaskList.add(title)` — validates title, creates Task with sequential ID, appends to list, returns Task in `src/models.py`
- [x] T033 [US1] Implement `TaskList.list_all()` — returns `self.tasks` in `src/models.py`
- [x] T034 [US1] Implement `create_task(title)` in `src/services.py` — calls `TaskList.add()`, returns Task
- [x] T035 [US1] Implement `list_tasks()` in `src/services.py` — calls `TaskList.list_all()`, returns list
- [x] T036 [US1] Implement `create` subcommand handler in `dispatch_command()` in `src/cli.py` — validates title, calls `create_task`, prints confirmation
- [x] T037 [US1] Implement `list` subcommand handler in `dispatch_command()` in `src/cli.py` — calls `list_tasks`, calls `format_task_table`, prints output
- [x] T038 [US1] Wire `main.py` to create global TaskList, parse args, dispatch, exit with correct code in `src/main.py`

**Checkpoint**: At this point, User Story 1 should be fully functional — `python src/main.py create "task"` and `python src/main.py list` both work.

---

## Phase 4: User Story 2 — Mark Task as Complete (Priority: P2)

**Goal**: User can mark a task as completed by ID. Status changes from pending to completed.

**Independent Test**: Create a task, mark it complete by ID, list tasks, verify status shows "completed". Already-completed and non-existent IDs produce errors.

### Tests for User Story 2 ⚠️

- [x] T039 [P] [US2] Test `TaskList.complete(id)` changes status to COMPLETED in `tests/test_models.py`
- [x] T040 [P] [US2] Test `TaskList.complete(id)` raises `TaskNotFoundError` for non-existent ID in `tests/test_models.py`
- [x] T041 [P] [US2] Test `TaskList.complete(id)` raises `TaskAlreadyCompletedError` for completed task in `tests/test_models.py`
- [x] T042 [US2] Test `complete_task` service calls `TaskList.complete()` and returns updated Task in `tests/test_services.py`
- [x] T043 [US2] Test CLI prints `Task [ID] marked as completed.` on success in `tests/test_cli.py`
- [x] T044 [US2] Test CLI prints `Error: Task with ID [ID] not found.` for non-existent ID in `tests/test_cli.py`
- [x] T045 [US2] Test CLI prints `Error: Task [ID] is already completed.` for already-completed task in `tests/test_cli.py`

### Implementation for User Story 2

- [x] T046 [US2] Implement `TaskList.get_by_id(id)` — returns Task or None in `src/models.py`
- [x] T047 [US2] Implement `TaskList.complete(id)` — finds task, checks status, sets COMPLETED or raises in `src/models.py`
- [x] T048 [US2] Implement `complete_task(id)` in `src/services.py` — calls `TaskList.complete()`, returns Task
- [x] T049 [US2] Implement `complete` subcommand handler in `dispatch_command()` in `src/cli.py` — parses ID, calls `complete_task`, prints confirmation or error
- [x] T050 [US2] Add exception handling for `TaskAlreadyCompletedError` in CLI layer in `src/cli.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 — Update and Delete Tasks (Priority: P3)

**Goal**: User can update a task's title and delete a task by ID.

**Independent Test**: Create a task, update its title, verify change in list, delete it, confirm it no longer appears.

### Tests for User Story 3 ⚠️

- [x] T051 [P] [US3] Test `TaskList.update(id, new_title)` changes title in `tests/test_models.py`
- [x] T052 [P] [US3] Test `TaskList.update(id, new_title)` raises `TaskNotFoundError` for non-existent ID in `tests/test_models.py`
- [x] T053 [P] [US3] Test `TaskList.update(id, "")` raises `EmptyTitleError` for empty title in `tests/test_models.py`
- [x] T054 [P] [US3] Test `TaskList.delete(id)` removes task from list in `tests/test_models.py`
- [x] T055 [P] [US3] Test `TaskList.delete(id)` raises `TaskNotFoundError` for non-existent ID in `tests/test_models.py`
- [x] T056 [US3] Test `update_task` service calls `TaskList.update()` and returns updated Task in `tests/test_services.py`
- [x] T057 [US3] Test `delete_task` service calls `TaskList.delete()` and returns None in `tests/test_services.py`
- [x] T058 [US3] Test CLI prints `Task [ID] updated.` on successful update in `tests/test_cli.py`
- [x] T059 [US3] Test CLI prints `Task [ID] deleted.` on successful delete in `tests/test_cli.py`
- [x] T060 [US3] Test CLI handles missing arguments for update/delete subcommands in `tests/test_cli.py`

### Implementation for User Story 3

- [x] T061 [US3] Implement `TaskList.update(id, new_title)` — finds task, validates title, updates title or raises in `src/models.py`
- [x] T062 [US3] Implement `TaskList.delete(id)` — finds task, removes from list or raises in `src/models.py`
- [x] T063 [US3] Implement `update_task(id, new_title)` in `src/services.py` — calls `TaskList.update()`, returns Task
- [x] T064 [US3] Implement `delete_task(id)` in `src/services.py` — calls `TaskList.delete()`, returns None
- [x] T065 [US3] Implement `update` subcommand handler in `dispatch_command()` in `src/cli.py` — parses ID + title, calls `update_task`, prints confirmation or error
- [x] T066 [US3] Implement `delete` subcommand handler in `dispatch_command()` in `src/cli.py` — parses ID, calls `delete_task`, prints confirmation or error

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T067 [P] Add `TaskList.to_dict()` serialization method in `src/models.py` (Phase II hook)
- [x] T068 [P] Add `TaskList.from_dict(data)` deserialization method in `src/models.py` (Phase II hook)
- [x] T069 Implement `--help` output with all commands and descriptions in `src/cli.py`
- [x] T070 Verify all error paths return correct exit codes (0 for success, 1 for app errors, 2 for argparse errors) in `src/main.py`
- [x] T071 Run full test suite and fix any failures
- [x] T072 Run `python src/main.py` against all quickstart.md scenarios and verify output
- [x] T073 Final code review — verify constitution compliance (type hints, separation of concerns, no gold plating)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — **BLOCKS all user stories**
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) — Depends on US1's `create_task` for test setup
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) — Depends on US1's `create_task` for test setup

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before CLI handlers
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003)
- Foundational model tasks can run in parallel (T004–T006: exceptions + enum)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Polish serialization tasks can run in parallel (T067, T068)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test Task creation with valid title" (T019)
Task: "Test Task auto-assigns PENDING status" (T020)
Task: "Test TaskList.add() assigns sequential IDs" (T021)
Task: "Test TaskList.add() raises EmptyTitleError" (T022)
Task: "Test TaskList.list_all() returns all tasks" (T023)

# After tests fail, implement models:
Task: "Implement TaskList.add(title)" (T032)
Task: "Implement TaskList.list_all()" (T033)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: Foundational (T004–T018)
3. Complete Phase 3: User Story 1 (T019–T038)
4. **STOP and VALIDATE**: `python src/main.py create "test"` and `python src/main.py list` work
5. Run tests: `pytest tests/ -v`
6. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP delivered!
3. Add User Story 2 → Test independently → Complete feature added
4. Add User Story 3 → Test independently → Full CRUD delivered
5. Polish → Edge cases, help, exit codes, constitution review

### Single Developer Strategy

1. Complete Setup + Foundational together
2. Implement tests for US1, watch them fail, then implement US1
3. Implement tests for US2, watch them fail, then implement US2
4. Implement tests for US3, watch them fail, then implement US3
5. Run full polish phase
6. Final test suite + quickstart validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing (Red-Green-Refactor)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total tasks: **73**
  - Setup: 3
  - Foundational: 15
  - US1 (P1): 20 (13 tests + 7 implementation)
  - US2 (P2): 12 (7 tests + 5 implementation)
  - US3 (P3): 16 (10 tests + 6 implementation)
  - Polish: 7
