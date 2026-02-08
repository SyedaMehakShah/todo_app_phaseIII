"""
Health check endpoint.
No authentication required.
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check() -> dict:
    """
    Check if the API is running.

    Returns:
        dict with status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }
