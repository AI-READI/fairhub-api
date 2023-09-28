"""Defines fixtures available to all tests."""
import os
import pytest

from app import create_app
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(".env")


# Create the flask app for testing
@pytest.fixture()
def flask_app():
    """An application for the tests."""
    yield create_app(config_module="pytest-config")


# Create a test client for the app
@pytest.fixture()
def test_client(flask_app):
    """A test client for the app."""
    with flask_app.test_client() as test_client:
        yield test_client


# Create a user for testing

# Sign in the user for module testing
