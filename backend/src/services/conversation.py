"""
Conversation service for managing chat sessions and messages.
Handles conversation persistence and history retrieval.
"""
from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import select
from src.services.database import get_session
from src.models import Conversation, Message, MessageRole


async def get_or_create_conversation(user_id: str) -> Conversation:
    """
    Get existing conversation or create new one for user.
    Each user has one conversation (MVP simplification).

    Args:
        user_id: The user's ID

    Returns:
        The user's conversation
    """
    async with get_session() as session:
        query = select(Conversation).where(Conversation.user_id == user_id)
        result = await session.exec(query)
        conversation = result.first()

        if conversation:
            # Create a new Conversation object with the same data to avoid detached instance issues
            fresh_conversation = Conversation(
                id=conversation.id,
                user_id=conversation.user_id,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at
            )
            return fresh_conversation

        # Create new conversation
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Create a new Conversation object with the same data to avoid detached instance issues
        fresh_conversation = Conversation(
            id=conversation.id,
            user_id=conversation.user_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )
        return fresh_conversation


async def get_conversation_history(
    user_id: str, limit: int = 50
) -> list[dict]:
    """
    Get recent messages from user's conversation.

    Args:
        user_id: The user's ID
        limit: Maximum number of messages to return

    Returns:
        List of message dicts with role and content
    """
    async with get_session() as session:
        # Get conversation
        conv_query = select(Conversation).where(Conversation.user_id == user_id)
        result = await session.exec(conv_query)
        conversation = result.first()

        if not conversation:
            return []

        # Get messages
        msg_query = (
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        result = await session.exec(msg_query)
        messages = result.all()

        # Create fresh copies of the messages to avoid detached instance issues
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]


async def save_message(
    user_id: str, role: str, content: str
) -> Message:
    """
    Save a message to the conversation.

    Args:
        user_id: The user's ID
        role: Message role ('user' or 'assistant')
        content: Message content

    Returns:
        The saved message
    """
    async with get_session() as session:
        # Get or create conversation within the same session
        conv_query = select(Conversation).where(Conversation.user_id == user_id)
        result = await session.exec(conv_query)
        conversation = result.first()

        if not conversation:
            # Create new conversation
            conversation = Conversation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)

        # Create message
        message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation.id,
            role=MessageRole.USER if role == "user" else MessageRole.ASSISTANT,
            content=content,
            created_at=datetime.utcnow(),
        )
        session.add(message)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

        await session.commit()
        await session.refresh(message)

        # Create a new Message object with the same data to avoid detached instance issues
        fresh_message = Message(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at
        )
        return fresh_message


async def get_full_conversation_history(user_id: str, limit: int = 50) -> dict:
    """
    Get full conversation history with metadata.

    Args:
        user_id: The user's ID
        limit: Maximum number of messages

    Returns:
        Dict with conversation_id and messages list
    """
    async with get_session() as session:
        # Get conversation
        conv_query = select(Conversation).where(Conversation.user_id == user_id)
        result = await session.exec(conv_query)
        conversation = result.first()

        if not conversation:
            return {"conversation_id": None, "messages": []}

        # Get messages
        msg_query = (
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        result = await session.exec(msg_query)
        messages = result.all()

        return {
            "conversation_id": conversation.id,  # This should be fine since it's just the ID
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role.value,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat(),
                }
                for msg in messages  # These should be fine since we're extracting values
            ],
        }
