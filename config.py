"""Configuration for the application."""
from os import environ
from pathlib import Path
from dotenv import dotenv_values

# Check if `.env` file exists
env_path = Path(".") / ".env"

LOCAL_ENV_FILE = env_path.exists()

# Load environment variables from .env
config = dotenv_values(".env")


def get_env(key):
    """Return environment variable from .env or native environment."""
    return config.get(key) if LOCAL_ENV_FILE else environ.get(key)


FAIRHUB_DATABASE_URL = get_env("FAIRHUB_DATABASE_URL")
FAIRHUB_SECRET = get_env("FAIRHUB_SECRET")
FAIRHUB_LOCALHOST_URL = get_env("FAIRHUB_LOCALHOST_URL")

FAIRHUB_AZURE_READ_SAS_TOKEN = get_env("FAIRHUB_AZURE_READ_SAS_TOKEN")
FAIRHUB_AZURE_STORAGE_ACCOUNT_NAME = get_env("FAIRHUB_AZURE_STORAGE_ACCOUNT_NAME")
