"""Defines fixtures available to all tests."""
import pytest

from app import create_app
from dotenv import load_dotenv
from model.db import db

# Load environment variables from .env
load_dotenv(".env")

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
    yield create_app(config_module="pytest-config")


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


# Create a user for testing

# Sign in the user for module testing
