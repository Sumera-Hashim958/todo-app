"""Task model for todo management"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, JSON, Column
from sqlalchemy import JSON as SAJSON


class Task(SQLModel, table=True):
    """Represents a todo task"""
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)
    text: str = Field(max_length=500)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Phase III additions
    conversation_id: Optional[UUID] = Field(default=None, foreign_key="conversations.id")
    created_via: str = Field(default="api")  # "chat" or "api"

    # Intermediate Level additions
    priority: str = Field(default="medium")  # "low", "medium", "high"
    tags: Optional[str] = Field(default=None, sa_column=Column(SAJSON))  # JSON array of tags

    # Advanced Level additions
    due_date: Optional[datetime] = Field(default=None)  # When task is due
    recurrence: Optional[str] = Field(default=None)  # "daily", "weekly", "monthly", or None
    reminder_sent: bool = Field(default=False)  # Track if reminder notification was sent
