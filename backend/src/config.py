"""
Environment configuration for the Todo application.
Re-exports settings from the root config module.
"""
import logging
import sys
import os

# Load .env file
from dotenv import load_dotenv
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        # Database
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

        # Authentication
        self.BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_EXPIRY_DAYS: int = int(os.getenv("JWT_EXPIRY_DAYS", "7"))

        # Application
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        self.DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

        # CORS - parsed from comma-separated string
        cors_env = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        self.CORS_ORIGINS: list[str] = [
            origin.strip() for origin in cors_env.split(",") if origin.strip()
        ]

        # Logging
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")

        # Rate Limiting
        self.AUTH_RATE_LIMIT: str = os.getenv("AUTH_RATE_LIMIT", "5/minute")


# Global settings instance
settings = Settings()


def configure_logging():
    """
    Configure structured logging for the application.

    Supports both JSON and text formats.
    Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Set log levels for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured: level={settings.LOG_LEVEL}, format={settings.LOG_FORMAT}, environment={settings.ENVIRONMENT}")


# Configure logging on module import
configure_logging()
