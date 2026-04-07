"""Unit tests for services layer."""

import pytest

from src.models import TaskList, EmptyTitleError, TaskNotFoundError
from src import services


class TestCreateTask:
    # T024
    def test_create_task_returns_task(self):
        tl = TaskList()
        task = services.create_task(tl, "Buy groceries", "Milk, eggs, bread")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"

    def test_create_task_empty_title_raises(self):
        tl = TaskList()
        with pytest.raises(EmptyTitleError):
            services.create_task(tl, "")

    def test_create_task_default_description(self):
        tl = TaskList()
        task = services.create_task(tl, "Task")
        assert task.description == ""


class TestListTasks:
    # T025
    def test_list_tasks_returns_all(self):
        tl = TaskList()
        services.create_task(tl, "Task 1")
        services.create_task(tl, "Task 2")
        result = services.list_tasks(tl)
        assert len(result) == 2


class TestCompleteTask:
    # T042
    def test_complete_task_returns_updated_task(self):
        tl = TaskList()
        task = services.create_task(tl, "Task")
        completed = services.complete_task(tl, task.id)
        assert completed.status.value == "completed"

    def test_complete_non_existent_raises(self):
        tl = TaskList()
        with pytest.raises(TaskNotFoundError):
            services.complete_task(tl, 999)


class TestToggleTask:
    def test_toggle_task_returns_updated_task(self):
        tl = TaskList()
        task = services.create_task(tl, "Task")
        toggled = services.toggle_task(tl, task.id)
        assert toggled.status.value == "completed"

    def test_toggle_completed_to_pending(self):
        tl = TaskList()
        task = services.create_task(tl, "Task")
        services.complete_task(tl, task.id)
        toggled = services.toggle_task(tl, task.id)
        assert toggled.status.value == "pending"

    def test_toggle_non_existent_raises(self):
        tl = TaskList()
        with pytest.raises(TaskNotFoundError):
            services.toggle_task(tl, 999)


class TestUpdateTask:
    # T056
    def test_update_task_returns_updated_task(self):
        tl = TaskList()
        task = services.create_task(tl, "Old")
        updated = services.update_task(tl, task.id, "New")
        assert updated.title == "New"

    def test_update_non_existent_raises(self):
        tl = TaskList()
        with pytest.raises(TaskNotFoundError):
            services.update_task(tl, 999, "New")

    def test_update_empty_title_raises(self):
        tl = TaskList()
        services.create_task(tl, "Task")
        with pytest.raises(EmptyTitleError):
            services.update_task(tl, 1, "")


class TestDeleteTask:
    # T057
    def test_delete_task_returns_none(self):
        tl = TaskList()
        services.create_task(tl, "Task")
        result = services.delete_task(tl, 1)
        assert result is None
        assert services.list_tasks(tl) == []

    def test_delete_non_existent_raises(self):
        tl = TaskList()
        with pytest.raises(TaskNotFoundError):
            services.delete_task(tl, 999)
