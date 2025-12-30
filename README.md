# Evolution of Todo - Phase I

This project implements a console-based todo application as part of the "Evolution of Todo" project. Phase I provides a simple, in-memory todo application with basic functionality.

## Features

- **Add Tasks**: Create new todo items with descriptions
- **View Task List**: Display all tasks with their completion status
- **Update Tasks**: Modify existing task descriptions
- **Delete Tasks**: Remove tasks from the list
- **Mark Complete/Incomplete**: Toggle task completion status
- **Menu-Driven Interface**: Simple and intuitive console interface
- **Error Handling**: Graceful handling of invalid inputs and edge cases

## Requirements

- Python 3.8 or higher

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ambreen140187/hakathon-two.git
   ```

2. Navigate to the project directory:
   ```bash
   cd hakathon-two
   ```

## Usage

Run the application using Python:

```bash
python todo_app.py
```

The application will present you with a menu-driven interface:

```
========================================
Todo Application - Main Menu
========================================
1. Add Task
2. View Task List
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit
========================================
```

Follow the on-screen prompts to interact with the application.

## Project Structure

```
.
├── todo_app.py           # Main application file
├── spec-phase-I.md       # Phase I specification
├── specs/                # Detailed specifications
│   └── phase-I/
│       ├── plan.md       # Implementation plan
│       ├── data-model.md # Data model documentation
│       ├── quickstart.md # Quickstart guide
│       ├── research.md   # Research documentation
│       └── tasks.md      # Implementation tasks
├── tests/                # Test suite
│   └── test_todo_app.py  # Unit and integration tests
└── README.md             # This file
```

## Testing

To run the test suite:

```bash
python -m pytest tests/ -v
```

The project includes 32 comprehensive tests covering all functionality.

## Architecture

- **Task Model**: Represents a single todo item with ID, description, and completion status
- **TaskManager**: Handles in-memory storage and operations for tasks
- **CLIInterface**: Provides menu-driven console interface for user interaction
- **In-Memory Storage**: All data is stored in memory during runtime (no persistence)

## Phase I Scope

Phase I implements a single-user, in-memory console application with no persistence beyond runtime. The application is built with pure Python without external dependencies.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).