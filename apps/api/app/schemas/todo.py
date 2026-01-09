"""Pydantic schemas for todo endpoints"""
from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID


class TodoCreate(BaseModel):
    """Request schema for creating a todo"""
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Validate todo text"""
        # Trim whitespace
        v = v.strip()

        if not v:
            raise ValueError("Todo text cannot be empty")

        if len(v) > 200:
            raise ValueError("Todo text must be 200 characters or less")

        # Check for control characters
        if any(ord(char) < 32 for char in v):
            raise ValueError("Todo text cannot contain control characters")

        return v


class TodoUpdate(BaseModel):
    """Request schema for updating a todo"""
    text: str | None = None
    completed: bool | None = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str | None) -> str | None:
        """Validate todo text if provided"""
        if v is None:
            return v

        # Trim whitespace
        v = v.strip()

        if not v:
            raise ValueError("Todo text cannot be empty")

        if len(v) > 200:
            raise ValueError("Todo text must be 200 characters or less")

        # Check for control characters
        if any(ord(char) < 32 for char in v):
            raise ValueError("Todo text cannot contain control characters")

        return v


class TodoResponse(BaseModel):
    """Response schema for todo data"""
    id: UUID
    text: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
