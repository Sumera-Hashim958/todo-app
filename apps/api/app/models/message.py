"""Message model for Phase III AI Chatbot"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column, JSON
from enum import Enum


class MessageRole(str, Enum):
    """Message role enum"""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """Represents a single message in a conversation"""
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field()  # Simplified: "user" or "assistant"
    content: str = Field()
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
