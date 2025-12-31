"""
Todo service module - CRUD operations for todos

Manages the in-memory todo list
"""

from validators.input_validator import validate_text, validate_id

# Import global storage from todo.py
import todo


def add_todo(text):
    """
    Add a new todo item

    Args:
        text: The todo text

    Returns:
        dict: The created todo item

    Raises:
        ValueError: If validation fails
    """
    # Validate text
    validated_text = validate_text(text)

    # Create todo dictionary
    new_todo = {
        "id": todo.next_id,
        "text": validated_text,
        "completed": False
    }

    # Add to storage
    todo.todos.append(new_todo)
    todo.next_id += 1

    return new_todo


def find_todo_by_id(todo_id):
    """
    Find a todo by ID

    Args:
        todo_id: The todo ID to find

    Returns:
        dict: The todo item if found, None otherwise
    """
    for t in todo.todos:
        if t["id"] == todo_id:
            return t
    return None


def get_all_todos():
    """
    Get all todos

    Returns:
        list: Copy of all todos
    """
    return todo.todos.copy()


def complete_todo(todo_id):
    """
    Mark a todo as complete

    Args:
        todo_id: The todo ID

    Returns:
        dict: The completed todo

    Raises:
        ValueError: If todo not found
    """
    validated_id = validate_id(str(todo_id))
    found_todo = find_todo_by_id(validated_id)

    if not found_todo:
        raise ValueError("Todo not found")

    found_todo["completed"] = True
    return found_todo


def update_todo(todo_id, new_text):
    """
    Update a todo's text

    Args:
        todo_id: The todo ID
        new_text: The new text

    Returns:
        dict: The updated todo

    Raises:
        ValueError: If validation fails or todo not found
    """
    validated_id = validate_id(str(todo_id))
    validated_text = validate_text(new_text)

    found_todo = find_todo_by_id(validated_id)

    if not found_todo:
        raise ValueError("Todo not found")

    found_todo["text"] = validated_text
    return found_todo


def delete_todo(todo_id):
    """
    Delete a todo

    Args:
        todo_id: The todo ID

    Returns:
        dict: The deleted todo

    Raises:
        ValueError: If todo not found
    """
    validated_id = validate_id(str(todo_id))
    found_todo = find_todo_by_id(validated_id)

    if not found_todo:
        raise ValueError("Todo not found")

    todo.todos.remove(found_todo)
    return found_todo
