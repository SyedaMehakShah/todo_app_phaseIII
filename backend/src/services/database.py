"""
Database connection service.
Supports both PostgreSQL (production) and SQLite (development).
Provides async database sessions and connection management.
"""
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import os


# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")


def get_async_url(url: str) -> str:
    """Convert database URL to async version."""
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://")
    elif url.startswith("postgresql+asyncpg://"):
        return url
    elif url.startswith("sqlite:///"):
        # SQLite async requires aiosqlite
        return url.replace("sqlite:///", "sqlite+aiosqlite:///")
    elif url.startswith("sqlite+aiosqlite:///"):
        return url
    return url


ASYNC_DATABASE_URL = get_async_url(DATABASE_URL)

# Determine if we're using SQLite
IS_SQLITE = "sqlite" in ASYNC_DATABASE_URL.lower()

# Create async engine
engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    """Get or create the async database engine."""
    global engine
    if engine is None:
        # SQLite doesn't support pool settings
        if IS_SQLITE:
            engine = create_async_engine(
                ASYNC_DATABASE_URL,
                echo=os.getenv("DEBUG", "false").lower() == "true",
                connect_args={"check_same_thread": False},
            )
        else:
            engine = create_async_engine(
                ASYNC_DATABASE_URL,
                echo=os.getenv("DEBUG", "false").lower() == "true",
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
            )
    return engine


# Async session factory - initialized lazily to avoid binding to None engine
_async_session_factory = None


def get_session_factory():
    """Get or create the async session factory."""
    global _async_session_factory
    if _async_session_factory is None:
        _async_session_factory = sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_factory


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.

    Usage:
        async with get_session() as session:
            result = await session.exec(select(Task))
    """
    async with AsyncSession(get_engine()) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Initialize database tables."""
    async with get_engine().begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None
