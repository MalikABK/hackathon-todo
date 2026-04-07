# CLI Contract: Todo App (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2026-04-07

## Entry Point

```
python src/main.py <command> [arguments]
```

## Commands

### `create <title>`

Creates a new task with the given title.

| Aspect | Detail |
|--------|--------|
| **Arguments** | `title` (required, string, non-empty) |
| **Success Output** | `Task created: [ID] - "title"` |
| **Success Exit Code** | `0` |
| **Error Output** | `Error: Title cannot be empty.` |
| **Error Exit Code** | `1` |

**Examples**:
```
$ python src/main.py create "Buy groceries"
Task created: 1 - "Buy groceries"

$ python src/main.py create ""
Error: Title cannot be empty.
```

---

### `list`

Displays all tasks in a formatted table.

| Aspect | Detail |
|--------|--------|
| **Arguments** | None |
| **Success Output** | Formatted table: `ID  STATUS    TITLE` (one row per task) |
| **Empty Output** | `No tasks found.` |
| **Success Exit Code** | `0` |
| **Error Output** | N/A |
| **Error Exit Code** | `0` |

**Examples**:
```
$ python src/main.py list
ID  STATUS    TITLE
1   pending   Buy groceries
2   completed Write spec

$ python src/main.py list
No tasks found.
```

---

### `complete <id>`

Marks a task as completed.

| Aspect | Detail |
|--------|--------|
| **Arguments** | `id` (required, integer, must exist) |
| **Success Output** | `Task [ID] marked as completed.` |
| **Success Exit Code** | `0` |
| **Error Output** | `Error: Task with ID [ID] not found.` / `Error: Task [ID] is already completed.` |
| **Error Exit Code** | `1` |

**Examples**:
```
$ python src/main.py complete 1
Task 1 marked as completed.

$ python src/main.py complete 999
Error: Task with ID 999 not found.

$ python src/main.py complete 1
Error: Task 1 is already completed.
```

---

### `update <id> <new_title>`

Updates a task's title.

| Aspect | Detail |
|--------|--------|
| **Arguments** | `id` (required, integer, must exist), `new_title` (required, string, non-empty) |
| **Success Output** | `Task [ID] updated.` |
| **Success Exit Code** | `0` |
| **Error Output** | `Error: Task with ID [ID] not found.` / `Error: Title cannot be empty.` |
| **Error Exit Code** | `1` |

**Examples**:
```
$ python src/main.py update 1 "Buy groceries and cook dinner"
Task 1 updated.

$ python src/main.py update 999 "Something"
Error: Task with ID 999 not found.
```

---

### `delete <id>`

Deletes a task.

| Aspect | Detail |
|--------|--------|
| **Arguments** | `id` (required, integer, must exist) |
| **Success Output** | `Task [ID] deleted.` |
| **Success Exit Code** | `0` |
| **Error Output** | `Error: Task with ID [ID] not found.` |
| **Error Exit Code** | `1` |

**Examples**:
```
$ python src/main.py delete 1
Task 1 deleted.

$ python src/main.py delete 999
Error: Task with ID 999 not found.
```

---

### `--help` / no command

Displays usage information.

| Aspect | Detail |
|--------|--------|
| **Output** | List of available commands with brief descriptions |
| **Exit Code** | `0` |

## Error Taxonomy

| Error | Exit Code | Trigger |
|-------|-----------|---------|
| Empty title | 1 | Create or update with empty/whitespace title |
| Task not found | 1 | Complete, update, or delete with non-existent ID |
| Task already completed | 1 | Complete called on a COMPLETED task |
| Invalid arguments | 1 | Missing required arguments or malformed input |
| Unknown command | 2 | argparse default behavior |
