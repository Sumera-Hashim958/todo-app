#!/usr/bin/env python3
"""
Todo CLI - Simple command-line todo management

Phase I: In-memory implementation (no persistence)
"""

import sys
import re

# Global in-memory storage
todos = []
next_id = 1

# Import modules after globals are defined
from services import todo_service
from utils.formatter import error_exit, success_message, format_todo_list
from validators.input_validator import validate_text, validate_id


def print_help():
    """Display usage information"""
    help_text = """Todo CLI - Simple command-line todo management

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
"""
    print(help_text)


def handle_add(args):
    """Handle the add command"""
    if len(args) < 1:
        error_exit("Missing required argument: text", 2)

    text = " ".join(args)

    try:
        todo = todo_service.add_todo(text)
        success_message(f"Added: {todo['text']}")
    except ValueError as e:
        error_exit(str(e))


def handle_list(args):
    """Handle the list command"""
    todos = todo_service.get_all_todos()
    output = format_todo_list(todos)
    print(output)


def handle_complete(args):
    """Handle the complete command"""
    if len(args) < 1:
        error_exit("Missing required argument: ID", 2)

    try:
        todo_id = validate_id(args[0])
        todo = todo_service.complete_todo(todo_id)
        success_message(f"Completed: {todo['text']}")
    except ValueError as e:
        error_exit(str(e))


def handle_update(args):
    """Handle the update command"""
    if len(args) < 1:
        error_exit("Missing required argument: ID", 2)
    if len(args) < 2:
        error_exit("Missing required argument: text", 2)

    try:
        todo_id = validate_id(args[0])
        new_text = " ".join(args[1:])
        todo = todo_service.update_todo(todo_id, new_text)
        success_message(f"Updated: {todo['text']}")
    except ValueError as e:
        error_exit(str(e))


def handle_delete(args):
    """Handle the delete command"""
    if len(args) < 1:
        error_exit("Missing required argument: ID", 2)

    try:
        todo_id = validate_id(args[0])
        todo = todo_service.delete_todo(todo_id)
        success_message(f"Deleted: {todo['text']}")
    except ValueError as e:
        error_exit(str(e))


def main():
    """Main entry point"""
    # Configure UTF-8 encoding for cross-platform emoji/unicode support
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    # Check for command
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command = sys.argv[1]
    args = sys.argv[2:]

    # Route commands
    if command == "add":
        handle_add(args)
    elif command == "list":
        handle_list(args)
    elif command == "complete":
        handle_complete(args)
    elif command == "update":
        handle_update(args)
    elif command == "delete":
        handle_delete(args)
    elif command == "help" or command == "--help":
        print_help()
    else:
        error_exit(f"Unknown command '{command}'\nTry 'python todo.py help' for usage information.", 2)


if __name__ == "__main__":
    main()
