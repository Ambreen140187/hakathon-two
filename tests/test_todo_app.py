import pytest
from todo_app import Task, TaskManager, CLIInterface


class TestTask:
    """Test the Task data model."""

    def test_task_creation(self):
        """Test creating a Task with valid attributes."""
        task = Task(id=1, description="Test task", completed=False)
        assert task.id == 1
        assert task.description == "Test task"
        assert task.completed is False

    def test_task_defaults(self):
        """Test Task creation with default values."""
        task = Task(id=1, description="Test task")
        assert task.id == 1
        assert task.description == "Test task"
        assert task.completed is False  # Default value


class TestTaskManager:
    """Test the TaskManager functionality."""

    def setup_method(self):
        """Set up a fresh TaskManager for each test."""
        self.task_manager = TaskManager()

    def test_add_task(self):
        """Test adding a task to the manager."""
        task = self.task_manager.add_task("Test task")
        assert task.id == 1
        assert task.description == "Test task"
        assert task.completed is False

    def test_add_task_empty_description(self):
        """Test adding a task with empty description raises ValueError."""
        with pytest.raises(ValueError):
            self.task_manager.add_task("")

    def test_add_task_whitespace_description(self):
        """Test adding a task with whitespace-only description raises ValueError."""
        with pytest.raises(ValueError):
            self.task_manager.add_task("   ")

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when the list is empty."""
        tasks = self.task_manager.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_with_tasks(self):
        """Test getting all tasks when the list has tasks."""
        self.task_manager.add_task("Task 1")
        self.task_manager.add_task("Task 2")
        tasks = self.task_manager.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].description == "Task 1"
        assert tasks[1].description == "Task 2"

    def test_get_task_by_id_found(self):
        """Test getting a task by ID that exists."""
        task = self.task_manager.add_task("Test task")
        found_task = self.task_manager.get_task_by_id(task.id)
        assert found_task is not None
        assert found_task.id == task.id
        assert found_task.description == task.description

    def test_get_task_by_id_not_found(self):
        """Test getting a task by ID that doesn't exist."""
        result = self.task_manager.get_task_by_id(999)
        assert result is None

    def test_update_task(self):
        """Test updating a task's description."""
        task = self.task_manager.add_task("Original task")
        updated = self.task_manager.update_task(task.id, "Updated task")
        assert updated is True

        updated_task = self.task_manager.get_task_by_id(task.id)
        assert updated_task.description == "Updated task"

    def test_update_task_empty_description(self):
        """Test updating a task with empty description raises ValueError."""
        task = self.task_manager.add_task("Original task")
        with pytest.raises(ValueError):
            self.task_manager.update_task(task.id, "")

    def test_update_task_whitespace_description(self):
        """Test updating a task with whitespace-only description raises ValueError."""
        task = self.task_manager.add_task("Original task")
        with pytest.raises(ValueError):
            self.task_manager.update_task(task.id, "   ")

    def test_update_task_not_found(self):
        """Test updating a task that doesn't exist."""
        result = self.task_manager.update_task(999, "New description")
        assert result is False

    def test_delete_task(self):
        """Test deleting an existing task."""
        task = self.task_manager.add_task("Test task")
        deleted = self.task_manager.delete_task(task.id)
        assert deleted is True
        assert self.task_manager.get_task_by_id(task.id) is None

    def test_delete_task_not_found(self):
        """Test deleting a task that doesn't exist."""
        result = self.task_manager.delete_task(999)
        assert result is False

    def test_mark_complete(self):
        """Test marking a task as complete."""
        task = self.task_manager.add_task("Test task")
        assert task.completed is False

        marked = self.task_manager.mark_complete(task.id)
        assert marked is True

        updated_task = self.task_manager.get_task_by_id(task.id)
        assert updated_task.completed is True

    def test_mark_complete_not_found(self):
        """Test marking a task as complete when it doesn't exist."""
        result = self.task_manager.mark_complete(999)
        assert result is False

    def test_mark_incomplete(self):
        """Test marking a task as incomplete."""
        task = self.task_manager.add_task("Test task")
        # First mark it complete
        self.task_manager.mark_complete(task.id)
        assert task.completed is True

        marked = self.task_manager.mark_incomplete(task.id)
        assert marked is True

        updated_task = self.task_manager.get_task_by_id(task.id)
        assert updated_task.completed is False

    def test_mark_incomplete_not_found(self):
        """Test marking a task as incomplete when it doesn't exist."""
        result = self.task_manager.mark_incomplete(999)
        assert result is False

    def test_id_generation_sequential(self):
        """Test that task IDs are generated sequentially."""
        task1 = self.task_manager.add_task("Task 1")
        task2 = self.task_manager.add_task("Task 2")
        task3 = self.task_manager.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3


