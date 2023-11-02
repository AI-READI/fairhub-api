"""Configuration for the application."""
from os import environ
from pathlib import Path
from dotenv import dotenv_values

# Check if `.env` file exists
env_path = Path(".") / ".env"

LOCAL_ENV_FILE = env_path.exists()

# Load environment variables from .env
config = dotenv_values(".env")

<<<<<<< HEAD
from dotenv import load_dotenv
load_dotenv(".env")

FAIRHUB_DATABASE_URL = environ.get("FAIRHUB_DATABASE_URL")
FAIRHUB_SECRET = environ.get("FAIRHUB_SECRET")
CACHE_DEFAULT_TIMEOUT = environ.get("CACHE_DEFAULT_TIMEOUT")
CACHE_KEY_PREFIX = environ.get("CACHE_KEY_PREFIX")
CACHE_HOST = environ.get("CACHE_HOST")
CACHE_PORT = environ.get("CACHE_PORT")
CACHE_DB = environ.get("CACHE_DB")
CACHE_URL = environ.get("CACHE_URL")
=======

def get_env(key):
    """Return environment variable from .env or native environment."""
    return config.get(key) if LOCAL_ENV_FILE else environ.get(key)


FAIRHUB_DATABASE_URL = get_env("FAIRHUB_DATABASE_URL")
FAIRHUB_SECRET = get_env("FAIRHUB_SECRET")

FAIRHUB_AZURE_READ_SAS_TOKEN = get_env("FAIRHUB_AZURE_READ_SAS_TOKEN")
FAIRHUB_AZURE_STORAGE_ACCOUNT_NAME = get_env("FAIRHUB_AZURE_STORAGE_ACCOUNT_NAME")
>>>>>>> fb3fb5cace0ebc1c41c9914afad862ec4a889831
