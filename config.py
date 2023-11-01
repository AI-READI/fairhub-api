"""Configuration for the application."""
from os import environ
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(".env")

FAIRHUB_DATABASE_URL = environ.get("FAIRHUB_DATABASE_URL")
FAIRHUB_SECRET = environ.get("FAIRHUB_SECRET")

FAIRHUB_AZURE_READ_SAS_TOKEN = environ.get("FAIRHUB_AZURE_READ_SAS_TOKEN")
FAIRHUB_AZURE_STORAGE_ACCOUNT_NAME = environ.get("FAIRHUB_AZURE_STORAGE_ACCOUNT_NAME")
