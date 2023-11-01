"""Configuration for testing the application."""
from dotenv import dotenv_values

# Load environment variables from .env
config = dotenv_values(".env")


class TestConfig:
    """Configuration for testing the application."""

    FAIRHUB_DATABASE_URL = config.get("FAIRHUB_DATABASE_URL")
    FAIRHUB_SECRET = config.get("FAIRHUB_SECRET")
    TESTING = True
