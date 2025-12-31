# Research: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2025-12-31
**Phase**: 0 - Technical Research

## Research Questions

### 1. CLI Argument Parsing in Python

**Question**: Best approach for command parsing (`add`, `list`, `complete`, `update`, `delete`)

**Options Evaluated**:
- **Option A**: argparse with subparsers (standard approach)
- **Option B**: Manual sys.argv parsing (simple but error-prone)
- **Option C**: Simple positional argument matching (minimal but limited)

**Decision**: **Option C - Simple Positional Argument Matching**

**Rationale**:
- Phase I prioritizes simplicity over feature richness
- Our commands have simple structure: `command [arg1] [arg2]`
- No optional flags or complex argument combinations needed
- argparse adds ~100 lines of boilerplate for basic subcommand setup
- Manual parsing with sys.argv[1] for command, sys.argv[2:] for args is sufficient
- Easier to understand for beginners (constitutional requirement for beginner-friendly code)
- Still provides clear error messages for invalid usage

**Implementation Approach**:
```python
import sys

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "add":
        handle_add(args)
    elif command == "list":
        handle_list(args)
    # ... etc
```

**Trade-offs**:
- ✅ Simplicity: ~20 lines vs ~100 lines with argparse
- ✅ Transparency: Clear command routing logic
- ❌ No built-in --help (but we can implement simple help text)
- ❌ Manual argument count validation (acceptable for 5 simple commands)

**Alternatives Considered**:
- argparse: Too complex for Phase I scope, constitutional violation (YAGNI principle)
- Third-party CLI libraries (click, typer): Violates "Python stdlib only" constraint

---

### 2. In-Memory Data Structure Selection

**Question**: Optimal structure for storing todos (list vs dict vs custom class)

**Options Evaluated**:
- **Option A**: List of dictionaries `[{"id": 1, "text": "...", "completed": False}]`
- **Option B**: Dictionary with ID keys `{1: {"text": "...", "completed": False}}`
- **Option C**: List of Todo objects (custom class)

**Decision**: **Option A - List of Dictionaries**

**Rationale**:
- Simplest data structure that meets all requirements
- IDs are sequential (1, 2, 3...), list index correlates with creation order
- No need for complex lookups - linear search acceptable for <100 items (spec constraint)
- Dictionaries provide clear, readable data structure
- No custom classes needed - reduces code complexity
- Easy to filter/iterate for display operations

**Implementation Approach**:
```python
todos = []  # Global in-memory storage
next_id = 1  # Counter for sequential IDs

def add_todo(text):
    global next_id
    todo = {
        "id": next_id,
        "text": text,
        "completed": False
    }
    todos.append(todo)
    next_id += 1
    return todo

def find_todo(todo_id):
    return next((t for t in todos if t["id"] == todo_id), None)
```

**Trade-offs**:
- ✅ Simple: No custom classes, standard Python data types
- ✅ Readable: Clear structure, self-documenting
- ✅ Performance: O(n) lookup acceptable for n<100 (spec constraint)
- ❌ No type safety: But acceptable for Phase I simplicity

**Alternatives Considered**:
- Dict with ID keys: Faster lookup (O(1)) but unnecessary for <100 items, adds complexity
- Custom Todo class: More "proper" but violates YAGNI for Phase I

---

### 3. Input Validation Patterns

**Question**: How to validate text length, reject control characters, support UTF-8

**Research Focus**: Python string validation, regex patterns, Unicode handling

**Decision**: Multi-layer validation with regex and string methods

**Validation Strategy**:

1. **Empty/Whitespace Check**:
   ```python
   if not text or not text.strip():
       raise ValueError("Todo text cannot be empty")
   ```

2. **Length Validation**:
   ```python
   if len(text) > 200:
       raise ValueError("Todo text too long (max 200 characters)")
   ```

3. **Control Character Detection**:
   ```python
   import re
   if re.search(r'[\n\r\t]', text):
       raise ValueError("Todo text cannot contain newlines or tabs")
   ```

4. **UTF-8 Support**:
   - Python 3 strings are Unicode by default
   - No special handling needed for emoji/unicode
   - Ensure stdout encoding is UTF-8: `sys.stdout.reconfigure(encoding='utf-8')` (if needed)

**ID Validation**:
```python
def validate_id(id_str):
    try:
        id_val = int(id_str)
        if id_val <= 0:
            raise ValueError("Invalid ID: ID must be a positive number")
        return id_val
    except ValueError:
        raise ValueError("Invalid ID: ID must be a positive number")
```

**Rationale**:
- Layered validation catches all edge cases from spec
- Simple, readable validation logic
- Clear error messages for each failure mode
- No external regex libraries needed (stdlib `re` module)

---

### 4. Error Handling Best Practices

**Question**: stderr vs stdout, exit codes, error message formatting

**Research Focus**: CLI error conventions, Python exception handling

**Decision**: Consistent error handling with stderr and exit codes

**Error Handling Pattern**:

```python
import sys

def error_exit(message, exit_code=1):
    """Print error to stderr and exit with non-zero code"""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)

def success_message(message):
    """Print success message to stdout"""
    print(message)
```

**Usage**:
```python
try:
    # Operation
    result = add_todo(text)
    success_message(f"Added: {result['text']}")
except ValueError as e:
    error_exit(str(e))
```

**Exit Code Convention**:
- **0**: Success (all operations completed successfully)
- **1**: General error (validation failed, todo not found, invalid command)
- **2**: Usage error (wrong number of arguments, invalid command name)

**Error Message Format**:
- Prefix all errors with "Error: " for consistency
- Use clear, actionable language: "Todo not found" not "ID doesn't exist"
- Specify the issue and what's expected: "Invalid ID: ID must be a positive number"

**Rationale**:
- stdout/stderr separation follows Unix conventions (constitutional requirement for standards)
- Non-zero exit codes enable shell scripting integration
- Consistent error prefix makes errors easy to identify
- Clear messages align with FR-010 (clear error messages for invalid operations)

---

## Research Summary

All technical unknowns resolved:

1. ✅ **CLI Parsing**: Simple positional argument matching (sys.argv)
2. ✅ **Data Structure**: List of dictionaries with sequential ID counter
3. ✅ **Validation**: Multi-layer validation with regex and string methods
4. ✅ **Error Handling**: stderr + exit codes + consistent error messages

**Constitutional Compliance**: All decisions align with Phase I constraints (stdlib only, simplicity, deterministic behavior, CLI-only).

**Next Phase**: Phase 1 - Create data-model.md, contracts/, and quickstart.md
