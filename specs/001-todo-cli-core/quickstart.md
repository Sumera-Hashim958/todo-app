# Quickstart Guide: Todo CLI Core

**Version**: 1.0.0
**Date**: 2025-12-31

## Overview

Todo CLI Core is a simple command-line todo management application. It allows you to create, view, complete, update, and delete todo items directly from your terminal.

**Key Features**:
- ✅ Add new todos with descriptive text
- ✅ View all todos in a organized list
- ✅ Mark todos as complete
- ✅ Update todo text
- ✅ Delete todos you no longer need
- ✅ Simple command-line interface
- ✅ No installation required (Python stdlib only)

**Important**: This is an in-memory application. All todos are lost when the program exits (Phase I limitation).

---

## Prerequisites

- **Python 3.8 or higher** installed on your system
- Terminal/Command Prompt access

### Check Python Version

```bash
python --version
# Should output: Python 3.8.x or higher
```

---

## Installation

1. **Download** the `todo.py` file to your computer

2. **Navigate** to the directory containing `todo.py`:
   ```bash
   cd path/to/todo-app
   ```

3. **Test** the installation:
   ```bash
   python todo.py help
   ```

You should see the help message displaying available commands.

---

## Basic Usage

### Adding Your First Todo

Create a new todo item:

```bash
python todo.py add "Buy groceries"
```

**Output**:
```
Added: Buy groceries
```

### Viewing All Todos

Display all your todo items:

```bash
python todo.py list
```

**Output**:
```
  1  [ ] Buy groceries
```

The format is: `ID  [Status] Text`
- `[ ]` means incomplete
- `[✓]` means completed

### Marking a Todo Complete

Complete a todo by its ID:

```bash
python todo.py complete 1
```

**Output**:
```
Completed: Buy groceries
```

Now when you list todos:
```bash
python todo.py list
```

**Output**:
```
  1  [✓] Buy groceries
```

### Updating a Todo

Change the text of an existing todo:

```bash
python todo.py update 1 "Buy organic groceries"
```

**Output**:
```
Updated: Buy organic groceries
```

### Deleting a Todo

Remove a todo you no longer need:

```bash
python todo.py delete 1
```

**Output**:
```
Deleted: Buy organic groceries
```

---

## Complete Workflow Example

Let's walk through a complete todo management session:

```bash
# Add some todos
$ python todo.py add "Buy groceries"
Added: Buy groceries

$ python todo.py add "Write project report"
Added: Write project report

$ python todo.py add "Call dentist"
Added: Call dentist

# View all todos
$ python todo.py list
  1  [ ] Buy groceries
  2  [ ] Write project report
  3  [ ] Call dentist

# Complete the first task
$ python todo.py complete 1
Completed: Buy groceries

# Update the second task
$ python todo.py update 2 "Write quarterly project report"
Updated: Write quarterly project report

# View updated list
$ python todo.py list
  1  [✓] Buy groceries
  2  [ ] Write quarterly project report
  3  [ ] Call dentist

# Delete completed task
$ python todo.py delete 1
Deleted: Buy groceries

# Final list
$ python todo.py list
  2  [ ] Write quarterly project report
  3  [ ] Call dentist
```

---

## Command Reference

### `add "<text>"`
Create a new todo item.

**Example**: `python todo.py add "Finish homework"`

**Notes**:
- Text must be 1-200 characters
- Cannot be empty or only whitespace
- No newlines or tabs allowed
- Supports unicode and emoji (🚀✨)

---

### `list`
Display all todo items.

**Example**: `python todo.py list`

**Notes**:
- Shows todos in creation order (oldest first)
- Displays ID, completion status, and text
- Shows "No todos found" if list is empty

---

### `complete <id>`
Mark a todo as complete.

**Example**: `python todo.py complete 2`

**Notes**:
- ID must be a positive number
- Completing an already-completed todo is okay (no error)
- Cannot undo completion (Phase I limitation)

---

### `update <id> "<new_text>"`
Update the text of an existing todo.

**Example**: `python todo.py update 3 "Call dentist at 2pm"`

