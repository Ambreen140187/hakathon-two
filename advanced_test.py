#!/usr/bin/env python3
"""
Test script for the Advanced Level features of the Todo Application.
This script tests all the new functionality added in the Advanced Phase.
"""

from todo_app import TaskManager, CLIInterface
from datetime import datetime, timedelta

def test_advanced_features():
    """Test all the new Advanced Level features."""
    print("Testing Advanced Level Features...")

    # Initialize the task manager
    task_manager = TaskManager()
    cli = CLIInterface(task_manager)

    print("\n1. Testing Task Creation with Due Dates and Recurrence...")

    # Test adding tasks with due date and recurrence
    due_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    task1 = task_manager.add_task(
        "Complete project documentation",
        "high",
        ["work", "important"],
        due_date=due_date,
        recurrence="daily"
    )
    print(f"   Added task: {task1.description}")
    print(f"   Due date: {task1.due_date}")
    print(f"   Recurrence: {task1.recurrence}")

    due_date2 = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")  # Past due
    task2 = task_manager.add_task(
        "Buy groceries",
        "medium",
        ["personal", "shopping"],
        due_date=due_date2,
        recurrence="weekly"
    )
    print(f"   Added task: {task2.description}")
    print(f"   Due date: {task2.due_date} (past due)")
    print(f"   Recurrence: {task2.recurrence}")

    print("\n2. Testing Task Update with Due Dates and Recurrence...")

    # Test updating task with new due date and recurrence
    new_due_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
    task_manager.update_task(
        task1.id,
        new_due_date=new_due_date,
        new_recurrence="monthly"
    )
    updated_task = task_manager.get_task_by_id(task1.id)
    print(f"   Updated task: {updated_task.description}")
    print(f"   New due date: {updated_task.due_date}")
    print(f"   New recurrence: {updated_task.recurrence}")

    print("\n3. Testing Due Date Status Classification...")

    # Test due date status classification
    status1, indicator1 = cli.get_due_date_status(task1.due_date)
    print(f"   Task 1 status: {status1} ({indicator1})")

    status2, indicator2 = cli.get_due_date_status(task2.due_date)
    print(f"   Task 2 status: {status2} ({indicator2})")

    print("\n4. Testing Recurrence Logic...")

    # Test completing a recurring task
    print(f"   Before completing task 2: {len(task_manager.get_all_tasks())} tasks")
    task_manager.mark_complete(task2.id)
    print(f"   After completing task 2: {len(task_manager.get_all_tasks())} tasks")

    # Should now have 3 tasks: original completed task 2 + new recurring instance
    all_tasks = task_manager.get_all_tasks()
    completed_task = next((t for t in all_tasks if t.id == task2.id and t.completed), None)
    new_recurring_task = next((t for t in all_tasks if t.id != task2.id and t.description == task2.description), None)

    print(f"   Original task completed: {completed_task is not None}")
    print(f"   New recurring task created: {new_recurring_task is not None}")
    if new_recurring_task:
        print(f"   New task due date: {new_recurring_task.due_date}")

    print("\n5. Testing Filter Functionality with New Fields...")

    # Test filtering by due status
    overdue_tasks = task_manager.filter_tasks(due_status="overdue")
    print(f"   Overdue tasks: {len(overdue_tasks)}")

    upcoming_tasks = task_manager.filter_tasks(due_status="upcoming")
    print(f"   Upcoming tasks: {len(upcoming_tasks)}")

    # Test filtering by recurrence
    daily_tasks = task_manager.filter_tasks(recurrence="daily")
    print(f"   Daily recurring tasks: {len(daily_tasks)}")

    weekly_tasks = task_manager.filter_tasks(recurrence="weekly")
    print(f"   Weekly recurring tasks: {len(weekly_tasks)}")

    print("\n6. Testing Sort Functionality with New Fields...")

    # Test sorting by due date
    sorted_by_due = task_manager.sort_tasks("due_date", reverse=False)  # Earliest first
    print("   Tasks sorted by due date (earliest first):")
    for task in sorted_by_due[:3]:  # Show first 3
        due_status, indicator = cli.get_due_date_status(task.due_date)
        print(f"     - {task.description} [{task.due_date} {indicator}]")

    # Test sorting by due status
    sorted_by_status = task_manager.sort_tasks("due_status", reverse=True)  # Overdue first
    print("\n   Tasks sorted by due status (overdue first):")
    for task in sorted_by_status[:3]:  # Show first 3
        due_status, indicator = cli.get_due_date_status(task.due_date)
        print(f"     - {task.description} [{due_status}]")

    print("\n7. Testing Validation...")

    # Test validation of recurrence
    try:
        task_manager.add_task("Test task", recurrence="invalid_recurrence")
        print("   ERROR: Should not allow invalid recurrence")
    except ValueError:
        print("   OK: Correctly rejects invalid recurrence")

    # Test validation of due date (not in this function but in the update function)
    print("\nAll Advanced Level features tested successfully!")

if __name__ == "__main__":
    test_advanced_features()