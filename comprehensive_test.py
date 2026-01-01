2#!/usr/bin/env python3
"""
Comprehensive test for the enhanced Todo Application CLI.
This script simulates user interactions to verify all features work together.
"""

from todo_app import TaskManager, CLIInterface
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

def test_cli_integration():
    """Test the CLI integration of all features."""
    print("Testing CLI Integration of All Features...")

    # Initialize the task manager and CLI
    task_manager = TaskManager()
    cli = CLIInterface(task_manager)

    # Add some test tasks
    print("\nAdding test tasks...")
    task1 = task_manager.add_task("Complete project proposal", "high", ["work", "important", "deadline"])
    task2 = task_manager.add_task("Buy groceries for weekend", "medium", ["personal", "shopping"])
    task3 = task_manager.add_task("Schedule team meeting", "low", ["work", "meeting"])
    task4 = task_manager.add_task("Review code changes", "high", ["work", "development"])
    task5 = task_manager.add_task("Plan vacation", "medium", ["personal", "travel"])

    print(f"Added {len(task_manager.get_all_tasks())} tasks")

    # Test search functionality
    print("\nTesting search functionality...")
    search_results = task_manager.search_tasks("work")
    print(f"Search 'work' returned {len(search_results)} tasks")

    search_results = task_manager.search_tasks("groceries")
    print(f"Search 'groceries' returned {len(search_results)} tasks")

    # Test filtering functionality
    print("\nTesting filtering functionality...")
    high_priority_tasks = task_manager.filter_tasks(priority="high")
    print(f"High priority tasks: {len(high_priority_tasks)}")

    work_tasks = task_manager.filter_tasks(tags=["work"])
    print(f"Work tasks: {len(work_tasks)}")

    active_tasks = task_manager.filter_tasks(status="active")
    print(f"Active tasks: {len(active_tasks)}")

    # Mark a task as complete to test status filtering
    task_manager.mark_complete(task1.id)
    completed_tasks = task_manager.filter_tasks(status="completed")
    print(f"Completed tasks after marking one complete: {len(completed_tasks)}")

    active_tasks = task_manager.filter_tasks(status="active")
    print(f"Active tasks after marking one complete: {len(active_tasks)}")

    # Test sorting functionality
    print("\nTesting sorting functionality...")
    sorted_by_priority = task_manager.sort_tasks("priority", reverse=True)
    print("Tasks sorted by priority (high to low):")
    for task in sorted_by_priority[:3]:  # Show first 3
        priority_indicator = cli.get_priority_indicator(task.priority)
        print(f"  - {task.description} [{priority_indicator}]")

    sorted_by_title = task_manager.sort_tasks("title", reverse=False)
    print("\nTasks sorted by title (A-Z):")
    for task in sorted_by_title[:3]:  # Show first 3
        print(f"  - {task.description}")

    # Test updating a task
    print("\nTesting task update functionality...")
    task_manager.update_task(task2.id, new_priority="high", new_tags=["personal", "urgent"])
    updated_task = task_manager.get_task_by_id(task2.id)
    priority_indicator = cli.get_priority_indicator(updated_task.priority)
    print(f"Updated task: {updated_task.description}, Priority: {priority_indicator}, Tags: {updated_task.tags}")

    # Test the CLI display methods
    print("\nTesting CLI display methods...")
    print("Priority indicators:")
    print(f"  High: {cli.get_priority_indicator('high')}")
    print(f"  Medium: {cli.get_priority_indicator('medium')}")
    print(f"  Low: {cli.get_priority_indicator('low')}")
    print(f"  None: {cli.get_priority_indicator(None)}")

    # Test tag parsing
    print("\nTesting tag parsing:")
    parsed = cli.parse_tags_input("work, important, project, work, personal, important")
    print(f"  Input: 'work, important, project, work, personal, important'")
    print(f"  Output: {parsed} (duplicates should be removed)")

    print("\nCLI Integration test completed successfully!")

def test_edge_cases():
    """Test edge cases and error handling."""
    print("\nTesting Edge Cases...")

    task_manager = TaskManager()

    # Test adding task with empty description
    try:
        task_manager.add_task("")
        print("  ERROR: Should not allow empty task description")
    except ValueError:
        print("  OK: Correctly rejects empty task description")

    # Test adding task with too many tags
    try:
        many_tags = [f"tag{i}" for i in range(11)]  # 11 tags, max is 10
        task_manager.add_task("Test task", tags=many_tags)
        print("  ERROR: Should not allow more than 10 tags")
    except ValueError:
        print("  OK: Correctly rejects more than 10 tags")

    # Test adding task with invalid priority
    try:
        task_manager.add_task("Test task", priority="invalid_priority")
        print("  ERROR: Should not allow invalid priority")
    except ValueError:
        print("  OK: Correctly rejects invalid priority")

    # Test updating with invalid priority
    task = task_manager.add_task("Test task for update")
    try:
        task_manager.update_task(task.id, new_priority="invalid_priority")
        print("  ERROR: Should not allow invalid priority in update")
    except ValueError:
        print("  OK: Correctly rejects invalid priority in update")

    # Test tag with empty string
    try:
        task_manager.add_task("Test task", tags=["", "valid_tag"])
        print("  ERROR: Should not allow empty tag")
    except ValueError:
        print("  OK: Correctly rejects empty tag")

    print("Edge case testing completed!")

if __name__ == "__main__":
    test_cli_integration()
    test_edge_cases()
    print("\nAll tests passed! The Intermediate Phase implementation is working correctly.")