"""
Chat endpoint for AI-powered task management.
Constitution Principle VI: Single chat endpoint for all interactions.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from .middleware.jwt_auth import get_current_user_id
# Using Gemini-based agent
from src.services.agent_gemini import process_message
from src.services.conversation import (
    get_conversation_history,
    save_message,
    get_or_create_conversation,
    get_full_conversation_history,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Chat"])


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=10000)


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""

    message: str
    conversation_id: str


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def send_chat_message(
    user_id: str,
    request: ChatRequest,
    authenticated_user_id: str = Depends(get_current_user_id),
) -> ChatResponse:
    """
    Send a chat message and receive AI response.

    The AI agent processes the message, calls MCP tools as needed,
    and returns a friendly response.

    Args:
        user_id: User ID (must match JWT sub claim)
        request: Chat request with message

    Returns:
        AI response and conversation ID
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch",
        )
    
    try:
        # Get or create conversation
        conversation = await get_or_create_conversation(user_id)
        # Capture the conversation ID to avoid detached instance issues
        conversation_id = conversation.id

        # Get conversation history for context
        history = await get_conversation_history(user_id, limit=20)

        # Save user message
        await save_message(user_id, "user", request.message)

        # Process with AI agent
        response = await process_message(user_id, request.message, history)

        # Save assistant response
        await save_message(user_id, "assistant", response)

        return ChatResponse(
            message=response,
            conversation_id=conversation_id,
        )

    except Exception as e:
        # Handle specific errors from the AI agent
        error_msg = str(e).lower()
        if "quota" in error_msg or "rate" in error_msg:
            logger.warning(f"Gemini rate limit or quota exceeded for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="The AI service is busy. Please try again in a moment.",
            )
        elif "auth" in error_msg or "api" in error_msg:
            logger.error(f"Gemini authentication or API error for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service configuration error. Please contact support.",
            )
        else:
            logger.exception(f"Unexpected error in chat for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong. Please try again later.",
            )


@router.get("/api/{user_id}/conversations")
async def get_conversations(
    user_id: str,
    limit: int = 50,
    authenticated_user_id: str = Depends(get_current_user_id),
) -> dict:
    """
    Get conversation history for a user.

    Args:
        user_id: User ID (must match JWT sub claim)
        limit: Maximum messages to return (default: 50)

    Returns:
        Conversation ID and messages list
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch",
        )
    
    try:
        return await get_full_conversation_history(user_id, limit)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve conversation history.",
        )
