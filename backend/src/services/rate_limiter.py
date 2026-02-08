"""
Simple in-memory rate limiter.
For production, use Redis-based rate limiting.
"""
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple
from fastapi import HTTPException, Request

class RateLimiter:
    """Simple sliding window rate limiter."""

    def __init__(self):
        # Format: {ip: [(timestamp, count)]}
        self._requests: Dict[str, list] = defaultdict(list)

    def check_rate_limit(
        self,
        request: Request,
        max_requests: int,
        window_seconds: int = 60
    ):
        """
        Check if request exceeds rate limit.

        Args:
            request: FastAPI Request object
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds (default: 60)

        Raises:
            HTTPException: 429 if rate limit exceeded
        """
        client_ip = request.client.host if request.client else "unknown"
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)

        # Clean old requests
        self._requests[client_ip] = [
            (ts, count) for ts, count in self._requests[client_ip]
            if ts > window_start
        ]

        # Count requests in current window
        current_count = sum(count for _, count in self._requests[client_ip])

        if current_count >= max_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds."
            )

        # Add current request
        self._requests[client_ip].append((now, 1))

# Global rate limiter instance
rate_limiter = RateLimiter()
