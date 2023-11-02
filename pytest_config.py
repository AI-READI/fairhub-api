"""Configuration for testing the application."""
from os import environ
from dotenv import dotenv_values

# Load environment variables from .env
config = dotenv_values(".env")

IN_CI_ENV = environ.get("CI")


def get_env(key):
    """Return environment variable from .env or native environment."""
    return environ.get(key) if IN_CI_ENV else config.get(key)


class TestConfig:
    """Configuration for testing the application."""

    # Load from native environment variables if running in CI environment
    FAIRHUB_DATABASE_URL = get_env("FAIRHUB_DATABASE_URL")
    FAIRHUB_SECRET = get_env("FAIRHUB_SECRET")

    TESTING = True
