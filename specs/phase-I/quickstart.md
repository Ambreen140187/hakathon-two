# Quickstart: Phase I - Todo In-Memory Console Application

## Prerequisites

- Python 3.8 or higher
- No additional dependencies required

## Setup

1. Ensure Python is installed:
   ```bash
   python --version
   ```

2. Clone or access the project directory

3. No installation steps required - the application uses only built-in Python libraries

## Running the Application

Execute the main application file:

```bash
python todo_app.py
```

## Basic Usage

### Adding a Task
1. Select option "1" from the main menu
2. Enter your task description when prompted
3. The task will be added with a unique ID and marked as incomplete

### Viewing Tasks
1. Select option "2" from the main menu
2. All tasks will be displayed with their ID, description, and completion status

### Updating a Task
1. Select option "3" from the main menu
2. Enter the task ID you want to update
3. Enter the new description for the task

### Deleting a Task
1. Select option "4" from the main menu
2. Enter the task ID you want to delete
3. Confirm the deletion if prompted

### Marking Task Complete
1. Select option "5" from the main menu
2. Enter the task ID you want to mark as complete

### Marking Task Incomplete
1. Select option "6" from the main menu
2. Enter the task ID you want to mark as incomplete

### Exiting the Application
1. Select option "7" from the main menu
2. The application will terminate

## Example Session

```
Welcome to the Todo App!
1. Add Task
2. View Task List
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Enter your choice: 1
Enter task description: Buy groceries
Task added successfully with ID 1.

Enter your choice: 2
ID: 1 | [ ] Buy groceries

Enter your choice: 5
Enter task ID to mark complete: 1
Task 1 marked as complete.

Enter your choice: 2
ID: 1 | [x] Buy groceries

Enter your choice: 7
Goodbye!
```

## Error Handling

- Invalid menu choices will show an error message and return to the main menu
- Invalid task IDs will show an error message
- Empty task lists will display an appropriate message
- Empty descriptions will be rejected when adding tasks

## Limitations

- Data is stored only in memory and will be lost when the application exits
- Single-user application
- No authentication required
- Maximum recommended number of tasks: 1000 (for performance)