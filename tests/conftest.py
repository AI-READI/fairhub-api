"""Defines fixtures available to all tests."""
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

# Set global variable for study ID
pytest.global_study_id = {}
pytest.global_dataset_id = ""
pytest.global_version_id = ""
pytest.global_arm_id = ""
pytest.global_available_ipd_id = ""
pytest.global_cc_id = ""
pytest.global_identification_id = ""
pytest.global_intervention_id = ""
pytest.global_link_id = ""
pytest.global_location_id = ""
pytest.global_overall_official_id = ""
pytest.global_reference_id = ""


# Create the flask app for testing
@pytest.fixture()
def flask_app():
    """An application for the tests."""
    yield create_app(config_module="pytest_config")


# Create a test client for the app
@pytest.fixture()
def _test_client(flask_app):
    """A test client for the app."""
    with flask_app.test_client() as _test_client:
        yield _test_client


# Empty local database for testing
@pytest.fixture()
def _empty_db(flask_app):
    """Empty the local database."""
    with flask_app.app_context():
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            # print(f"Clear table {table}")
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture()
def _create_user(_test_client):
    """Create a user for testing."""
    with unittest.mock.patch("pytest_config.TestConfig", TestConfig):
        response = _test_client.post(
            "/auth/signup",
            json={
                "email_address": "sample@gmail.com",
                "password": "Testingyeshello11!",
            },
        )

        assert response.status_code == 201


# Fixture to sign in the user for module testing
@pytest.fixture()
def _login_user(_test_client):
    """Sign in the user for testing."""
    with unittest.mock.patch("pytest_config.TestConfig", TestConfig):
        response = _test_client.post(
            "/auth/login",
            json={
                "email_address": "sample@gmail.com",
                "password": "Testingyeshello11!",
            },
        )

        assert response.status_code == 200
