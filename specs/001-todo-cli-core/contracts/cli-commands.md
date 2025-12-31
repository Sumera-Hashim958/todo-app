# CLI Command Contracts: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2025-12-31
**Phase**: 1 - Design

## General Command Format

```
python todo.py <command> [arguments...]
```

**Exit Codes**:
- **0**: Success (operation completed successfully)
- **1**: General error (validation failure, todo not found, operation failed)
- **2**: Usage error (invalid command, wrong number of arguments)

**Output Streams**:
- **stdout**: Success messages, list output, help text
- **stderr**: Error messages (prefixed with "Error: ")

---

## Command: `add`

### Purpose
Create a new todo item with the specified text.

### Syntax
```bash
python todo.py add "<text>"
```

### Arguments
- **text** (required): The todo description text (1-200 characters)

### Behavior
1. Validate text is not empty or only whitespace
2. Validate text length ≤ 200 characters
3. Validate text contains no control characters (\n, \r, \t)
4. Assign next sequential ID
5. Create todo with ID, text, completed=False
6. Add to in-memory storage
7. Print success message to stdout
8. Exit with code 0

### Success Output (stdout)
```
Added: <text>
```

### Error Cases (stderr, exit code 1)

| Error Condition | Error Message |
|----------------|---------------|
| No text provided | `Error: Todo text cannot be empty` |
| Empty or whitespace-only text | `Error: Todo text cannot be empty` |
| Text > 200 characters | `Error: Todo text too long (max 200 characters)` |
| Text contains newline/tab | `Error: Todo text cannot contain newlines or tabs` |

### Examples

**Success**:
```bash
$ python todo.py add "Buy groceries"
Added: Buy groceries
$ echo $?
0
```

**Error - Empty**:
```bash
$ python todo.py add ""
Error: Todo text cannot be empty
$ echo $?
1
```

**Error - Too Long**:
```bash
$ python todo.py add "Lorem ipsum dolor sit amet, consectetur adipiscing elit... [250 chars]"
Error: Todo text too long (max 200 characters)
$ echo $?
1
```

---

## Command: `list`

### Purpose
Display all todo items with their IDs, text, and completion status.

### Syntax
```bash
python todo.py list
```

### Arguments
None

### Behavior
1. If todos list is empty, print "No todos found"
2. Otherwise, iterate through all todos in creation order
3. For each todo, print formatted line with:
   - ID
   - Completion indicator ([✓] for completed, [ ] for incomplete)
   - Text
4. Exit with code 0

### Success Output (stdout)

**Empty List**:
```
No todos found
```

**Non-Empty List**:
```
[ID] [Status] Text
  1  [ ] Buy groceries
  2  [✓] Write report
  3  [ ] Call dentist
```

### Error Cases
None - list command always succeeds (exit code 0)

### Examples

**Empty List**:
```bash
$ python todo.py list
No todos found
$ echo $?
0
```

**With Todos**:
```bash
$ python todo.py list
  1  [ ] Buy groceries
  2  [✓] Write report
  3  [ ] Call dentist
$ echo $?
0
```

---

## Command: `complete`

### Purpose
Mark a todo item as complete by ID.

### Syntax
```bash
python todo.py complete <id>
```

### Arguments
- **id** (required): The todo ID (positive integer)

### Behavior
1. Validate ID is a positive integer
2. Find todo with matching ID
3. If not found, return error
4. Set todo's completed status to True
5. Print success message
6. Exit with code 0

**Idempotent**: Completing an already-completed todo succeeds without error.

### Success Output (stdout)
```
Completed: <text>
```

### Error Cases (stderr, exit code 1)

| Error Condition | Error Message |
|----------------|---------------|
| No ID provided | `Error: Missing required argument: ID` |
| ID is not numeric | `Error: Invalid ID: ID must be a positive number` |
| ID is negative or zero | `Error: Invalid ID: ID must be a positive number` |
| ID not found | `Error: Todo not found` |

### Examples

**Success**:
```bash
$ python todo.py complete 1
Completed: Buy groceries
$ echo $?
0
```

**Error - Invalid ID**:
```bash
$ python todo.py complete abc
Error: Invalid ID: ID must be a positive number
$ echo $?
1
```

**Error - Not Found**:
```bash
$ python todo.py complete 999
Error: Todo not found
$ echo $?
1
```

---

## Command: `update`

### Purpose
Update the text of an existing todo item by ID.

### Syntax
```bash
python todo.py update <id> "<new_text>"
```

### Arguments
- **id** (required): The todo ID (positive integer)
- **new_text** (required): The new todo text (1-200 characters)

