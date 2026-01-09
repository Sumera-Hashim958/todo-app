"""Todo service layer for CRUD operations"""
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID

from ..models.task import Task


def get_todos(session: Session, user_id: int) -> List[Task]:
    """
    Get all todos for a user

    Args:
        session: Database session
        user_id: User ID (integer from User model)

    Returns:
        List of Task objects
    """
    # Convert user_id to string for Task model compatibility
    user_id_str = str(user_id)

    statement = select(Task).where(
        Task.user_id == user_id_str,
        Task.created_via == "api"  # Only API-created tasks for web app
    ).order_by(Task.created_at.desc())

    return list(session.exec(statement).all())


def create_todo(session: Session, user_id: int, text: str) -> Task:
    """
    Create a new todo

    Args:
        session: Database session
        user_id: User ID
        text: Todo text

    Returns:
        Created Task object
    """
    task = Task(
        user_id=str(user_id),
        text=text,
        created_via="api"
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_todo(session: Session, todo_id: UUID, user_id: int) -> Optional[Task]:
    """
    Get a specific todo by ID

    Args:
        session: Database session
        todo_id: Todo UUID
        user_id: User ID (for ownership verification)

    Returns:
        Task object if found and owned by user, None otherwise
    """
    statement = select(Task).where(
        Task.id == todo_id,
        Task.user_id == str(user_id)
    )

    return session.exec(statement).first()


def update_todo(
    session: Session,
    todo_id: UUID,
    user_id: int,
    text: Optional[str] = None,
    completed: Optional[bool] = None
) -> Optional[Task]:
    """
    Update a todo

    Args:
        session: Database session
        todo_id: Todo UUID
        user_id: User ID (for ownership verification)
        text: New text (optional)
        completed: New completion status (optional)

    Returns:
        Updated Task object if found and owned by user, None otherwise
    """
    task = get_todo(session, todo_id, user_id)

    if not task:
        return None

    if text is not None:
        task.text = text

    if completed is not None:
        task.completed = completed

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_todo(session: Session, todo_id: UUID, user_id: int) -> bool:
    """
    Delete a todo

    Args:
        session: Database session
        todo_id: Todo UUID
        user_id: User ID (for ownership verification)

    Returns:
        True if deleted, False if not found or not owned by user
    """
    task = get_todo(session, todo_id, user_id)

    if not task:
        return False

    session.delete(task)
    session.commit()

    return True
