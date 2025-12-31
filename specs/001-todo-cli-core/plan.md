# Implementation Plan: Todo CLI Core

**Branch**: `001-todo-cli-core` | **Date**: 2025-12-31 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-core/spec.md`

## Summary

Build a CLI-based todo management application with full CRUD operations (add, list, update, complete, delete). The application will use in-memory storage with Python standard library only, providing immediate command-line interaction for task management. Core functionality includes sequential ID assignment, validation, error handling, and UTF-8 support for todo text.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: Python standard library only (argparse for CLI, sys for I/O)
**Storage**: In-memory (Python list data structure)
**Testing**: Manual QA validation via qa-agent skills (validate-crud-operations, verify-input-edge-cases, run-regression-suite)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux with Python 3.8+)
**Project Type**: Single project (simple CLI application)
**Performance Goals**: <1 second response time for all operations with up to 100 todos
**Constraints**: No external dependencies, no file/database persistence, CLI-only interface, deterministic behavior
**Scale/Scope**: Single-user, single-session, in-memory only (Phase I constraint)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Scope Compliance

**✅ COMPLIANT** - All requirements aligned with constitutional constraints:

| Principle | Requirement | Status |
|-----------|-------------|--------|
| **CLI-Only Interface** | All operations via command-line arguments (`python todo.py <command>`) | ✅ PASS |
| **In-Memory Storage** | Todo items stored in Python list (no files, no databases) | ✅ PASS |
| **Python Stdlib Only** | Using only argparse, sys, re from standard library | ✅ PASS |
| **Deterministic Behavior** | Sequential IDs, no randomness, predictable state transitions | ✅ PASS |
| **Explicit Error Handling** | All errors output to stderr with clear messages, non-zero exit codes | ✅ PASS |
| **No External APIs** | No network calls, no third-party libraries | ✅ PASS |
| **No File Persistence** | Data lost on exit (in-memory constraint) | ✅ PASS |
| **Testable** | Black-box testing via CLI commands, QA skills validate all operations | ✅ PASS |

### Quality Gate Requirements

- [x] Specification exists and approved (`spec.md` completed)
- [x] No Phase I constraint violations
- [x] Agent orchestration planned (`qa-agent` validates all implementations)
- [x] Clear acceptance criteria defined (19 functional requirements, 8 success criteria)
- [x] Edge cases documented and testable
- [x] Simple architecture (no unjustified complexity)

**Constitution Check Result**: ✅ **PASS** - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-core/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (CLI patterns, data structures)
├── data-model.md        # Phase 1 output (Todo entity model)
├── quickstart.md        # Phase 1 output (usage guide)
├── contracts/           # Phase 1 output (CLI command contracts)
│   └── cli-commands.md  # Command syntax and behavior specifications
└── checklists/
    └── requirements.md  # Specification quality checklist (complete)
```

### Source Code (repository root)

```text
todo-app/
├── todo.py              # Main entry point and CLI command dispatcher
├── models/
│   └── todo_item.py     # Todo entity class (ID, text, completed)
├── services/
│   └── todo_service.py  # CRUD operations logic (add, list, update, complete, delete)
├── validators/
│   └── input_validator.py  # Input validation (text length, ID format, special chars)
└── utils/
    └── formatter.py     # Output formatting (list display, error messages)
```

**Structure Decision**: Single project structure selected. Simple CLI application requires minimal organization. Using Python's standard module structure with clear separation of concerns:
- `todo.py`: Entry point, argument parsing, command routing
- `models/`: Data entities (Todo item with ID, text, completed status)
- `services/`: Business logic (CRUD operations on in-memory list)
- `validators/`: Input validation logic
- `utils/`: Output formatting and display helpers

No tests/ directory needed - Phase I uses QA agent black-box testing via CLI interface.

## Complexity Tracking

**No constitutional violations** - This section is empty because the implementation fully complies with Phase I constraints. No complexity justification required.

---

## Phase 0: Research & Technical Decisions

### Research Tasks

1. **CLI Argument Parsing in Python**
   - **Question**: Best approach for command parsing (`add`, `list`, `complete`, `update`, `delete`)
   - **Research Focus**: argparse patterns for subcommands vs positional arguments

2. **In-Memory Data Structure Selection**
   - **Question**: Optimal structure for storing todos (list vs dict vs custom class)
   - **Research Focus**: Performance, ID management, CRUD efficiency

3. **Input Validation Patterns**
   - **Question**: How to validate text length, reject control characters, support UTF-8
   - **Research Focus**: Python string validation, regex patterns, Unicode handling

4. **Error Handling Best Practices**
   - **Question**: stderr vs stdout, exit codes, error message formatting
   - **Research Focus**: CLI error conventions, Python exception handling

### Research Findings

*Generated in `research.md`*

---

## Phase 1: Design & Contracts

### Data Model

*Generated in `data-model.md`*

**Entity**: Todo Item
- ID: Integer (sequential, starts at 1)
- Text: String (1-200 chars, UTF-8, no control chars)
- Completed: Boolean (default False)

### CLI Command Contracts

*Generated in `contracts/cli-commands.md`*

Commands:
- `python todo.py add "text"` → Create new todo
- `python todo.py list` → Display all todos
- `python todo.py complete <id>` → Mark todo complete
- `python todo.py update <id> "text"` → Update todo text
- `python todo.py delete <id>` → Delete todo

### Quickstart Guide

*Generated in `quickstart.md`*

User-facing documentation for installation and basic usage.

---

## Phase 2: Implementation Readiness

**Output of `/sp.plan`**: Plan complete, ready for `/sp.tasks`

**Next Command**: `/sp.tasks` to generate actionable task list from this plan
