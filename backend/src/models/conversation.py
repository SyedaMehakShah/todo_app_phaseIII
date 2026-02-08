"""
Conversation model for chat sessions.
Each user has one conversation that persists their chat history.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class Conversation(SQLModel, table=True):
    """
    Conversation entity representing a chat session.

    Attributes:
        id: Unique identifier (UUID)
        user_id: Foreign key to users table
        created_at: Timestamp when conversation was created
        updated_at: Timestamp when conversation was last active
    """
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "created_at": "2026-02-06T10:00:00Z",
                "updated_at": "2026-02-06T10:30:00Z",
            }
        }
