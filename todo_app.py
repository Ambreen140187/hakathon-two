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
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single todo task with ID, description, completion status, priority, tags, due date, and recurrence.

    Attributes:
        id (int): Unique identifier for the task
        description (str): Description of the task
        completed (bool): Completion status of the task (default: False)
        priority (str): Priority level of the task - "high", "medium", "low", or None (default: None)
        tags (List[str]): List of tags associated with the task (default: empty list)
        created_at (str): Creation timestamp of the task (default: current timestamp)
        due_date (str): Due date/time of the task in ISO format (default: None)
        recurrence (str): Recurrence pattern - "none", "daily", "weekly", "monthly", or None (default: "none")
        last_completed (str): Timestamp when task was last completed (default: None)
    """
    id: int
    description: str
    completed: bool = False
    priority: Optional[str] = None  # "high", "medium", "low", or None
    tags: List[str] = None  # List of tags
    created_at: str = None  # Creation timestamp
    due_date: Optional[str] = None  # Due date/time in ISO format
    recurrence: Optional[str] = "none"  # "none", "daily", "weekly", "monthly", or None
    last_completed: Optional[str] = None  # Timestamp when last completed

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.recurrence is None:
            self.recurrence = "none"


class TaskManager:
    """
    Manages in-memory storage and operations for tasks.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task list and ID counter."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str, priority: Optional[str] = None, tags: Optional[List[str]] = None, due_date: Optional[str] = None, recurrence: Optional[str] = "none") -> Task:
        """
        Add a new task with the given description, priority, tags, due date, and recurrence.

        Args:
            description (str): The task description
            priority (Optional[str]): The priority level ("high", "medium", "low", or None)
            tags (Optional[List[str]]): List of tags for the task
            due_date (Optional[str]): Due date/time in ISO format
            recurrence (Optional[str]): Recurrence pattern ("none", "daily", "weekly", "monthly", or None)

        Returns:
            Task: The newly created task

        Raises:
            ValueError: If description is empty or contains only whitespace
            ValueError: If priority is not one of the allowed values
            ValueError: If recurrence is not one of the allowed values
        """
        if not description or description.strip() == "":
            raise ValueError("Task description cannot be empty or contain only whitespace")

        if priority is not None and priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of: 'high', 'medium', 'low', or None")

        if recurrence is not None and recurrence not in ["none", "daily", "weekly", "monthly"]:
            raise ValueError("Recurrence must be one of: 'none', 'daily', 'weekly', 'monthly', or None")

        if tags is None:
            tags = []

        # Validate tags
        if len(tags) > 10:
            raise ValueError("Tasks cannot have more than 10 tags")
        for tag in tags:
            if len(tag) > 30:
                raise ValueError("Tags cannot be longer than 30 characters")
            if not tag.strip():
                raise ValueError("Tags cannot be empty or contain only whitespace")

        task = Task(
            id=self._next_id,
            description=description.strip(),
            priority=priority,
            tags=tags.copy(),  # Copy to avoid reference issues
            due_date=due_date,
            recurrence=recurrence
        )
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

    def update_task(self, task_id: int, new_description: Optional[str] = None, new_priority: Optional[str] = None, new_tags: Optional[List[str]] = None, new_due_date: Optional[str] = None, new_recurrence: Optional[str] = None) -> bool:
        """
        Update the description, priority, tags, due date, or recurrence of an existing task.

        Args:
            task_id (int): The ID of the task to update
            new_description (Optional[str]): The new description for the task (if None, no change)
            new_priority (Optional[str]): The new priority for the task (if None, no change)
            new_tags (Optional[List[str]]): The new tags for the task (if None, no change)
            new_due_date (Optional[str]): The new due date for the task (if None, no change)
            new_recurrence (Optional[str]): The new recurrence for the task (if None, no change)

        Returns:
            bool: True if the task was updated, False if task was not found

        Raises:
            ValueError: If new description is empty or contains only whitespace
            ValueError: If priority is not one of the allowed values
            ValueError: If recurrence is not one of the allowed values
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        # Update description if provided
        if new_description is not None:
            if not new_description or new_description.strip() == "":
                raise ValueError("Task description cannot be empty or contain only whitespace")
            task.description = new_description.strip()

        # Update priority if provided
        if new_priority is not None:
            if new_priority not in ["high", "medium", "low", None]:
                raise ValueError("Priority must be one of: 'high', 'medium', 'low', or None")
            task.priority = new_priority

        # Update tags if provided
        if new_tags is not None:
            # Validate tags
            if len(new_tags) > 10:
                raise ValueError("Tasks cannot have more than 10 tags")
            for tag in new_tags:
                if len(tag) > 30:
                    raise ValueError("Tags cannot be longer than 30 characters")
                if not tag.strip():
                    raise ValueError("Tags cannot be empty or contain only whitespace")
            task.tags = new_tags.copy()

        # Update due date if provided
        if new_due_date is not None:
            task.due_date = new_due_date

        # Update recurrence if provided
        if new_recurrence is not None:
            if new_recurrence not in ["none", "daily", "weekly", "monthly", None]:
                raise ValueError("Recurrence must be one of: 'none', 'daily', 'weekly', 'monthly', or None")
            task.recurrence = new_recurrence

        return True

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

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title/description (case-insensitive partial matching).

        Args:
            query (str): The search query string

        Returns:
            List[Task]: List of tasks that match the search query
        """
        if not query:
            return self._tasks.copy()

        query_lower = query.lower().strip()
        matching_tasks = []

        for task in self._tasks:
            if query_lower in task.description.lower():
                matching_tasks.append(task)

        return matching_tasks

    def calculate_next_due_date(self, current_due_date: str, recurrence: str) -> str:
        """
        Calculate the next due date based on recurrence pattern.

        Args:
            current_due_date (str): Current due date in ISO format
            recurrence (str): Recurrence pattern ("daily", "weekly", "monthly")

        Returns:
            str: Next due date in ISO format
        """
        from datetime import datetime, timedelta
        current_date = datetime.fromisoformat(current_due_date.replace('Z', '+00:00'))

        if recurrence == "daily":
            next_date = current_date + timedelta(days=1)
        elif recurrence == "weekly":
            next_date = current_date + timedelta(weeks=1)
        elif recurrence == "monthly":
            # Handle month overflow by adding one month
            year = current_date.year
            month = current_date.month + 1
            if month > 12:
                month = 1
                year += 1

            # Handle case where the day doesn't exist in the next month (e.g., Jan 31 -> Feb 31 doesn't exist)
            day = current_date.day
            try:
                next_date = current_date.replace(year=year, month=month, day=day)
            except ValueError:
                # If the day doesn't exist (like Feb 31), set to the last day of the month
                if month == 2:
                    # Check for leap year
                    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                        max_day = 29
                    else:
                        max_day = 28
                elif month in [4, 6, 9, 11]:
                    max_day = 30
                else:
                    max_day = 31

                next_date = current_date.replace(year=year, month=month, day=max_day)
        else:
            # This shouldn't happen if properly validated, but return current date as fallback
            next_date = current_date

        return next_date.isoformat()

    def mark_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete. If the task is recurring, create a new instance.

        Args:
            task_id (int): The ID of the task to mark as complete

        Returns:
            bool: True if the task was marked complete, False if task was not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        # Mark current task as complete
        task.completed = True
        task.last_completed = datetime.now().isoformat()

        # If task is recurring, create a new instance
        if task.recurrence and task.recurrence != "none" and task.due_date:
            next_due_date = self.calculate_next_due_date(task.due_date, task.recurrence)

            # Create a new task with the same properties but new due date
            new_task = Task(
                id=self._next_id,
                description=task.description,
                completed=False,
                priority=task.priority,
                tags=task.tags.copy(),
                created_at=datetime.now().isoformat(),
                due_date=next_due_date,
                recurrence=task.recurrence,
                last_completed=None
            )

            self._tasks.append(new_task)
            self._next_id += 1

        return True

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[str] = None, tags: Optional[List[str]] = None, due_status: Optional[str] = None, recurrence: Optional[str] = None) -> List[Task]:
        """
        Filter tasks based on status, priority, tags, due date status, and recurrence.

        Args:
            status (Optional[str]): Filter by status - "all", "active", "completed" (default: None)
            priority (Optional[str]): Filter by priority - "high", "medium", "low" (default: None)
            tags (Optional[List[str]]): Filter by tags - tasks with ANY of these tags (default: None)
            due_status (Optional[str]): Filter by due date status - "all", "upcoming", "due-soon", "overdue" (default: None)
            recurrence (Optional[str]): Filter by recurrence - "all", "none", "daily", "weekly", "monthly" (default: None)

        Returns:
            List[Task]: List of tasks that match the filter criteria
        """
        from datetime import datetime
        filtered_tasks = self._tasks.copy()

        # Filter by status
        if status == "active":
            filtered_tasks = [task for task in filtered_tasks if not task.completed]
        elif status == "completed":
            filtered_tasks = [task for task in filtered_tasks if task.completed]

        # Filter by priority
        if priority is not None:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        # Filter by tags (OR logic - task matches if it has ANY of the specified tags)
        if tags:
            filtered_tasks = [task for task in filtered_tasks if any(tag in task.tags for tag in tags)]

        # Filter by due date status
        if due_status and due_status != "all":
            now = datetime.now()
            if due_status == "upcoming":
                # Due in the future, more than 1 hour from now
                filtered_tasks = [task for task in filtered_tasks
                                  if task.due_date and
                                  datetime.fromisoformat(task.due_date.replace('Z', '+00:00')) > now and
                                  (datetime.fromisoformat(task.due_date.replace('Z', '+00:00')) - now).seconds > 3600]
            elif due_status == "due-soon":
                # Due within the next hour
                filtered_tasks = [task for task in filtered_tasks
                                  if task.due_date and
                                  datetime.fromisoformat(task.due_date.replace('Z', '+00:00')) > now and
                                  (datetime.fromisoformat(task.due_date.replace('Z', '+00:00')) - now).seconds <= 3600]
            elif due_status == "overdue":
                # Due in the past and not completed
                filtered_tasks = [task for task in filtered_tasks
                                  if task.due_date and
                                  datetime.fromisoformat(task.due_date.replace('Z', '+00:00')) < now and
                                  not task.completed]

        # Filter by recurrence
        if recurrence and recurrence != "all":
            if recurrence == "none":
                filtered_tasks = [task for task in filtered_tasks
                                  if not task.recurrence or task.recurrence == "none"]
            else:
                filtered_tasks = [task for task in filtered_tasks
                                  if task.recurrence == recurrence]

        return filtered_tasks

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

    def sort_tasks(self, sort_by: str = "created_at", reverse: bool = True) -> List[Task]:
        """
        Sort tasks based on specified criteria.

        Args:
            sort_by (str): Criteria to sort by - "created_at", "priority", "title", "due_date", "due_status" (default: "created_at")
            reverse (bool): Sort order - True for descending, False for ascending (default: True)

        Returns:
            List[Task]: List of tasks sorted according to the specified criteria
        """
        from datetime import datetime

        if sort_by == "created_at":
            # Sort by creation date (newest first by default)
            return sorted(self._tasks, key=lambda task: task.created_at, reverse=reverse)
        elif sort_by == "priority":
            # Define priority order for sorting: high > medium > low > None
            priority_order = {"high": 4, "medium": 3, "low": 2, None: 1}
            return sorted(self._tasks, key=lambda task: priority_order[task.priority], reverse=reverse)
        elif sort_by == "title":
            # Sort by title alphabetically
            return sorted(self._tasks, key=lambda task: task.description.lower(), reverse=reverse)
        elif sort_by == "due_date":
            # Sort by due date (earliest first by default, None values at the end)
            def due_date_key(task):
                if task.due_date is None:
                    # Return a future date so None values go to the end
                    return datetime.max.isoformat()
                return task.due_date
            return sorted(self._tasks, key=lambda task: due_date_key(task), reverse=reverse)
        elif sort_by == "due_status":
            # Sort by due date status: overdue > due soon > upcoming > no due date
            def due_status_key(task):
                if not task.due_date:
                    return 0  # No due date
                due_date = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
                now = datetime.now()

                if due_date < now:
                    return 3  # Overdue
                elif (due_date - now).total_seconds() <= 3600:  # Within 1 hour
                    return 2  # Due soon
                else:
                    return 1  # Upcoming
            return sorted(self._tasks, key=lambda task: due_status_key(task), reverse=reverse)
        else:
            # Default to sorting by creation date
            return sorted(self._tasks, key=lambda task: task.created_at, reverse=reverse)


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

    def get_priority_indicator(self, priority: Optional[str]) -> str:
        """
        Get visual indicator for priority level.

        Args:
            priority (Optional[str]): Priority level ("high", "medium", "low", or None)

        Returns:
            str: Visual indicator for the priority
        """
        if priority == "high":
            return "[HIGH] High"
        elif priority == "medium":
            return "[MED] Medium"
        elif priority == "low":
            return "[LOW] Low"
        else:
            return "[N/A] No Priority"

    def get_due_date_status(self, due_date: Optional[str]) -> tuple[str, str]:
        """
        Get status and color for due date.

        Args:
            due_date (Optional[str]): Due date in ISO format or None

        Returns:
            tuple[str, str]: Status text and color indicator
        """
        if not due_date:
            return "", ""

        from datetime import datetime
        now = datetime.now()
        due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))

        if due < now:
            return "OVERDUE", "[RED] Overdue"
        elif (due - now).total_seconds() <= 3600:  # Within 1 hour
            return "DUE-SOON", "[YELLOW] Due Soon"
        else:
            return "UPCOMING", "[GREEN] Upcoming"

    def display_recurrence_menu(self):
        """Display the recurrence selection menu to the user."""
        print("\nSelect Recurrence:")
        print("1. No Recurrence")
        print("2. Daily")
        print("3. Weekly")
        print("4. Monthly")
        print("5. Keep current recurrence")

    def get_recurrence_from_choice(self, choice: int, current_recurrence: Optional[str] = None) -> Optional[str]:
        """
        Get recurrence value from user menu choice.

        Args:
            choice (int): User's menu choice (1-5)
            current_recurrence (Optional[str]): Current recurrence to return if user chooses to keep it

        Returns:
            Optional[str]: Recurrence value ("none", "daily", "weekly", "monthly", or None)
        """
        if choice == 1:
            return "none"
        elif choice == 2:
            return "daily"
        elif choice == 3:
            return "weekly"
        elif choice == 4:
            return "monthly"
        elif choice == 5:
            return current_recurrence
        else:
            return "none"

    def display_priority_menu(self):
        """Display the priority selection menu to the user."""
        print("\nSelect Priority:")
        print("1. High ([HIGH])")
        print("2. Medium ([MED])")
        print("3. Low ([LOW])")
        print("4. No Priority ([N/A])")
        print("5. Keep current priority")

    def get_priority_from_choice(self, choice: int, current_priority: Optional[str] = None) -> Optional[str]:
        """
        Get priority value from user menu choice.

        Args:
            choice (int): User's menu choice (1-5)
            current_priority (Optional[str]): Current priority to return if user chooses to keep it

        Returns:
            Optional[str]: Priority value ("high", "medium", "low", or None)
        """
        if choice == 1:
            return "high"
        elif choice == 2:
            return "medium"
        elif choice == 3:
            return "low"
        elif choice == 4:
            return None
        elif choice == 5:
            return current_priority
        else:
            return None

    def parse_tags_input(self, tags_input: str) -> List[str]:
        """
        Parse tags input string into a list of tags.

        Args:
            tags_input (str): Comma-separated tags string

        Returns:
            List[str]: List of individual tags
        """
        if not tags_input.strip():
            return []

        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        # Remove duplicates while preserving order
        unique_tags = []
        for tag in tags:
            if tag not in unique_tags:
                unique_tags.append(tag)
        return unique_tags

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
        print("7. Search Tasks")
        print("8. Filter Tasks")
        print("9. Sort Tasks")
        print("10. Advanced Search/Filter/Sort")
        print("11. Exit")
        print("="*40)

    def get_user_choice(self) -> int:
        """
        Get and validate user menu selection.

        Returns:
            int: The valid menu selection (1-11)
        """
        while True:
            try:
                choice = int(input("Enter your choice (1-11): "))
                if 1 <= choice <= 11:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 11.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 11.")

    def add_task_cli(self):
        """Handle adding tasks through the CLI."""
        try:
            description = input("Enter task description: ")

            # Get priority
            self.display_priority_menu()
            try:
                priority_choice = int(input("Enter your choice (1-5): "))
                priority = self.get_priority_from_choice(priority_choice)
            except ValueError:
                print("Invalid choice. Setting priority to None.")
                priority = None

            # Get tags
            tags_input = input("Enter tags (comma-separated, or press Enter for none): ")
            tags = self.parse_tags_input(tags_input)

            # Get due date
            due_date_input = input("Enter due date (YYYY-MM-DD HH:MM, or press Enter for none): ")
            due_date = None
            if due_date_input.strip():
                try:
                    # Parse the date - expecting format like "2026-01-01 14:30"
                    from datetime import datetime
                    due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M").isoformat()
                except ValueError:
                    print("Invalid date format. Due date not set.")
                    due_date = None

            # Get recurrence
            self.display_recurrence_menu()
            try:
                recurrence_choice = int(input("Enter your choice (1-5): "))
                recurrence = self.get_recurrence_from_choice(recurrence_choice)
            except ValueError:
                print("Invalid choice. Setting recurrence to 'none'.")
                recurrence = "none"

            task = self.task_manager.add_task(
                description,
                priority=priority,
                tags=tags,
                due_date=due_date,
                recurrence=recurrence
            )
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
        print("-" * 100)
        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            priority_indicator = self.get_priority_indicator(task.priority)
            tags_str = ", ".join(task.tags) if task.tags else "No tags"

            # Get due date status
            due_status, due_indicator = self.get_due_date_status(task.due_date)
            due_date_str = task.due_date if task.due_date else "No due date"
            recurrence_str = task.recurrence if task.recurrence else "none"

            print(f"ID: {task.id} | {status} {task.description}")
            print(f"      Priority: {priority_indicator} | Due: {due_date_str} {due_indicator}")
            print(f"      Recurrence: {recurrence_str} | Tags: {tags_str}")
        print("-" * 100)

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
            # Ask what to update
            print(f"\nCurrent task: {task.description}")
            print(f"Current priority: {self.get_priority_indicator(task.priority)}")
            print(f"Current tags: {', '.join(task.tags) if task.tags else 'No tags'}")
            print(f"Current due date: {task.due_date if task.due_date else 'No due date'}")
            print(f"Current recurrence: {task.recurrence if task.recurrence else 'none'}")

            update_desc = input("Update description? (y/n, or press Enter for no): ").lower() in ['y', 'yes', '']
            new_description = None
            if update_desc:
                new_description = input(f"Enter new description (current: '{task.description}'): ")

            update_priority = input("Update priority? (y/n, or press Enter for no): ").lower() in ['y', 'yes', '']
            new_priority = None
            if update_priority:
                self.display_priority_menu()
                try:
                    priority_choice = int(input("Enter your choice (1-5): "))
                    new_priority = self.get_priority_from_choice(priority_choice, task.priority)
                except ValueError:
                    print("Invalid choice. Keeping current priority.")
                    new_priority = task.priority

            update_tags = input("Update tags? (y/n, or press Enter for no): ").lower() in ['y', 'yes', '']
            new_tags = None
            if update_tags:
                tags_input = input(f"Enter new tags (comma-separated, or press Enter to keep current: '{', '.join(task.tags) if task.tags else 'None'}'): ")
                if tags_input.strip():
                    new_tags = self.parse_tags_input(tags_input)
                else:
                    new_tags = task.tags  # Keep current tags if input is empty

            update_due_date = input("Update due date? (y/n, or press Enter for no): ").lower() in ['y', 'yes', '']
            new_due_date = None
            if update_due_date:
                due_date_input = input(f"Enter new due date (YYYY-MM-DD HH:MM, or press Enter to keep current: '{task.due_date or 'None'}'): ")
                if due_date_input.strip():
                    try:
                        # Parse the date - expecting format like "2026-01-01 14:30"
                        from datetime import datetime
                        new_due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M").isoformat()
                    except ValueError:
                        print("Invalid date format. Keeping current due date.")
                        new_due_date = task.due_date
                else:
                    new_due_date = task.due_date  # Keep current due date if input is empty

            update_recurrence = input("Update recurrence? (y/n, or press Enter for no): ").lower() in ['y', 'yes', '']
            new_recurrence = None
            if update_recurrence:
                self.display_recurrence_menu()
                try:
                    recurrence_choice = int(input("Enter your choice (1-5): "))
                    new_recurrence = self.get_recurrence_from_choice(recurrence_choice, task.recurrence)
                except ValueError:
                    print("Invalid choice. Keeping current recurrence.")
                    new_recurrence = task.recurrence

            updated = self.task_manager.update_task(
                task_id,
                new_description=new_description if update_desc else None,
                new_priority=new_priority if update_priority else None,
                new_tags=new_tags if update_tags else None,
                new_due_date=new_due_date if update_due_date else None,
                new_recurrence=new_recurrence if update_recurrence else None
            )
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

    def search_tasks_cli(self):
        """Handle searching tasks through the CLI."""
        query = input("Enter search query (will search in task descriptions): ")

        if not query.strip():
            print("Empty search query. Showing all tasks.")
            self.view_task_list_cli()
            return

        matching_tasks = self.task_manager.search_tasks(query)

        if not matching_tasks:
            print(f"\nNo tasks found matching '{query}'.")
            return

        print(f"\nSearch results for '{query}':")
        print("-" * 80)
        for task in matching_tasks:
            status = "[x]" if task.completed else "[ ]"
            priority_indicator = self.get_priority_indicator(task.priority)
            tags_str = ", ".join(task.tags) if task.tags else "No tags"
            print(f"ID: {task.id} | {status} {task.description}")
            print(f"      Priority: {priority_indicator} | Tags: {tags_str}")
        print("-" * 80)

    def display_filter_menu(self):
        """Display the filter options menu to the user."""
        print("\nFilter Options:")
        print("1. Filter by Status")
        print("2. Filter by Priority")
        print("3. Filter by Tags")
        print("4. Filter by Due Date Status")
        print("5. Filter by Recurrence")
        print("6. Clear all filters")
        print("7. Back to main menu")

    def filter_tasks_cli(self):
        """Handle filtering tasks through the CLI."""
        status_filter = None
        priority_filter = None
        tags_filter = []
        due_status_filter = None
        recurrence_filter = None

        while True:
            print(f"\nCurrent filters - Status: {status_filter or 'All'}, Priority: {priority_filter or 'All'}, Tags: {', '.join(tags_filter) or 'All'}, Due Status: {due_status_filter or 'All'}, Recurrence: {recurrence_filter or 'All'}")
            self.display_filter_menu()

            try:
                choice = int(input("Enter your choice (1-7): "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")
                continue

            if choice == 1:
                # Filter by status
                print("\nSelect Status Filter:")
                print("1. All")
                print("2. Active only")
                print("3. Completed only")
                try:
                    status_choice = int(input("Enter your choice (1-3): "))
                    if status_choice == 1:
                        status_filter = None
                    elif status_choice == 2:
                        status_filter = "active"
                    elif status_choice == 3:
                        status_filter = "completed"
                    else:
                        print("Invalid choice. No status filter applied.")
                except ValueError:
                    print("Invalid input. No status filter applied.")

            elif choice == 2:
                # Filter by priority
                self.display_priority_menu()
                try:
                    priority_choice = int(input("Enter your choice (1-4): "))
                    priority = self.get_priority_from_choice(priority_choice)
                    priority_filter = priority
                except ValueError:
                    print("Invalid input. No priority filter applied.")

            elif choice == 3:
                # Filter by tags
                tags_input = input("Enter tags to filter by (comma-separated): ")
                tags_filter = self.parse_tags_input(tags_input)
                if not tags_filter:
                    print("No tags entered. Clearing tag filter.")

            elif choice == 4:
                # Filter by due date status
                print("\nSelect Due Date Status Filter:")
                print("1. All")
                print("2. Upcoming")
                print("3. Due Soon")
                print("4. Overdue")
                try:
                    due_status_choice = int(input("Enter your choice (1-4): "))
                    if due_status_choice == 1:
                        due_status_filter = None
                    elif due_status_choice == 2:
                        due_status_filter = "upcoming"
                    elif due_status_choice == 3:
                        due_status_filter = "due-soon"
                    elif due_status_choice == 4:
                        due_status_filter = "overdue"
                    else:
                        print("Invalid choice. No due date status filter applied.")
                except ValueError:
                    print("Invalid input. No due date status filter applied.")

            elif choice == 5:
                # Filter by recurrence
                print("\nSelect Recurrence Filter:")
                print("1. All")
                print("2. None")
                print("3. Daily")
                print("4. Weekly")
                print("5. Monthly")
                try:
                    recurrence_choice = int(input("Enter your choice (1-5): "))
                    if recurrence_choice == 1:
                        recurrence_filter = None
                    elif recurrence_choice == 2:
                        recurrence_filter = "none"
                    elif recurrence_choice == 3:
                        recurrence_filter = "daily"
                    elif recurrence_choice == 4:
                        recurrence_filter = "weekly"
                    elif recurrence_choice == 5:
                        recurrence_filter = "monthly"
                    else:
                        print("Invalid choice. No recurrence filter applied.")
                except ValueError:
                    print("Invalid input. No recurrence filter applied.")

            elif choice == 6:
                # Clear all filters
                status_filter = None
                priority_filter = None
                tags_filter = []
                due_status_filter = None
                recurrence_filter = None
                print("All filters cleared.")

            elif choice == 7:
                # Back to main menu
                break

            else:
                print("Invalid choice. Please select 1-7.")

            # Show filtered results after each filter change
            if choice in [1, 2, 3, 4, 5, 6]:
                filtered_tasks = self.task_manager.filter_tasks(
                    status=status_filter,
                    priority=priority_filter,
                    tags=tags_filter if tags_filter else None,
                    due_status=due_status_filter,
                    recurrence=recurrence_filter
                )

                if not filtered_tasks:
                    print(f"\nNo tasks match current filters (Status: {status_filter or 'All'}, Priority: {priority_filter or 'All'}, Tags: {', '.join(tags_filter) or 'All'}, Due Status: {due_status_filter or 'All'}, Recurrence: {recurrence_filter or 'All'}).")
                else:
                    print(f"\nFiltered tasks (Status: {status_filter or 'All'}, Priority: {priority_filter or 'All'}, Tags: {', '.join(tags_filter) or 'All'}, Due Status: {due_status_filter or 'All'}, Recurrence: {recurrence_filter or 'All'}):")
                    print("-" * 100)
                    for task in filtered_tasks:
                        status = "[x]" if task.completed else "[ ]"
                        priority_indicator = self.get_priority_indicator(task.priority)
                        tags_str = ", ".join(task.tags) if task.tags else "No tags"
                        due_status, due_indicator = self.get_due_date_status(task.due_date)
                        due_date_str = task.due_date if task.due_date else "No due date"
                        recurrence_str = task.recurrence if task.recurrence else "none"

                        print(f"ID: {task.id} | {status} {task.description}")
                        print(f"      Priority: {priority_indicator} | Due: {due_date_str} {due_indicator}")
                        print(f"      Recurrence: {recurrence_str} | Tags: {tags_str}")
                    print("-" * 100)

    def display_sort_menu(self):
        """Display the sort options menu to the user."""
        print("\nSort Options:")
        print("1. Sort by Creation Date (Newest first)")
        print("2. Sort by Creation Date (Oldest first)")
        print("3. Sort by Priority (High to Low)")
        print("4. Sort by Priority (Low to High)")
        print("5. Sort by Title (A-Z)")
        print("6. Sort by Title (Z-A)")
        print("7. Sort by Due Date (Earliest first)")
        print("8. Sort by Due Date (Latest first)")
        print("9. Sort by Due Status (Overdue first)")

    def display_advanced_menu(self):
        """Display the advanced options menu to the user."""
        print("\nAdvanced Options:")
        print("1. Search + Filter + Sort")
        print("2. Search + Filter")
        print("3. Search + Sort")
        print("4. Filter + Sort")
        print("5. Back to main menu")

    def advanced_tasks_cli(self):
        """Handle advanced search/filter/sort operations through the CLI."""
        while True:
            self.display_advanced_menu()

            try:
                choice = int(input("Enter your choice (1-5): "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")
                continue

            if choice == 5:
                # Back to main menu
                break

            # Initialize filters
            query = ""
            status_filter = None
            priority_filter = None
            tags_filter = []
            sort_by = "created_at"
            reverse = True

            # Get search query if needed
            if choice in [1, 2, 3]:  # Search is involved
                query = input("Enter search query (or press Enter for none): ")

            # Get filters if needed
            if choice in [1, 2, 4]:  # Filter is involved
                # Get status filter
                print("\nSelect Status Filter (or press Enter for all):")
                print("1. All")
                print("2. Active only")
                print("3. Completed only")
                try:
                    status_input = input("Enter your choice (1-3, or press Enter for all): ")
                    if status_input:
                        status_choice = int(status_input)
                        if status_choice == 2:
                            status_filter = "active"
                        elif status_choice == 3:
                            status_filter = "completed"
                except ValueError:
                    print("Invalid input. Using 'All' status filter.")

                # Get priority filter
                print("\nCurrent priority options:")
                self.display_priority_menu()
                try:
                    priority_input = input("Enter your choice (1-4, or press Enter for all): ")
                    if priority_input:
                        priority_choice = int(priority_input)
                        priority = self.get_priority_from_choice(priority_choice)
                        priority_filter = priority
                except ValueError:
                    print("Invalid input. Using 'All' priority filter.")

                # Get tags filter
                tags_input = input("Enter tags to filter by (comma-separated, or press Enter for all): ")
                if tags_input.strip():
                    tags_filter = self.parse_tags_input(tags_input)

            # Get sort option if needed
            if choice in [1, 3, 4]:  # Sort is involved
                self.display_sort_menu()
                try:
                    sort_input = input("Enter your choice (1-9, or press Enter for default): ")
                    if sort_input:
                        sort_choice = int(sort_input)
                        if sort_choice == 1:
                            sort_by = "created_at"
                            reverse = True
                        elif sort_choice == 2:
                            sort_by = "created_at"
                            reverse = False
                        elif sort_choice == 3:
                            sort_by = "priority"
                            reverse = True
                        elif sort_choice == 4:
                            sort_by = "priority"
                            reverse = False
                        elif sort_choice == 5:
                            sort_by = "title"
                            reverse = False
                        elif sort_choice == 6:
                            sort_by = "title"
                            reverse = True
                        elif sort_choice == 7:
                            sort_by = "due_date"
                            reverse = False
                        elif sort_choice == 8:
                            sort_by = "due_date"
                            reverse = True
                        elif sort_choice == 9:
                            sort_by = "due_status"
                            reverse = True
                        else:
                            print("Invalid choice. Using default sort.")
                except ValueError:
                    print("Invalid input. Using default sort.")

            # Apply operations in order: search -> filter -> sort
            # Start with all tasks
            tasks = self.task_manager.get_all_tasks()

            # Apply search if query exists
            if query.strip():
                tasks = self.task_manager.search_tasks(query)

            # Apply filter if any filter is set
            if status_filter is not None or priority_filter is not None or tags_filter:
                # Create a temporary TaskManager-like object to use the filter method
                # We'll create a temporary list and apply filters
                filtered_tasks = []
                for task in tasks:
                    # Apply status filter
                    if status_filter == "active" and task.completed:
                        continue
                    if status_filter == "completed" and not task.completed:
                        continue

                    # Apply priority filter
                    if priority_filter is not None and task.priority != priority_filter:
                        continue

                    # Apply tags filter (OR logic within tags)
                    if tags_filter and not any(tag in task.tags for tag in tags_filter):
                        continue

                    filtered_tasks.append(task)
                tasks = filtered_tasks

            # Apply sort
            if sort_by == "created_at":
                tasks = sorted(tasks, key=lambda task: task.created_at, reverse=reverse)
            elif sort_by == "priority":
                priority_order = {"high": 4, "medium": 3, "low": 2, None: 1}
                tasks = sorted(tasks, key=lambda task: priority_order[task.priority], reverse=reverse)
            elif sort_by == "title":
                tasks = sorted(tasks, key=lambda task: task.description.lower(), reverse=reverse)
            elif sort_by == "due_date":
                def due_date_key(task):
                    if task.due_date is None:
                        # Return a future date so None values go to the end
                        from datetime import datetime
                        return datetime.max.isoformat()
                    return task.due_date
                tasks = sorted(tasks, key=lambda task: due_date_key(task), reverse=reverse)
            elif sort_by == "due_status":
                def due_status_key(task):
                    if not task.due_date:
                        return 0  # No due date
                    from datetime import datetime
                    due_date = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
                    now = datetime.now()

                    if due_date < now:
                        return 3  # Overdue
                    elif (due_date - now).total_seconds() <= 3600:  # Within 1 hour
                        return 2  # Due soon
                    else:
                        return 1  # Upcoming
                tasks = sorted(tasks, key=lambda task: due_status_key(task), reverse=reverse)

            # Display results
            if not tasks:
                print(f"\nNo tasks match your criteria.")
                if query:
                    print(f"  Search query: {query}")
                print(f"  Status: {status_filter or 'All'}")
                print(f"  Priority: {priority_filter or 'All'}")
                print(f"  Tags: {', '.join(tags_filter) or 'All'}")
                print(f"  Sort by: {sort_by}, {'descending' if reverse else 'ascending'}")
            else:
                print(f"\nFiltered and sorted tasks:")
                if query:
                    print(f"  Search query: {query}")
                print(f"  Status: {status_filter or 'All'}")
                print(f"  Priority: {priority_filter or 'All'}")
                print(f"  Tags: {', '.join(tags_filter) or 'All'}")
                print(f"  Sort by: {sort_by}, {'descending' if reverse else 'ascending'}")
                print("-" * 80)
                for task in tasks:
                    status = "[x]" if task.completed else "[ ]"
                    priority_indicator = self.get_priority_indicator(task.priority)
                    tags_str = ", ".join(task.tags) if task.tags else "No tags"
                    print(f"ID: {task.id} | {status} {task.description}")
                    print(f"      Priority: {priority_indicator} | Tags: {tags_str}")
                print("-" * 80)

    def sort_tasks_cli(self):
        """Handle sorting tasks through the CLI."""
        self.display_sort_menu()

        try:
            choice = int(input("Enter your choice (1-6): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
            return

        sort_by = "created_at"
        reverse = True  # Default to descending

        if choice == 1:
            # Sort by creation date (newest first) - default behavior
            sort_by = "created_at"
            reverse = True
        elif choice == 2:
            # Sort by creation date (oldest first)
            sort_by = "created_at"
            reverse = False
        elif choice == 3:
            # Sort by priority (high to low)
            sort_by = "priority"
            reverse = True
        elif choice == 4:
            # Sort by priority (low to high)
            sort_by = "priority"
            reverse = False
        elif choice == 5:
            # Sort by title (A-Z)
            sort_by = "title"
            reverse = False
        elif choice == 6:
            # Sort by title (Z-A)
            sort_by = "title"
            reverse = True
        else:
            print("Invalid choice. Using default sort (newest first).")
            sort_by = "created_at"
            reverse = True

        sorted_tasks = self.task_manager.sort_tasks(sort_by=sort_by, reverse=reverse)

        if not sorted_tasks:
            print("\nNo tasks to display.")
            return

        print(f"\nSorted tasks (by {sort_by}, {'descending' if reverse else 'ascending'}):")
        print("-" * 80)
        for task in sorted_tasks:
            status = "[x]" if task.completed else "[ ]"
            priority_indicator = self.get_priority_indicator(task.priority)
            tags_str = ", ".join(task.tags) if task.tags else "No tags"
            print(f"ID: {task.id} | {status} {task.description}")
            print(f"      Priority: {priority_indicator} | Tags: {tags_str}")
        print("-" * 80)

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
            cli_interface.search_tasks_cli()
        elif choice == 8:
            cli_interface.filter_tasks_cli()
        elif choice == 9:
            cli_interface.sort_tasks_cli()
        elif choice == 10:
            cli_interface.advanced_tasks_cli()
        elif choice == 11:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()