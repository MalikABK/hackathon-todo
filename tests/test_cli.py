"""Unit tests for CLI interface."""

import pytest

from src.models import TaskList
from src.cli import create_parser, dispatch_command, format_task_table


class TestFormatTaskTable:
    # T030
    def test_formats_multiple_tasks(self):
        tl = TaskList()
        tl.add("Buy groceries")
        tl.add("Write spec")
        result = format_task_table(tl.list_all())
        assert "Buy groceries" in result
        assert "Write spec" in result
        assert "pending" in result

    # T031
    def test_empty_list_returns_no_tasks_found(self):
        assert format_task_table([]) == "No tasks found."

    def test_header_present(self):
        tl = TaskList()
        tl.add("Task")
        result = format_task_table(tl.list_all())
        assert "ID" in result
        assert "STATUS" in result
        assert "TITLE" in result


class TestDispatchCommand:
    def setup_method(self):
        self.tl = TaskList()

    # T026: create subcommand
    def test_create_subcommand(self, capsys):
        code = dispatch_command(["create", "Buy groceries"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert 'Task created: 1 - "Buy groceries"' in captured.out

    # T028: create prints confirmation
    def test_create_prints_confirmation(self, capsys):
        code = dispatch_command(["create", "Test"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "Task created:" in captured.out

    def test_create_with_description(self, capsys):
        code = dispatch_command(["create", "Task", "-d", "Some desc"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "Task created:" in captured.out

    # T029: empty title error
    def test_create_empty_title_error(self, capsys):
        code = dispatch_command(["create", ""], self.tl)
        captured = capsys.readouterr()
        assert code == 1
        assert "Error: Title cannot be empty." in captured.out

    # T027: list subcommand
    def test_list_subcommand(self, capsys):
        self.tl.add("Task 1")
        code = dispatch_command(["list"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "Task 1" in captured.out

    # T031: list empty
    def test_list_empty(self, capsys):
        code = dispatch_command(["list"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "No tasks found." in captured.out

    # T043: complete success
    def test_complete_subcommand(self, capsys):
        self.tl.add("Task")
        code = dispatch_command(["complete", "1"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "Task 1 marked as completed." in captured.out

    # T044: complete non-existent ID
    def test_complete_not_found(self, capsys):
        code = dispatch_command(["complete", "999"], self.tl)
        captured = capsys.readouterr()
        assert code == 1
        assert "Error: Task with ID 999 not found." in captured.out

    # T045: complete already completed
    def test_complete_already_completed(self, capsys):
        self.tl.add("Task")
        dispatch_command(["complete", "1"], self.tl)
        code = dispatch_command(["complete", "1"], self.tl)
        captured = capsys.readouterr()
        assert code == 1
        assert "already completed" in captured.out

    # Toggle tests
    def test_toggle_pending_to_completed(self, capsys):
        self.tl.add("Task")
        code = dispatch_command(["toggle", "1"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "toggled to completed" in captured.out

    def test_toggle_completed_to_pending(self, capsys):
        self.tl.add("Task")
        dispatch_command(["complete", "1"], self.tl)
        code = dispatch_command(["toggle", "1"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "toggled to pending" in captured.out

    def test_toggle_not_found(self, capsys):
        code = dispatch_command(["toggle", "999"], self.tl)
        captured = capsys.readouterr()
        assert code == 1
        assert "not found" in captured.out

    # T058: update success
    def test_update_subcommand(self, capsys):
        self.tl.add("Old")
        code = dispatch_command(["update", "1", "New"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "Task 1 updated." in captured.out

    # T059: delete success
    def test_delete_subcommand(self, capsys):
        self.tl.add("Task")
        code = dispatch_command(["delete", "1"], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "Task 1 deleted." in captured.out

    # T060: missing arguments
    def test_update_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch_command(["update"], self.tl)

    def test_delete_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch_command(["delete"], self.tl)

    def test_complete_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch_command(["complete"], self.tl)

    # T069: no command prints help
    def test_no_command_prints_help(self, capsys):
        code = dispatch_command([], self.tl)
        captured = capsys.readouterr()
        assert code == 0
        assert "usage" in captured.out.lower()

    # T070: exit codes
    def test_exit_code_success(self, capsys):
        code = dispatch_command(["list"], self.tl)
        assert code == 0

    def test_exit_code_error(self, capsys):
        code = dispatch_command(["create", ""], self.tl)
        assert code == 1
