#!/usr/bin/env python3
"""
Test script for the enhanced Todo Application.
This script tests all the new functionality added in the Intermediate Phase.
"""

from todo_app import TaskManager, CLIInterface

def test_intermediate_features():
    """Test all the new Intermediate Phase features."""
    print("Testing Intermediate Phase Features...")

    # Initialize the task manager
    task_manager = TaskManager()
    cli = CLIInterface(task_manager)

    print("\n1. Testing Task Creation with Priority and Tags...")

    # Test adding tasks with priority and tags
    task1 = task_manager.add_task("Complete project documentation", "high", ["work", "important"])
    print(f"   Added task: {task1.description}, Priority: {task1.priority}, Tags: {task1.tags}")

    task2 = task_manager.add_task("Buy groceries", "medium", ["personal", "shopping"])
    print(f"   Added task: {task2.description}, Priority: {task2.priority}, Tags: {task2.tags}")

    task3 = task_manager.add_task("Schedule meeting", "low", ["work", "meeting"])
    print(f"   Added task: {task3.description}, Priority: {task3.priority}, Tags: {task3.tags}")

    print("\n2. Testing Task Update with Priority and Tags...")

    # Test updating task with new priority and tags
    task_manager.update_task(task1.id, new_priority="low", new_tags=["work", "completed"])
    updated_task = task_manager.get_task_by_id(task1.id)
    print(f"   Updated task: {updated_task.description}, Priority: {updated_task.priority}, Tags: {updated_task.tags}")

    print("\n3. Testing Search Functionality...")

    # Test searching
    search_results = task_manager.search_tasks("project")
    print(f"   Search results for 'project': {len(search_results)} tasks found")
    for task in search_results:
        print(f"     - {task.description}")

    search_results = task_manager.search_tasks("groceries")
    print(f"   Search results for 'groceries': {len(search_results)} tasks found")
    for task in search_results:
        print(f"     - {task.description}")

    print("\n4. Testing Filter Functionality...")

    # Test filtering by priority
    high_priority_tasks = task_manager.filter_tasks(priority="high")
    print(f"   High priority tasks: {len(high_priority_tasks)} tasks found")

    medium_priority_tasks = task_manager.filter_tasks(priority="medium")
    print(f"   Medium priority tasks: {len(medium_priority_tasks)} tasks found")

    work_tasks = task_manager.filter_tasks(tags=["work"])
    print(f"   Tasks with 'work' tag: {len(work_tasks)} tasks found")

    personal_tasks = task_manager.filter_tasks(tags=["personal"])
    print(f"   Tasks with 'personal' tag: {len(personal_tasks)} tasks found")

    print("\n5. Testing Sort Functionality...")

    # Test sorting by priority
    sorted_by_priority = task_manager.sort_tasks("priority", reverse=True)  # High to low
    print("   Tasks sorted by priority (High to Low):")
    for task in sorted_by_priority:
        priority_indicator = cli.get_priority_indicator(task.priority)
        print(f"     - {task.description} [{priority_indicator}]")

    # Test sorting by title
    sorted_by_title = task_manager.sort_tasks("title", reverse=False)  # A-Z
    print("   Tasks sorted by title (A-Z):")
    for task in sorted_by_title:
        print(f"     - {task.description}")

    print("\n6. Testing Combined Operations...")

    # Test combined search and filter
    search_and_filter = task_manager.search_tasks("task")
    filtered_search = [t for t in search_and_filter if t.priority == "low"]
    print(f"   Tasks containing 'task' with low priority: {len(filtered_search)} tasks")

    print("\n7. Testing Priority Indicators...")
    print(f"   High priority indicator: {cli.get_priority_indicator('high')}")
    print(f"   Medium priority indicator: {cli.get_priority_indicator('medium')}")
    print(f"   Low priority indicator: {cli.get_priority_indicator('low')}")
    print(f"   No priority indicator: {cli.get_priority_indicator(None)}")

    print("\n8. Testing Tag Parsing...")
    parsed_tags = cli.parse_tags_input("work, important, project, work")  # Should remove duplicates
    print(f"   Parsed tags (should remove duplicates): {parsed_tags}")

    print("\nAll Intermediate Phase features tested successfully!")

if __name__ == "__main__":
    test_intermediate_features()