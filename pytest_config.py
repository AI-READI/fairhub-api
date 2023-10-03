"""Configuration for testing the application."""
from os import environ


class TestConfig:
    FAIRHUB_DATABASE_URL = environ.get("FAIRHUB_DATABASE_URL")
    secret = environ.get("secret")
    TESTING = True
