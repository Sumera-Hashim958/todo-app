"""Conversation model for Phase III AI Chatbot"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message
    from .task import Task


class Conversation(SQLModel, table=True):
    """Represents a chat session between user and AI assistant"""
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Simplified: using string for hackathon
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships (optional for hackathon)
    # messages: list["Message"] = Relationship(back_populates="conversation")
    # tasks: list["Task"] = Relationship(back_populates="conversation")
