"""
Authentication API endpoints.
Handles user signup and signin.
"""
from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
import jwt
from datetime import datetime, timedelta

from ..models.user import User
from ..services.database import get_engine
from ..services.token_blacklist import token_blacklist
from ..services.rate_limiter import rate_limiter
from config import settings

router = APIRouter(tags=["auth"])


class SignupRequest(BaseModel):
    """Signup request payload."""
    email: EmailStr
    password: str


class SigninRequest(BaseModel):
    """Signin request payload."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User information in auth response."""
    id: str
    email: str
    email_verified: bool
    created_at: str
    updated_at: str


class AuthResponse(BaseModel):
    """Authentication response."""
    token: str
    user: UserResponse


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_token(user_id: str) -> str:
    """Create a JWT token for a user."""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")
    return token


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, http_request: Request):
    """Create a new user account."""
    # Rate limiting: 5 requests per minute
    rate_limiter.check_rate_limit(http_request, max_requests=5, window_seconds=60)
    async with AsyncSession(get_engine()) as session:
        # Check if user already exists
        result = await session.execute(
            select(User).where(User.email == request.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = hash_password(request.password)

        # Create user
        user = User(
            email=request.email,
            password_hash=hashed_password,
            email_verified=False
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        # Generate token
        token = create_token(str(user.id))

        return AuthResponse(
            token=token,
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                email_verified=user.email_verified,
                created_at=user.created_at.isoformat(),
                updated_at=user.updated_at.isoformat()
            )
        )


@router.post("/signin", response_model=AuthResponse)
async def signin(request: SigninRequest, http_request: Request):
    """Sign in to an existing account."""
    # Rate limiting: 10 requests per minute
    rate_limiter.check_rate_limit(http_request, max_requests=10, window_seconds=60)
    async with AsyncSession(get_engine()) as session:
        # Find user
        result = await session.execute(
            select(User).where(User.email == request.email)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Generate token
        token = create_token(str(user.id))

        return AuthResponse(
            token=token,
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                email_verified=user.email_verified,
                created_at=user.created_at.isoformat(),
                updated_at=user.updated_at.isoformat()
            )
        )


@router.post("/logout")
async def logout(http_request: Request):
    """
    Logout user by revoking JWT token.
    Token must be provided in Authorization header.
    """
    auth_header = http_request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = auth_header.split(" ")[1]
    
    # Add token to blacklist
    token_blacklist.add_token(token)
    
    return {"message": "Successfully logged out"}
