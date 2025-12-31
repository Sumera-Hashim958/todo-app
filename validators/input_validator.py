"""
Input validation module for Todo CLI

Provides validation functions for todo text and IDs
"""

import re


def validate_text(text):
    """
    Validate todo text input

    Args:
        text: The todo text to validate

    Returns:
        str: The validated text (stripped)

    Raises:
        ValueError: If text is invalid
    """
    if not text or not text.strip():
        raise ValueError("Todo text cannot be empty")

    text = text.strip()

    if len(text) > 200:
        raise ValueError("Todo text too long (max 200 characters)")

    # Check for control characters (newlines, tabs, carriage returns)
    if re.search(r'[\n\r\t]', text):
        raise ValueError("Todo text cannot contain newlines or tabs")

    return text


def validate_id(id_str):
    """
    Validate todo ID input

    Args:
        id_str: The ID string to validate

    Returns:
        int: The validated ID as an integer

    Raises:
        ValueError: If ID is invalid
    """
    try:
        id_val = int(id_str)
        if id_val <= 0:
            raise ValueError("Invalid ID: ID must be a positive number")
        return id_val
    except (ValueError, TypeError):
        raise ValueError("Invalid ID: ID must be a positive number")
