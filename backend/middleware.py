"""
JWT verification middleware for Better Auth tokens.
Validates tokens and extracts user identity.
"""
import jwt
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
from src.services.token_blacklist import token_blacklist

security = HTTPBearer()


class TokenData:
    """Decoded token data."""

    def __init__(self, user_id: str, email: str | None = None):
        self.user_id = user_id
        self.email = email


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenData:
    """
    Verify Better Auth JWT token and extract user info.

    Args:
        credentials: HTTP Bearer credentials from Authorization header

    Returns:
        TokenData with user_id and email

    Raises:
        HTTPException: 401 if token is invalid or expired
    """
    token = credentials.credentials

    # Check if token is blacklisted (revoked)
    if token_blacklist.is_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.jwt_algorithm],
        )

        user_id: str | None = payload.get("sub")
        email: str | None = payload.get("email")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: no user ID")

        return TokenData(user_id=user_id, email=email)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token")


async def verify_user_access(
    user_id: str,
    token_data: TokenData = Depends(verify_token),
) -> TokenData:
    """
    Verify that the token user matches the requested user_id.

    Args:
        user_id: User ID from path parameter
        token_data: Decoded token data

    Returns:
        TokenData if user matches

    Raises:
        HTTPException: 403 if user_id doesn't match token
    """
    if token_data.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this resource",
        )
    return token_data
