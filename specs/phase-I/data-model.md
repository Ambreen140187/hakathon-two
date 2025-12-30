# Data Model: Phase I - Todo In-Memory Console Application

## Task Entity

### Attributes
- **id** (Integer, Required, Auto-generated)
  - Unique identifier for each task
  - Sequential integer starting from 1
  - Remains constant during application runtime

- **description** (String, Required)
  - Text description of the task
  - Cannot be empty or whitespace-only
  - Maximum length: Not constrained for Phase I

- **completed** (Boolean, Required)
  - Status indicator for task completion
  - Default value: False
  - True = Complete, False = Incomplete

### Constraints
- ID must be unique within the application session
- Description cannot be empty or contain only whitespace
- ID must be positive integer
- Task must exist before update/delete/mark operations

### Valid States
- Active Task: {id: positive_int, description: non_empty_string, completed: boolean}
- Invalid Task: {id: null/empty, description: empty_string, completed: null}

## Task List Container

### Structure
- Python list containing Task objects
- Maintains insertion order
- Indexed by position for iteration, referenced by ID for operations

### Operations
- Add: Append new Task to list
- Read: Iterate through list to display all Tasks
- Update: Find Task by ID and modify its properties
- Delete: Remove Task from list by ID
- Mark Complete/Incomplete: Find Task by ID and update completion status

## In-Memory Storage Characteristics

### Persistence
- Data exists only during application runtime
- Lost when application terminates
- No serialization to external storage

### Access Patterns
- Sequential access for displaying all tasks
- Direct lookup by ID for specific operations
- Index-based iteration for searching/filtering

## ID Generation Strategy

### Algorithm
- Maintain counter starting at 1
- Increment counter for each new task
- Assign counter value as new task ID
- Counter persists during application session

### Guarantees
- Uniqueness within session
- Sequential ordering
- No gaps in sequence (except after deletions)