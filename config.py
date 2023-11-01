"""Configuration for the application."""
from dotenv import dotenv_values

# Load environment variables from .env
config = dotenv_values(".env")

FAIRHUB_DATABASE_URL = config.get("FAIRHUB_DATABASE_URL")
FAIRHUB_SECRET = config.get("FAIRHUB_SECRET")

FAIRHUB_AZURE_READ_SAS_TOKEN = config.get("FAIRHUB_AZURE_READ_SAS_TOKEN")
FAIRHUB_AZURE_STORAGE_ACCOUNT_NAME = config.get("FAIRHUB_AZURE_STORAGE_ACCOUNT_NAME")
