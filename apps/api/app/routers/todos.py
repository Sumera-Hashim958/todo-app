"""Todos router with CRUD endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID

from ..database import get_session
from ..models.user import User
from ..models.task import Task
from ..schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from ..middleware.jwt_middleware import get_current_user
from ..services import todo_service
from ..websocket_manager import manager


router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("", response_model=List[TodoResponse])
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all todos for the authenticated user

    Requires JWT authentication
    Returns todos in descending order (newest first)
    """
    todos = todo_service.get_todos(session, current_user.id)
    return todos


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo

    Requires JWT authentication
    Validates text (1-200 chars, no control characters)
    """
    new_todo = todo_service.create_todo(session, current_user.id, todo.text)

    # Broadcast real-time update
    await manager.broadcast_to_user(
        str(current_user.id),
        "todo_created",
        {
            "id": str(new_todo.id),
            "text": new_todo.text,
            "completed": new_todo.completed,
            "created_at": new_todo.created_at.isoformat()
        }
    )

    return new_todo


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo by ID

    Requires JWT authentication
    Returns 404 if todo not found or not owned by user
    """
    todo = todo_service.get_todo(session, todo_id, current_user.id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a todo

    Requires JWT authentication
    Can update text and/or completed status
    Returns 404 if todo not found or not owned by user
    """
    updated_todo = todo_service.update_todo(
        session,
        todo_id,
        current_user.id,
        text=todo_update.text,
        completed=todo_update.completed
    )

    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Broadcast real-time update
    await manager.broadcast_to_user(
        str(current_user.id),
        "todo_updated",
        {
            "id": str(updated_todo.id),
            "text": updated_todo.text,
            "completed": updated_todo.completed,
            "created_at": updated_todo.created_at.isoformat()
        }
    )

    return updated_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a todo

    Requires JWT authentication
    Returns 404 if todo not found or not owned by user
    Returns 204 No Content on success
    """
    deleted = todo_service.delete_todo(session, todo_id, current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Broadcast real-time update
    await manager.broadcast_to_user(
        str(current_user.id),
        "todo_deleted",
        {"id": str(todo_id)}
    )

    return None
