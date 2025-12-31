"""
Output formatting module for Todo CLI

Provides functions for formatting output and error messages
"""

import sys


def format_todo(todo):
    """
    Format a single todo item for display

    Args:
        todo: Dictionary with 'id', 'text', 'completed' keys

    Returns:
        str: Formatted todo string
    """
    status = "[✓]" if todo['completed'] else "[ ]"
    return f"  {todo['id']:>2}  {status} {todo['text']}"


def format_todo_list(todos):
    """
    Format a list of todos for display

    Args:
        todos: List of todo dictionaries

    Returns:
        str: Formatted output string
    """
    if not todos:
        return "No todos found"

    lines = []
    for todo in todos:
        lines.append(format_todo(todo))

    return "\n".join(lines)


def error_exit(message, exit_code=1):
    """
    Print error message to stderr and exit with non-zero code

    Args:
        message: Error message to display
        exit_code: Exit code (default: 1)
    """
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)


def success_message(message):
    """
    Print success message to stdout

    Args:
        message: Success message to display
    """
    print(message)
