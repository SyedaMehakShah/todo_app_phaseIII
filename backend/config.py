"""
Configuration module for the backend application.
Loads settings from environment variables.
"""
from pydantic import field_validator
from functools import lru_cache
import os

# Load .env file
from dotenv import load_dotenv
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        # Database
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

        # Authentication
        self.better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
        self.jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_expiry_days: int = int(os.getenv("JWT_EXPIRY_DAYS", "7"))

        # OpenAI
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

        # Server
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"

        # CORS - parsed from CORS_ORIGINS environment variable
        cors_env = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        self.cors_origins: list[str] = [
            origin.strip() for origin in cors_env.split(",") if origin.strip()
        ]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience access
settings = get_settings()
