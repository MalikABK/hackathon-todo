# Feature Specification: CLI Todo App (Phase I)

**Feature Branch**: `001-cli-todo-app`
**Created**: 2026-04-07
**Status**: Draft
**Input**: User description: "Build a Phase I CLI Todo App with in-memory storage supporting create, read, update, delete, list, and complete operations for managing tasks via command-line interface"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and List Tasks (Priority: P1)

A user opens the CLI and wants to quickly add tasks and see all their existing tasks. They type a command to create a task with a title, and another command to list everything they've added. This is the core loop: add tasks, see tasks.

**Why this priority**: Without the ability to create and view tasks, the application provides zero value. This is the absolute minimum viable product.

**Independent Test**: Can be fully tested by creating multiple tasks via the CLI, listing them, and verifying all created tasks appear with correct titles. Delivers the core value of "a task list you can add to and review."

**Acceptance Scenarios**:

1. **Given** the task list is empty, **When** the user creates a task with title "Buy groceries", **Then** the task is stored and a confirmation message is shown with the task's unique ID.
2. **Given** the user has created several tasks, **When** the user lists all tasks, **Then** every task is displayed with its ID, title, and current status (pending/completed).
3. **Given** the user attempts to create a task with an empty title, **Then** the system rejects the input and displays a clear error message.

---

### User Story 2 - Mark Task as Complete (Priority: P2)

A user has tasks in their list and wants to mark one as done. They reference the task by its ID and issue a complete command. The task's status changes and this is reflected when listing tasks.

**Why this priority**: Completing tasks is the second most fundamental todo app operation. It provides the satisfaction of crossing items off and lets users track progress.

**Independent Test**: Can be fully tested by creating a task, marking it complete by ID, listing tasks, and verifying the status changed to "completed."

**Acceptance Scenarios**:

1. **Given** a task exists with status "pending", **When** the user marks it complete by its ID, **Then** the task status changes to "completed" and a confirmation is shown.
2. **Given** a task is already "completed", **When** the user attempts to mark it complete again, **Then** the system notifies the user that the task is already completed.
3. **Given** no task exists with the provided ID, **When** the user attempts to mark it complete, **Then** the system returns an error indicating the ID was not found.

---

### User Story 3 - Update and Delete Tasks (Priority: P3)

A user wants to correct a task title they mistyped, or remove a task they no longer need. They issue update or delete commands referencing the task by ID.

**Why this priority**: Editing and deleting are important but secondary to creating, viewing, and completing. The app is still functional without these (workaround: create a new task, ignore the old one).

**Independent Test**: Can be fully tested by creating a task, updating its title, verifying the change in the list, then deleting it and confirming it no longer appears.

**Acceptance Scenarios**:

1. **Given** a task exists with title "Old title", **When** the user updates it to "New title", **Then** the task title is changed and the updated title appears in subsequent listings.
2. **Given** a task exists, **When** the user deletes it by ID, **Then** the task is removed and no longer appears in the task list.
3. **Given** the user attempts to delete a non-existent task ID, **Then** the system returns an error indicating the ID was not found.
4. **Given** the user attempts to update a task with an empty title, **Then** the system rejects the input and displays a clear error message.

---

### Edge Cases

- **Empty input**: User runs a command without providing required arguments (e.g., `create` with no title). System shows usage help.
- **Invalid ID format**: User provides a non-numeric or malformed ID. System returns a clear error.
- **Non-existent ID**: User references an ID that doesn't exist for update, delete, or complete operations. System returns "task not found" error.
- **Whitespace-only title**: User provides a title consisting only of spaces. System trims and rejects if empty after trimming.
- **Duplicate titles**: Multiple tasks with the same title are allowed (this is valid — users may have similar tasks).
- **Large number of tasks**: System handles 100+ tasks in memory without noticeable slowdown in list output.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create a new task by providing a title string and an optional description.
- **FR-002**: System MUST assign a unique, sequential numeric ID to each newly created task (starting from 1).
- **FR-003**: System MUST allow users to list all tasks, displaying ID, title, description, and status (pending/completed).
- **FR-004**: System MUST allow users to mark a task as completed by referencing its ID.
- **FR-004b**: System MUST allow users to toggle a task between completed and pending by referencing its ID.
- **FR-005**: System MUST allow users to update a task's title and optionally its description by referencing its ID.
- **FR-006**: System MUST allow users to delete a task by referencing its ID.
- **FR-007**: System MUST validate that task titles are not empty or whitespace-only before creating or updating.
- **FR-008**: System MUST validate that a task ID exists before performing update, delete, or complete operations.
- **FR-009**: System MUST handle all invalid inputs gracefully without crashing, displaying user-friendly error messages.
- **FR-010**: System MUST store all tasks in memory (list/dictionary) — no file or database persistence in Phase I.
- **FR-011**: System MUST provide a CLI entry point (`main.py`) that dispatches commands to the appropriate service.
- **FR-012**: System MUST separate CLI argument parsing (`cli.py`) from business logic (`services.py`) and data models (`models.py`).

### Key Entities

- **Task**: Represents a single todo item. Attributes: `id` (unique integer), `title` (non-empty string), `description` (optional string, defaults empty), `status` (enum: pending | completed), `created_at` (timestamp of creation).
- **TaskList**: Represents the in-memory collection of all Task objects. Supports add, remove, update, list, complete, toggle, and find-by-id operations.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task and see it listed within a single CLI session in under 1 second per operation.
- **SC-002**: Users can successfully complete all CRUD operations (create, read, update, delete, complete, toggle) without any unhandled exceptions or crashes.
- **SC-003**: All functional requirements (FR-001 through FR-012) are satisfied and verifiable through manual testing or automated tests.
- **SC-004**: Code structure strictly follows the constitution's mandated layout (`models.py`, `services.py`, `cli.py`, `main.py`) with no cross-layer violations.
- **SC-005**: Invalid inputs (empty title, non-existent ID, empty arguments) all produce clear error messages — zero crashes from bad input.

### Assumptions

- Phase I is a single-session CLI app — tasks exist only during the running process and are lost when the program exits (in-memory only per constitution).
- The CLI runs on Python 3.10+ on a standard terminal (Linux/macOS/Windows).
- No authentication, multi-user support, or network access is needed in Phase I.
- Task IDs are simple integers assigned sequentially (1, 2, 3…).
