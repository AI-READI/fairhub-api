"""Configuration for the application."""
from os import environ

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