### Behavior
1. Validate ID is a positive integer
2. Find todo with matching ID
3. If not found, return error
4. Validate new_text (same rules as `add` command)
5. Update todo's text field
6. Print success message
7. Exit with code 0

### Success Output (stdout)
```
Updated: <new_text>
```

### Error Cases (stderr, exit code 1)

| Error Condition | Error Message |
|----------------|---------------|
| No ID provided | `Error: Missing required argument: ID` |
| No text provided | `Error: Missing required argument: text` |
| ID is not numeric | `Error: Invalid ID: ID must be a positive number` |
| ID is negative or zero | `Error: Invalid ID: ID must be a positive number` |
| ID not found | `Error: Todo not found` |
| Text empty/whitespace | `Error: Todo text cannot be empty` |
| Text > 200 characters | `Error: Todo text too long (max 200 characters)` |
| Text contains newline/tab | `Error: Todo text cannot contain newlines or tabs` |

### Examples

**Success**:
```bash
$ python todo.py update 1 "Buy organic groceries"
Updated: Buy organic groceries
$ echo $?
0
```

**Error - Not Found**:
```bash
$ python todo.py update 999 "New text"
Error: Todo not found
$ echo $?
1
```

---

## Command: `delete`

### Purpose
Delete a todo item by ID, removing it from storage.

### Syntax
```bash
python todo.py delete <id>
```

### Arguments
- **id** (required): The todo ID (positive integer)

### Behavior
1. Validate ID is a positive integer
2. Find todo with matching ID
3. If not found, return error
4. Remove todo from in-memory list
5. Print success message
6. Exit with code 0

**Note**: Deleted ID is not reused. Sequential ID counter continues.

### Success Output (stdout)
```
Deleted: <text>
```

### Error Cases (stderr, exit code 1)

| Error Condition | Error Message |
|----------------|---------------|
| No ID provided | `Error: Missing required argument: ID` |
| ID is not numeric | `Error: Invalid ID: ID must be a positive number` |
| ID is negative or zero | `Error: Invalid ID: ID must be a positive number` |
| ID not found | `Error: Todo not found` |

### Examples

**Success**:
```bash
$ python todo.py delete 1
Deleted: Buy groceries
$ echo $?
0
```

**Error - Not Found**:
```bash
$ python todo.py delete 999
Error: Todo not found
$ echo $?
1
```

---

## Command: `help` (Optional)

### Purpose
Display usage information and available commands.

### Syntax
```bash
python todo.py help
python todo.py --help
python todo.py
```

### Behavior
1. Print usage information to stdout
2. List all available commands with brief descriptions
3. Exit with code 0

### Output (stdout)
```
Todo CLI - Simple command-line todo management

Usage:
  python todo.py <command> [arguments...]

Commands:
  add "<text>"       Create a new todo item
  list               Display all todo items
  complete <id>      Mark a todo as complete
  update <id> "text" Update a todo's text
  delete <id>        Delete a todo item
  help               Show this help message

Examples:
  python todo.py add "Buy groceries"
  python todo.py list
  python todo.py complete 1
  python todo.py update 1 "Buy organic groceries"
  python todo.py delete 1

Note: This is an in-memory application. All data is lost when the program exits.
```

---

## Invalid Command Handling

### Behavior
When an unknown command is provided:
1. Print error message to stderr
2. Print usage hint
3. Exit with code 2

### Error Output (stderr, exit code 2)
```
Error: Unknown command '<command>'
Try 'python todo.py help' for usage information.
```

### Example
```bash
$ python todo.py foo
Error: Unknown command 'foo'
Try 'python todo.py help' for usage information.
$ echo $?
2
```

---

## Contract Validation Against Requirements

| Requirement | Contract Support |
|-------------|------------------|
| FR-001 (add command) | ✅ `add "<text>"` contract defined |
| FR-004 (list command) | ✅ `list` contract defined with status display |
| FR-005 (complete command) | ✅ `complete <id>` contract defined |
| FR-006 (update command) | ✅ `update <id> "<text>"` contract defined |
| FR-007 (delete command) | ✅ `delete <id>` contract defined |
| FR-010 (clear errors) | ✅ All error messages specified |
| FR-011 (empty list message) | ✅ "No todos found" defined in list |
| FR-012 (completion indicator) | ✅ [✓] / [ ] format specified |
| FR-018 (stdout/stderr) | ✅ Output streams documented for all commands |
| FR-019 (exit codes) | ✅ Exit codes 0/1/2 specified |

**Contract Status**: ✅ **Complete** - All commands fully specified