**Notes**:
- Same text validation rules as `add` command
- ID remains unchanged
- Can update completed todos

---

### `delete <id>`
Delete a todo item.

**Example**: `python todo.py delete 1`

**Notes**:
- Permanently removes the todo from the list
- ID is not reused for future todos
- Cannot be undone

---

### `help`
Show usage information.

**Example**: `python todo.py help`

---

## Tips & Tricks

### Quoting Text with Spaces

Always use quotes around todo text that contains spaces:

```bash
# Correct
python todo.py add "Buy milk and eggs"

# Incorrect (will cause an error)
python todo.py add Buy milk and eggs
```

### Handling Special Characters

**Quotes in Text**: Use the opposite quote type or escape:

```bash
# Single quotes in double-quoted text (works)
python todo.py add "Review John's report"

# Double quotes (use single quotes around the whole thing)
python todo.py add 'Read "The Great Gatsby"'
```

**Unicode and Emoji**: Fully supported!

```bash
python todo.py add "Finish project 🚀"
python todo.py add "日本語のテスト"
```

### Empty List

If you see "No todos found", you have no active todos. Start adding some!

```bash
$ python todo.py list
No todos found
```

---

## Common Errors

### "Error: Todo text cannot be empty"

**Cause**: You tried to add or update with empty text.

**Solution**: Provide valid text (1-200 characters).

```bash
# Wrong
python todo.py add ""

# Right
python todo.py add "My todo"
```

---

### "Error: Todo not found"

**Cause**: The ID you specified doesn't exist (deleted or never existed).

**Solution**: Run `python todo.py list` to see valid IDs.

```bash
$ python todo.py complete 999
Error: Todo not found

$ python todo.py list
  1  [ ] Buy groceries
  2  [ ] Write report

$ python todo.py complete 1
Completed: Buy groceries
```

---

### "Error: Invalid ID: ID must be a positive number"

**Cause**: You provided a non-numeric or negative ID.

**Solution**: Use a positive integer (1, 2, 3, ...).

```bash
# Wrong
python todo.py complete abc
python todo.py complete -1

# Right
python todo.py complete 1
```

---

### "Error: Todo text too long (max 200 characters)"

**Cause**: Your todo text exceeds 200 characters.

**Solution**: Shorten your text to 200 characters or less.

---

## Limitations (Phase I)

**In-Memory Only**: All todos are stored in memory and **lost when the program exits**. This is a Phase I limitation. Future versions will add persistence.

**No Undo**: Completed todos cannot be marked as incomplete. Deleted todos cannot be recovered.

**No Search/Filter**: No built-in search or filtering. Use `list` to see all todos.

**No Priority/Tags**: Todos have no priority levels, categories, or tags.

**No Due Dates**: No time-based features like due dates or reminders.

---

## Troubleshooting

### Program Not Found

**Error**: `python: command not found` or similar

**Solution**: Ensure Python 3.8+ is installed and in your PATH.

```bash
# Try python3 instead of python
python3 todo.py add "Test"
```

---

### UTF-8 Display Issues

**Problem**: Emoji or unicode characters display incorrectly.

**Solution**: Ensure your terminal supports UTF-8 encoding. Most modern terminals do by default.

---

### Permission Denied (Linux/Mac)

**Error**: `Permission denied` when running `./todo.py`

**Solution**: Add execute permissions:

```bash
chmod +x todo.py
./todo.py add "Test"
```

Or use `python todo.py` instead.

---

## Getting Help

For usage information, run:

```bash
python todo.py help
```

For issues or questions:
- Check this quickstart guide
- Review error messages carefully
- Ensure you're using Python 3.8 or higher

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Add todo | `python todo.py add "text"` |
| List all | `python todo.py list` |
| Complete | `python todo.py complete <id>` |
| Update | `python todo.py update <id> "text"` |
| Delete | `python todo.py delete <id>` |
| Help | `python todo.py help` |

**Remember**: All data is lost when you exit! This is a Phase I limitation.

---

**Version**: 1.0.0 | **Phase**: I (In-Memory CLI) | **Date**: 2025-12-31
