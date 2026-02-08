"""
Message model for chat messages.
Messages belong to a conversation and have a role (user or assistant).
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
import uuid


class MessageRole(str, Enum):
    """Message sender role."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """
    Message entity representing a single chat message.

    Attributes:
        id: Unique identifier (UUID)
        conversation_id: Foreign key to conversations table
        role: Message sender role (user or assistant)
        content: Message text content
        created_at: Timestamp when message was created
    """
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(...)
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "conversation_id": "123e4567-e89b-12d3-a456-426614174001",
                "role": "user",
                "content": "Add a task to buy groceries",
                "created_at": "2026-02-06T10:00:00Z",
            }
        }
