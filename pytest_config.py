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

    FAIRHUB_CACHE_DEFAULT_TIMEOUT = get_env("FAIRHUB_CACHE_DEFAULT_TIMEOUT")
    FAIRHUB_CACHE_KEY_PREFIX = get_env("FAIRHUB_CACHE_KEY_PREFIX")
    FAIRHUB_CACHE_HOST = get_env("FAIRHUB_CACHE_HOST")
    FAIRHUB_CACHE_PORT = get_env("FAIRHUB_CACHE_PORT")
    FAIRHUB_CACHE_DB = get_env("FAIRHUB_CACHE_DB")
    FAIRHUB_CACHE_URL = get_env("FAIRHUB_CACHE_URL")
    FAIRHUB_CACHE_TYPE = get_env("FAIRHUB_CACHE_TYPE")

    TESTING = True
