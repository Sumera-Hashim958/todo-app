# Todo CLI - Phase I

A simple, in-memory command-line todo management application built following Spec-Driven Development (SDD) principles.

## 🎯 Project Overview

This is a **Phase I implementation** of a todo application, focusing on core CRUD operations with an in-memory storage model. The project demonstrates professional software development practices including specification-driven design, systematic testing, and constitutional constraints.

**Phase I Focus**: CLI-only, in-memory, Python standard library only - no databases, no web frameworks, maximum simplicity.

## ✨ Features

This console application demonstrates:

- ✅ **Adding tasks** - Create new todo items with text (1-200 characters)
- ✅ **Listing all tasks** - Display todos with ID, status indicators ([✓]/[ ]), and text
- ✅ **Marking tasks complete** - Toggle completion status with visual feedback
- ✅ **Updating task details** - Modify todo text while preserving ID and status
- ✅ **Deleting tasks** - Remove todos by ID (IDs are never reused)
- ✅ **Input validation** - Empty text, length limits, control character detection
- ✅ **Error handling** - Clear error messages with proper exit codes
- ✅ **Cross-platform UTF-8** - Emoji/unicode support on Windows, macOS, Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses Python standard library only)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-app
```

2. Verify Python version:
```bash
python --version  # Should be 3.8+
```

3. Run the application:
```bash
python todo.py help
```

## 📖 Usage

### Add a Todo

```bash
python todo.py add "Buy groceries"
# Output: Added: Buy groceries
```

### List All Todos

```bash
python todo.py list
# Output:
#   1  [ ] Buy groceries
#   2  [ ] Write report
#   3  [✓] Call dentist
```

### Mark Todo as Complete

```bash
python todo.py complete 1
# Output: Completed: Buy groceries
```

### Update Todo Text

```bash
python todo.py update 1 "Buy organic groceries"
# Output: Updated: Buy organic groceries
```

### Delete a Todo

```bash
python todo.py delete 1
# Output: Deleted: Buy organic groceries
```

### Get Help

```bash
python todo.py help
# Displays all available commands and usage
```

## 🏗️ Project Structure

```
todo-app/
├── todo.py                          # Main entry point and CLI routing
├── models/                          # Data models (currently empty - using dicts)
│   └── __init__.py
├── services/                        # Business logic and CRUD operations
│   ├── __init__.py
│   └── todo_service.py
├── validators/                      # Input validation
│   ├── __init__.py
│   └── input_validator.py
├── utils/                           # Output formatting and utilities
│   ├── __init__.py
│   └── formatter.py
├── specs/                           # Specification artifacts
│   └── 001-todo-cli-core/
│       ├── spec.md                  # Feature specification
│       ├── plan.md                  # Implementation plan
│       ├── tasks.md                 # Task breakdown (38 tasks)
│       ├── data-model.md            # Data model design
│       ├── contracts/
│       │   └── cli-commands.md      # CLI command contracts
│       └── research.md              # Technical decisions
├── history/                         # Development artifacts
│   ├── prompts/                     # Prompt history records (PHRs)
│   └── adr/                         # Architecture decision records
├── .specify/                        # SpecKit Plus framework
│   └── memory/
│       └── constitution.md          # Project constitution
├── .claude/                         # Claude Code configuration
│   ├── agents/                      # Specialized agents
│   └── skills/                      # QA validation skills
├── CLAUDE.md                        # Claude Code instructions
├── README.md                        # This file
└── .gitignore                       # Git ignore rules
```

## 🧪 Testing

Since this is Phase I (in-memory), testing is done via CLI black-box testing:

```bash
# Test in a single Python session
python -c "
import sys
sys.path.insert(0, '.')
import todo

# Add todos
sys.argv = ['todo.py', 'add', 'Task 1']
try: todo.main()
except SystemExit: pass

sys.argv = ['todo.py', 'add', 'Task 2']
try: todo.main()
except SystemExit: pass

