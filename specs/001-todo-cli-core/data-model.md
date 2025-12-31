# Data Model: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2025-12-31
**Phase**: 1 - Design

## Entity: Todo Item

### Description

A Todo Item represents a single task that a user needs to complete. It captures the essential information needed for task management: a unique identifier, the task description, and completion status.

### Attributes

| Attribute | Type | Constraints | Default | Description |
|-----------|------|-------------|---------|-------------|
| **id** | Integer | Positive, sequential, unique, immutable | Auto-assigned (1, 2, 3...) | Unique identifier for the todo item. Assigned sequentially starting from 1. Once assigned, cannot be changed. |
| **text** | String | 1-200 characters, UTF-8, no control chars (\n, \r, \t) | N/A (required) | The task description. Must not be empty or only whitespace. Supports unicode characters and emoji. |
| **completed** | Boolean | True or False | False | Completion status. False when created, transitions to True when marked complete. Not reversible in Phase I. |

### Validation Rules

**ID Validation**:
- Must be a positive integer (> 0)
- Must be unique across all todos
- Sequential assignment (no gaps in Phase I)
- Immutable once assigned

**Text Validation**:
- Minimum length: 1 character (after stripping whitespace)
- Maximum length: 200 characters
- Must not be only whitespace
- Must not contain control characters: newline (\n), carriage return (\r), tab (\t)
- UTF-8 encoding supported (unicode, emoji allowed)

**Completed Validation**:
- Must be boolean (True/False)
- Default value: False on creation
- Can transition: False → True (via complete command)
- Cannot transition: True → False (not reversible in Phase I)

### State Transitions

```
[CREATE] → Active (id=N, text="...", completed=False)
             ↓
          [COMPLETE] → Completed (id=N, text="...", completed=True)
             ↓
          [DELETE] → Deleted (removed from storage)
```

**State Descriptions**:

1. **Active**: Todo exists with completed=False
   - Can be listed (visible in output)
   - Can be completed (transition to Completed state)
   - Can be updated (text can be modified)
   - Can be deleted (removed from storage)

2. **Completed**: Todo exists with completed=True
   - Can be listed (visible in output, marked as complete)
   - Can be completed again (idempotent, no error)
   - Can be updated (text can still be modified)
   - Can be deleted (removed from storage)

3. **Deleted**: Todo removed from storage
   - No longer visible in list
   - Operations on deleted ID result in "Todo not found" error

### Lifecycle

1. **Creation** (via `add` command):
   - ID assigned sequentially (next available ID)
   - Text stored as provided (after validation)
   - Completed set to False
   - Todo added to in-memory list

2. **Active Usage**:
   - List: Display todo with ID, text, and completion indicator
   - Complete: Set completed=True
   - Update: Modify text (ID remains unchanged)

3. **Termination** (via `delete` command):
   - Todo removed from in-memory list
   - ID not reused (sequential counter continues)

### Storage Structure (In-Memory)

**Python Implementation**:
```python
# Global storage
todos = []  # List of todo dictionaries
next_id = 1  # Sequential ID counter

# Individual todo structure
todo = {
    "id": 1,                          # Integer (positive, sequential)
    "text": "Buy groceries",          # String (1-200 chars, UTF-8)
    "completed": False                # Boolean (default False)
}
```

**Example Storage State**:
```python
todos = [
    {"id": 1, "text": "Buy groceries", "completed": False},
    {"id": 2, "text": "Write report", "completed": True},
    {"id": 3, "text": "Call dentist", "completed": False}
]
next_id = 4  # Next todo will get ID 4
```

### Relationships

**None** - Todo Item is a standalone entity with no relationships to other entities (Phase I simplicity).

### Invariants

1. **Unique IDs**: No two todos can have the same ID at any point in time
2. **Sequential IDs**: IDs are assigned in order (1, 2, 3, ...) with no gaps during creation
3. **ID Persistence**: Once assigned, a todo's ID never changes (even when updated)
4. **Deterministic State**: Given the same sequence of operations, the system always reaches the same state
5. **In-Memory Only**: All data lost when application exits (Phase I constraint)

### Edge Cases

**Empty List**:
- When `todos = []`, list command displays "No todos found"
- ID counter still starts at 1 for first todo added

**Completed Idempotence**:
- Calling complete on an already-completed todo succeeds without error
- Completed status remains True (no state change)

**Non-Existent ID Operations**:
- complete, update, delete on non-existent ID returns "Todo not found" error
- No state changes occur

**ID Gaps After Deletion**:
- Deleting ID 2 from [1, 2, 3] leaves [1, 3] in list
- Gap is acceptable - IDs are not reused or reassigned

**Session Boundary**:
- All todos lost when app exits
- ID counter resets to 1 on next app start
- User warned about in-memory limitation (per spec)

## Data Model Validation Against Requirements

| Requirement | Data Model Support |
|-------------|-------------------|
| FR-002 (Sequential IDs) | ✅ `next_id` counter ensures sequential assignment |
| FR-003 (Store in memory) | ✅ Python list `todos` provides in-memory storage |
| FR-008 (Non-empty text) | ✅ Validation rule: min 1 char after strip |
| FR-009 (Positive integer IDs) | ✅ Validation rule: ID > 0, integer type |
| FR-012 (Visual distinction) | ✅ `completed` boolean enables display formatting |
| FR-013 (200 char limit) | ✅ Validation rule: max 200 chars |
| FR-014 (No control chars) | ✅ Validation rule: reject \n, \r, \t |
| FR-015 (UTF-8 support) | ✅ Python 3 strings are Unicode by default |

**Data Model Status**: ✅ **Complete** - All requirements supported
