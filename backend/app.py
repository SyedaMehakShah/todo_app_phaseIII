from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

# Import the lifespan from main to handle startup/shutdown
from src.database import init_db, close_db

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Close database connections
    await close_db()

# Initialize FastAPI application
app = FastAPI(
    title="Todo App API",
    description="Phase II Todo Full-Stack Web Application API",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Import and include routers
from src.api.v1 import auth, tasks
from src.api import chat

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/v1", tags=["Tasks"])
app.include_router(chat.router)