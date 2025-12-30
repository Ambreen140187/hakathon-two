#!/usr/bin/env python3
"""
Todo In-Memory Console Application - Phase I Implementation

This application provides basic todo list functionality with in-memory storage.
It follows a menu-driven interface to allow users to add, view, update, delete,
and mark tasks as complete/incomplete. All data is stored in memory during
runtime and will be lost when the application terminates.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Task:
    """
    Represents a single todo task with ID, description, and completion status.

    Attributes:
        id (int): Unique identifier for the task
        description (str): Description of the task
        completed (bool): Completion status of the task (default: False)
    """
    id: int
    description: str
    completed: bool = False


class TaskManager:
    """
    Manages in-memory storage and operations for tasks.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task list and ID counter."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """
        Add a new task with the given description.

        Args:
            description (str): The task description

        Returns:
            Task: The newly created task

        Raises:
            ValueError: If description is empty or contains only whitespace
        """
        if not description or description.strip() == "":
            raise ValueError("Task description cannot be empty or contain only whitespace")

        task = Task(id=self._next_id, description=description.strip())
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from storage.

        Returns:
            List[Task]: All tasks in the storage
        """
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task with the specified ID, or None if not found
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_description: str) -> bool:
        """
        Update the description of an existing task.

        Args:
            task_id (int): The ID of the task to update
            new_description (str): The new description for the task

        Returns:
            bool: True if the task was updated, False if task was not found

        Raises:
            ValueError: If new description is empty or contains only whitespace
        """
        if not new_description or new_description.strip() == "":
            raise ValueError("Task description cannot be empty or contain only whitespace")

        task = self.get_task_by_id(task_id)
        if task:
            task.description = new_description.strip()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if task was not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark as complete

        Returns:
            bool: True if the task was marked complete, False if task was not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = True
            return True
        return False

    def mark_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark as incomplete

        Returns:
            bool: True if the task was marked incomplete, False if task was not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = False
            return True
        return False


class CLIInterface:
    """
    Handles user interaction through a menu-driven console interface.
    """

    def __init__(self, task_manager: TaskManager):
        """
        Initialize the CLI interface with a task manager.

        Args:
            task_manager (TaskManager): The task manager to use for operations
        """
        self.task_manager = task_manager

    def display_menu(self):
        """Display the main menu options to the user."""
        print("\n" + "="*40)
        print("Todo Application - Main Menu")
        print("="*40)
        print("1. Add Task")
        print("2. View Task List")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print("="*40)

    def get_user_choice(self) -> int:
        """
        Get and validate user menu selection.

        Returns:
            int: The valid menu selection (1-7)
        """
        while True:
            try:
                choice = int(input("Enter your choice (1-7): "))
                if 1 <= choice <= 7:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")

    def add_task_cli(self):
        """Handle adding tasks through the CLI."""
        try:
            description = input("Enter task description: ")
            task = self.task_manager.add_task(description)
            print(f"Task added successfully with ID {task.id}.")
        except ValueError as e:
            print(f"Error: {e}")

    def view_task_list_cli(self):
        """Display all tasks in the console."""
        tasks = self.task_manager.get_all_tasks()

        if not tasks:
            print("\nYour task list is empty.")
            return

        print("\nYour Tasks:")
        print("-" * 50)
        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            print(f"ID: {task.id} | {status} {task.description}")
        print("-" * 50)

    def update_task_cli(self):
        """Handle updating task descriptions through the CLI."""
        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        try:
            new_description = input(f"Enter new description for task {task_id}: ")
            updated = self.task_manager.update_task(task_id, new_description)
            if updated:
                print(f"Task {task_id} updated successfully.")
            else:
                print(f"Failed to update task {task_id}.")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_task_cli(self):
        """Handle deleting tasks through the CLI."""
        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        confirm = input(f"Are you sure you want to delete task '{task.description}'? (y/n): ")
        if confirm.lower() in ['y', 'yes']:
            deleted = self.task_manager.delete_task(task_id)
            if deleted:
                print(f"Task {task_id} deleted successfully.")
            else:
                print(f"Failed to delete task {task_id}.")
        else:
            print("Deletion cancelled.")

    def mark_task_complete_cli(self):
        """Handle marking tasks as complete through the CLI."""
        try:
            task_id = int(input("Enter task ID to mark complete: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        marked = self.task_manager.mark_complete(task_id)
        if marked:
            print(f"Task {task_id} marked as complete.")
        else:
            print(f"Failed to mark task {task_id} as complete.")

    def mark_task_incomplete_cli(self):
        """Handle marking tasks as incomplete through the CLI."""
        try:
            task_id = int(input("Enter task ID to mark incomplete: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        marked = self.task_manager.mark_incomplete(task_id)
        if marked:
            print(f"Task {task_id} marked as incomplete.")
        else:
            print(f"Failed to mark task {task_id} as incomplete.")


def main():
    """Main application entry point."""
    print("Welcome to the Todo App!")

    task_manager = TaskManager()
    cli_interface = CLIInterface(task_manager)

    while True:
        cli_interface.display_menu()
        choice = cli_interface.get_user_choice()

        if choice == 1:
            cli_interface.add_task_cli()
        elif choice == 2:
            cli_interface.view_task_list_cli()
        elif choice == 3:
            cli_interface.update_task_cli()
        elif choice == 4:
            cli_interface.delete_task_cli()
        elif choice == 5:
            cli_interface.mark_task_complete_cli()
        elif choice == 6:
            cli_interface.mark_task_incomplete_cli()
        elif choice == 7:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()