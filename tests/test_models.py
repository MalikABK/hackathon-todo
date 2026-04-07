"""Unit tests for Task and TaskList models."""

import pytest
from datetime import datetime

from src.models import (
    EmptyTitleError,
    Task,
    TaskList,
    TaskNotFoundError,
    TaskAlreadyCompletedError,
    TaskStatus,
)


# --- T019: Task creation with valid title ---

class TestTaskCreation:
    def test_task_created_with_valid_title(self):
        task = Task(id=1, title="Buy groceries")
        assert task.id == 1
        assert task.title == "Buy groceries"

    # --- T020: Task auto-assigns PENDING status and datetime ---

    def test_task_defaults_to_pending_status(self):
        task = Task(id=1, title="Test task")
        assert task.status == TaskStatus.PENDING

    def test_task_auto_assigns_created_at(self):
        before = datetime.now()
        task = Task(id=1, title="Test task")
        after = datetime.now()
        assert before <= task.created_at <= after


# --- T021: TaskList.add() assigns sequential IDs ---

class TestTaskListAdd:
    def test_first_task_gets_id_1(self):
        tl = TaskList()
        task = tl.add("First task")
        assert task.id == 1

    def test_second_task_gets_id_2(self):
        tl = TaskList()
        tl.add("First")
        task = tl.add("Second")
        assert task.id == 2

    def test_ids_are_sequential(self):
        tl = TaskList()
        ids = [tl.add(f"Task {i}").id for i in range(5)]
        assert ids == [1, 2, 3, 4, 5]

    # --- T022: TaskList.add() raises EmptyTitleError ---

    def test_empty_title_raises(self):
        tl = TaskList()
        with pytest.raises(EmptyTitleError):
            tl.add("")

    def test_whitespace_only_title_raises(self):
        tl = TaskList()
        with pytest.raises(EmptyTitleError):
            tl.add("   ")

    def test_title_is_trimmed(self):
        tl = TaskList()
        task = tl.add("  padded  ")
        assert task.title == "padded"


# --- T023: TaskList.list_all() returns all tasks in order ---

class TestTaskListAll:
    def test_empty_list_returns_empty(self):
        tl = TaskList()
        assert tl.list_all() == []

    def test_returns_tasks_in_insertion_order(self):
        tl = TaskList()
        t1 = tl.add("First")
        t2 = tl.add("Second")
        assert tl.list_all() == [t1, t2]

    def test_list_all_returns_copy_not_reference(self):
        tl = TaskList()
        tl.add("Task")
        result = tl.list_all()
        result.clear()
        assert len(tl.list_all()) == 1  # original unaffected


# --- T046 (moved from US2): TaskList.get_by_id() ---

class TestTaskListGetById:
    def test_returns_task_when_found(self):
        tl = TaskList()
        task = tl.add("Task")
        assert tl.get_by_id(1) == task

    def test_returns_none_when_not_found(self):
        tl = TaskList()
        assert tl.get_by_id(999) is None


# --- T047 (moved from US2): TaskList.complete() ---

class TestTaskListComplete:
    def test_changes_status_to_completed(self):
        tl = TaskList()
        task = tl.add("Task")
        result = tl.complete(task.id)
        assert result.status == TaskStatus.COMPLETED
        assert task.status == TaskStatus.COMPLETED

    def test_raises_for_non_existent_id(self):
        tl = TaskList()
        with pytest.raises(TaskNotFoundError):
            tl.complete(999)

    def test_raises_for_already_completed(self):
        tl = TaskList()
        task = tl.add("Task")
        tl.complete(task.id)
        with pytest.raises(TaskAlreadyCompletedError):
            tl.complete(task.id)


# --- T051-T053 (moved from US3): TaskList.update() ---

class TestTaskListUpdate:
    def test_updates_title(self):
        tl = TaskList()
        tl.add("Old title")
        task = tl.update(1, "New title")
        assert task.title == "New title"

    def test_raises_for_non_existent_id(self):
        tl = TaskList()
        with pytest.raises(TaskNotFoundError):
            tl.update(999, "New title")

    def test_raises_for_empty_title(self):
        tl = TaskList()
        tl.add("Task")
        with pytest.raises(EmptyTitleError):
            tl.update(1, "")

    def test_trims_whitespace(self):
        tl = TaskList()
        tl.add("Task")
        task = tl.update(1, "  trimmed  ")
        assert task.title == "trimmed"


# --- T054-T055 (moved from US3): TaskList.delete() ---

class TestTaskListDelete:
    def test_removes_task(self):
        tl = TaskList()
        tl.add("Task")
        tl.delete(1)
        assert tl.list_all() == []

    def test_raises_for_non_existent_id(self):
        tl = TaskList()
        tl.add("Task")
        with pytest.raises(TaskNotFoundError):
            tl.delete(999)


# --- T067-T068 (moved from Polish): Serialization ---

class TestTaskListSerialization:
    def test_to_dict_returns_list_of_dicts(self):
        tl = TaskList()
        tl.add("Task 1")
        tl.add("Task 2")
        data = tl.to_dict()
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[0]["title"] == "Task 1"
        assert data[0]["status"] == "pending"
        assert "created_at" in data[0]

    def test_from_dict_restores_tasks(self):
        tl = TaskList()
        tl.add("Task 1")
        tl.add("Task 2")
        data = tl.to_dict()
        restored = TaskList.from_dict(data)
        assert len(restored.tasks) == 2
        assert restored.tasks[0].title == "Task 1"
        assert restored.tasks[1].id == 2

    def test_from_dict_preserves_next_id(self):
        tl = TaskList()
        tl.add("Task 1")
        tl.add("Task 2")
        data = tl.to_dict()
        restored = TaskList.from_dict(data)
        new_task = restored.add("Task 3")
        assert new_task.id == 3

    def test_roundtrip_empty_list(self):
        tl = TaskList()
        data = tl.to_dict()
        restored = TaskList.from_dict(data)
        assert restored.list_all() == []
