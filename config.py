"""Configuration for the application."""
from os import environ

FAIRHUB_DATABASE_URL = environ.get("FAIRHUB_DATABASE_URL")
secret = environ.get("secret")
