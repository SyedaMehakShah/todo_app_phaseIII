"""
Token blacklist service for JWT revocation.
Implements in-memory blacklist (for production, use Redis).
"""
from datetime import datetime, timedelta
from typing import Set
import asyncio

class TokenBlacklist:
    """Simple in-memory token blacklist."""

    def __init__(self):
        self._blacklist: Set[str] = set()
        self._cleanup_task = None

    async def start(self):
        """Start background cleanup task."""
        self._cleanup_task = asyncio.create_task(self._cleanup_expired())

    async def stop(self):
        """Stop background cleanup task."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

    def add_token(self, token: str):
        """Add token to blacklist."""
        self._blacklist.add(token)

    def is_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted."""
        return token in self._blacklist

    def remove_token(self, token: str):
        """Remove token from blacklist."""
        self._blacklist.discard(token)

    async def _cleanup_expired(self):
        """
        Cleanup expired tokens periodically.
        In production with Redis, use TTL instead.
        """
        while True:
            await asyncio.sleep(3600)  # Cleanup every hour
            # For now, keep all tokens (JWT expiry handles this)
            # In production: decode tokens, remove expired ones

# Global instance
token_blacklist = TokenBlacklist()