# List todos
sys.argv = ['todo.py', 'list']
try: todo.main()
except SystemExit: pass

# Complete a todo
sys.argv = ['todo.py', 'complete', '1']
try: todo.main()
except SystemExit: pass

# List again to verify
sys.argv = ['todo.py', 'list']
try: todo.main()
except SystemExit: pass
"
```

### QA Validation Skills

The project includes automated QA validation skills in `.claude/skills/`:
- `validate-crud-operations.md` - Test all CRUD operations
- `verify-input-edge-cases.md` - Test boundary conditions
- `run-regression-suite.md` - Comprehensive regression testing

## 📋 Constitutional Compliance

This project follows strict **Phase I constraints** as defined in `.specify/memory/constitution.md`:

### ✅ Allowed
- ✅ Command-line interface (CLI)
- ✅ In-memory data structures (lists, dicts)
- ✅ Python standard library only
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Input validation and error handling

### ❌ Prohibited in Phase I
- ❌ Databases (SQL, NoSQL)
- ❌ File-based persistence
- ❌ Web frameworks (Flask, FastAPI, Django)
- ❌ External libraries beyond stdlib
- ❌ GUI interfaces

## ⚠️ Important Notes

**Data Persistence**: This is an **in-memory application**. All data is lost when the program exits. Each command invocation runs in a separate Python process, so todos added in one command are not visible in subsequent commands unless run in the same Python session.

This is **intentional** for Phase I - future phases will add persistence.

**Exit Codes**:
- `0` - Success
- `1` - General error (validation failed, todo not found)
- `2` - Usage error (invalid command, missing arguments)

## 🛠️ Development

### Spec-Driven Development Workflow

This project was built using the SDD-RI (Spec-Driven Development - Rigorous Implementation) workflow:

1. **Constitution** (`/sp.constitution`) - Define project principles and constraints
2. **Specification** (`/sp.specify`) - Define what to build (user stories, requirements)
3. **Planning** (`/sp.plan`) - Design how to build it (architecture, contracts)
4. **Tasks** (`/sp.tasks`) - Break down into actionable tasks
5. **Implementation** (`/sp.implement`) - Execute tasks systematically
6. **QA Validation** - Verify acceptance criteria

All artifacts are preserved in `specs/001-todo-cli-core/` and `history/`.

### Task Breakdown

- **38 total tasks** organized in 8 phases
- **Phase 1**: Project setup (3 tasks)
- **Phase 2**: Foundational components (6 tasks)
- **Phases 3-7**: User stories (20 tasks)
- **Phase 8**: Polish and validation (6 tasks)

See `specs/001-todo-cli-core/tasks.md` for complete task list.

## 📚 Documentation

- **Constitution**: `.specify/memory/constitution.md` - Project principles
- **Specification**: `specs/001-todo-cli-core/spec.md` - Feature requirements
- **Plan**: `specs/001-todo-cli-core/plan.md` - Implementation design
- **CLI Contracts**: `specs/001-todo-cli-core/contracts/cli-commands.md` - Command specifications
- **Data Model**: `specs/001-todo-cli-core/data-model.md` - Data structure design
- **Claude Instructions**: `CLAUDE.md` - Instructions for Claude Code

## 🤝 Contributing

This project follows strict specification-driven development. To contribute:

1. Read the constitution (`.specify/memory/constitution.md`)
2. Create a feature specification using `/sp.specify`
3. Generate an implementation plan using `/sp.plan`
4. Break down into tasks using `/sp.tasks`
5. Implement following `/sp.implement`
6. Validate with QA skills

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

Built using:
- **Claude Code** - AI-powered development assistant
- **SpecKit Plus** - Spec-Driven Development framework
- **SDD-RI Workflow** - Rigorous implementation methodology

---

**Current Status**: ✅ Phase I Complete - All 38 tasks implemented and validated

**Next Phase**: Phase II will add file-based persistence, filtering, and enhanced features while maintaining CLI simplicity.