class TestCLIInterface:
    """Test the CLIInterface functionality."""

    def setup_method(self):
        """Set up a fresh TaskManager and CLIInterface for each test."""
        self.task_manager = TaskManager()
        self.cli = CLIInterface(self.task_manager)

    def test_display_menu_no_exception(self):
        """Test that display_menu doesn't raise an exception."""
        # This test simply ensures the method can be called without error
        # In a real implementation, we would mock print() to capture output
        try:
            self.cli.display_menu()
            assert True  # If we reach this, no exception was raised
        except Exception:
            assert False, "display_menu raised an exception"

    def test_add_task_cli(self, monkeypatch):
        """Test adding a task through CLI interface."""
        # Mock input to simulate user entering "Test task"
        monkeypatch.setattr('builtins.input', lambda _: "Test task")

        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.add_task_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify task was added
        tasks = self.task_manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].description == "Test task"

        # Verify success message was printed
        output = captured_output.getvalue()
        assert "Task added successfully" in output

    def test_add_task_cli_empty_description(self, monkeypatch):
        """Test adding a task with empty description through CLI."""
        # Mock input to simulate user entering empty string
        monkeypatch.setattr('builtins.input', lambda _: "")

        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.add_task_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify no task was added
        tasks = self.task_manager.get_all_tasks()
        assert len(tasks) == 0

        # Verify error message was printed
        output = captured_output.getvalue()
        assert "Error:" in output

    def test_view_task_list_cli_empty(self, monkeypatch):
        """Test viewing an empty task list through CLI."""
        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.view_task_list_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify appropriate message was printed
        output = captured_output.getvalue()
        assert "Your task list is empty" in output

    def test_view_task_list_cli_with_tasks(self, monkeypatch):
        """Test viewing a task list with tasks through CLI."""
        # Add some tasks
        self.task_manager.add_task("Task 1")
        self.task_manager.add_task("Task 2")

        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.view_task_list_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify tasks were printed
        output = captured_output.getvalue()
        assert "Task 1" in output
        assert "Task 2" in output
        assert "[ ]" in output  # Incomplete status

    def test_update_task_cli(self, monkeypatch):
        """Test updating a task through CLI interface."""
        # Add a task first
        task = self.task_manager.add_task("Original task")

        # Mock input to simulate user entering task ID and new description
        inputs = iter([str(task.id), "Updated task"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.update_task_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify task was updated
        updated_task = self.task_manager.get_task_by_id(task.id)
        assert updated_task.description == "Updated task"

        # Verify success message was printed
        output = captured_output.getvalue()
        assert "updated successfully" in output

    def test_update_task_cli_not_found(self, monkeypatch):
        """Test updating a non-existent task through CLI."""
        # Mock input to simulate user entering invalid task ID
        inputs = iter(["999", "Updated task"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.update_task_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify error message was printed
        output = captured_output.getvalue()
        assert "not found" in output

    def test_delete_task_cli(self, monkeypatch):
        """Test deleting a task through CLI interface."""
        # Add a task first
        task = self.task_manager.add_task("Task to delete")

        # Mock input to simulate user entering task ID and confirming deletion
        inputs = iter([str(task.id), "y"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.delete_task_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify task was deleted
        assert self.task_manager.get_task_by_id(task.id) is None

        # Verify success message was printed
        output = captured_output.getvalue()
        assert "deleted successfully" in output

    def test_delete_task_cli_cancel(self, monkeypatch):
        """Test canceling task deletion through CLI."""
        # Add a task first
        task = self.task_manager.add_task("Task to delete")

        # Mock input to simulate user entering task ID and canceling deletion
        inputs = iter([str(task.id), "n"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.delete_task_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify task was not deleted
        assert self.task_manager.get_task_by_id(task.id) is not None

        # Verify cancellation message was printed
        output = captured_output.getvalue()
        assert "Deletion cancelled" in output

    def test_mark_task_complete_cli(self, monkeypatch):
        """Test marking a task as complete through CLI."""
        # Add a task first
        task = self.task_manager.add_task("Task to complete")
        assert task.completed is False  # Initially incomplete

        # Mock input to simulate user entering task ID
        monkeypatch.setattr('builtins.input', lambda _: str(task.id))

        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.mark_task_complete_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify task was marked complete
        updated_task = self.task_manager.get_task_by_id(task.id)
        assert updated_task.completed is True

        # Verify success message was printed
        output = captured_output.getvalue()
        assert "marked as complete" in output

    def test_mark_task_incomplete_cli(self, monkeypatch):
        """Test marking a task as incomplete through CLI."""
        # Add a task first and mark it complete
        task = self.task_manager.add_task("Task to mark incomplete")
        self.task_manager.mark_complete(task.id)
        assert task.completed is True  # Initially complete

        # Mock input to simulate user entering task ID
        monkeypatch.setattr('builtins.input', lambda _: str(task.id))

        # Capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.cli.mark_task_incomplete_cli()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Verify task was marked incomplete
        updated_task = self.task_manager.get_task_by_id(task.id)
        assert updated_task.completed is False

        # Verify success message was printed
        output = captured_output.getvalue()
        assert "marked as incomplete" in output


class TestIntegration:
    """Integration tests for the complete application workflow."""

    def setup_method(self):
        """Set up a fresh TaskManager and CLIInterface for each test."""
        self.task_manager = TaskManager()
        self.cli = CLIInterface(self.task_manager)

    def test_full_workflow(self, monkeypatch):
        """Test the complete workflow: add, view, update, mark complete, delete."""
        # Add tasks
        inputs = iter(["First task", "Second task"])
        original_input = __builtins__['input']
        input_iter = iter(inputs)

        def mock_input(prompt):
            if "Enter task description:" in prompt:
                return next(input_iter)
            return original_input(prompt)

        __builtins__['input'] = mock_input

        try:
            self.cli.add_task_cli()  # Add "First task"
            self.cli.add_task_cli()  # Add "Second task"
        finally:
            __builtins__['input'] = original_input

        # Verify tasks were added
        tasks = self.task_manager.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].description == "First task"
        assert tasks[1].description == "Second task"

        # Update first task
        inputs = iter(["1", "Updated first task"])
        input_iter = iter(inputs)
        __builtins__['input'] = lambda _: next(input_iter)

        try:
            self.cli.update_task_cli()
        finally:
            __builtins__['input'] = original_input

        # Verify task was updated
        updated_task = self.task_manager.get_task_by_id(1)
        assert updated_task.description == "Updated first task"

        # Mark second task as complete
        monkeypatch.setattr('builtins.input', lambda _: "2")
        self.cli.mark_task_complete_cli()

        # Verify task was marked complete
        completed_task = self.task_manager.get_task_by_id(2)
        assert completed_task.completed is True

        # Delete first task
        inputs = iter(["1", "y"])  # Task ID and confirmation
        input_iter = iter(inputs)
        __builtins__['input'] = lambda _: next(input_iter)

        try:
            self.cli.delete_task_cli()
        finally:
            __builtins__['input'] = original_input

        # Verify task was deleted and only one remains
        remaining_tasks = self.task_manager.get_all_tasks()
        assert len(remaining_tasks) == 1
        assert remaining_tasks[0].id == 2
        assert remaining_tasks[0].description == "Second task"
        assert remaining_tasks[0].completed is True