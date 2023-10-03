"""Defines fixtures available to all tests."""
import json
import os
import unittest.mock

import pytest
from dotenv import load_dotenv

from app import create_app
from model.db import db
from pytest_config import TestConfig

# Load environment variables from .env
load_dotenv(".env")

# Set the FLASK_ENV environment variable to "testing"
os.environ["FLASK_ENV"] = "testing"
print(os.environ.get("FLASK_ENV"))

# Set global variable for study ID
pytest.global_study_id = {}
pytest.global_dataset_id = ""
pytest.global_version_id = ""
pytest.global_arm_id = ""
pytest.global_cc_id = ""
pytest.global_intermediate_id = ""
pytest.global_link_id = ""
pytest.global_location_id = ""
pytest.global_overall_official_id = ""


# Create the flask app for testing
@pytest.fixture()
def flask_app():
    """An application for the tests."""
    yield create_app(config_module="pytest_config")


# Create a test client for the app
@pytest.fixture()
def test_client(flask_app):
    """A test client for the app."""
    with flask_app.test_client() as test_client:
        yield test_client


# Empty local database for testing
@pytest.fixture()
def empty_db(flask_app):
    """Empty the local database."""
    with flask_app.app_context():
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            # print(f"Clear table {table}")
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture()
def create_user(test_client):
    """Create a user for testing."""
    with unittest.mock.patch("pytest_config.TestConfig", TestConfig):
        response = test_client.post(
            "/auth/signup",
            json={"email_address": "sample@gmail.com", "password": "test"},
        )

        assert response.status_code == 201


# Fixture to sign in the user for module testing
@pytest.fixture()
def login_user(test_client):
    """Sign in the user for testing."""
    with unittest.mock.patch("pytest_config.TestConfig", TestConfig):
        response = test_client.post(
            "/auth/login",
            json={"email_address": "sample@gmail.com", "password": "test"},
        )

        assert response.status_code == 200
