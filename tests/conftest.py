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

# Set global variable for study ID
# Study variables for main client
pytest.global_study_id = {}
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

# study variables for admin client and editor client
pytest.global_alternative_identifier_id_admin = ""
pytest.global_alternative_identifier_id_editor = ""
pytest.global_dataset_contributor_id_admin = ""
pytest.global_dataset_contributor_id_editor = ""
pytest.global_dataset_contributor_id_admin = ""
pytest.global_dataset_contributor_id_editor = ""
pytest.global_editor_arm_id_admin = ""
pytest.global_editor_arm_id_editor = ""
pytest.global_editor_available_ipd_id_admin = ""
pytest.global_editor_available_ipd_id_editor = ""
pytest.global_admin_cc_id_admin = ""
pytest.global_editor_cc_id_editor = ""
pytest.global_identification_id_admin = ""
pytest.global_identification_id_editor = ""
pytest.global_intervention_id_admin = ""
pytest.global_intervention_id_editor = ""
pytest.global_link_id_admin = ""
pytest.global_link_id_editor = ""
pytest.global_location_id_admin = ""
pytest.global_location_id_editor = ""
pytest.global_overall_official_id_admin = ""
pytest.global_overall_official_id_editor = ""

# Dataset variables use for testing
pytest.global_dataset_id = ""
pytest.global_dataset_version_id = ""
pytest.global_alternative_identifier_id = ""
pytest.global_dataset_contributor_id = ""
pytest.global_dataset_creator_id = ""
pytest.global_dataset_date_id = ""
pytest.global_dataset_description_id = ""
pytest.global_dataset_funder_id = ""
pytest.global_dataset_related_item_id = ""
pytest.global_dataset_related_item_contributor_id = ""
pytest.global_dataset_related_item_creator_id = ""
pytest.global_dataset_related_item_identifier_id = ""
pytest.global_dataset_related_item_title_id = ""
pytest.global_dataset_rights_id = ""
pytest.global_dataset_subject_id = ""
pytest.global_dataset_title_id = ""

# User token codes
pytest.global_admin_token = ""
pytest.global_editor_token = ""
pytest.global_viewer_token = ""


# Create the flask app for testing
@pytest.fixture(scope="session")
def flask_app():
    """An application for the tests."""
    return create_app(config_module="pytest_config")


# Create a test client for the app
# pylint: disable=redefined-outer-name
@pytest.fixture(scope="session")
def _test_client(flask_app):
    """A test client for the app."""
    with flask_app.test_client() as _test_client:
        yield _test_client


# Empty local database for testing
# pylint: disable=redefined-outer-name
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
                "email_address": "test@fairhub.io",
                "password": "Testingyeshello11!",
                "code": "",
            },
        )

        assert response.status_code == 201


# Fixture to sign in the user for module testing
@pytest.fixture(scope="session")
def _logged_in_client(flask_app):
    """Sign in the user for testing."""
    with flask_app.app_context():
        with flask_app.test_client() as _test_client:
            with unittest.mock.patch("pytest_config.TestConfig", TestConfig):
                response = _test_client.post(
                    "/auth/login",
                    json={
                        "email_address": "test@fairhub.io",
                        "password": "Testingyeshello11!",
                    },
                )

                assert response.status_code == 200
                response.close()
                yield _test_client


@pytest.fixture(scope="session")
def _test_invite_study_contributor(_logged_in_client):
    """Test invite study contributor."""
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
        f"/study/{study_id}/contributor",
        json={"email_address": "editor@gmail.com", "role": "editor"},
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)

    pytest.global_editor_token = response_data["token"]

    response = _logged_in_client.post(
        f"/study/{study_id}/contributor",
        json={"email_address": "admin@gmail.com", "role": "admin"},
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_admin_token = response_data["token"]

    response = _logged_in_client.post(
        f"/study/{study_id}/contributor",
        json={"email_address": "viewer@gmail.com", "role": "viewer"},
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_viewer_token = response_data["token"]


@pytest.fixture(scope="session")
def _create_admin_user(flask_app):
    """Create an admin user for testing."""
    with flask_app.test_client() as _test_client:
        with unittest.mock.patch("pytest_config.TestConfig", TestConfig):
            response = _test_client.post(
                "/auth/signup",
                json={
                    "email_address": "admin@gmail.com",
                    "password": "Testingyeshello11!",
                    "code": pytest.global_admin_token,
                },
            )

            assert response.status_code == 201


@pytest.fixture(scope="session")
def _create_editor_user(flask_app):
    """Create an editor user for testing."""
    with flask_app.test_client() as _test_client:
        with unittest.mock.patch("pytest_config.TestConfig", TestConfig):
            response = _test_client.post(
                "/auth/signup",
                json={
                    "email_address": "editor@gmail.com",
                    "password": "Testingyeshello11!",
                    "code": pytest.global_editor_token,
                },
            )

            assert response.status_code == 201


@pytest.fixture(scope="session")
def _create_viewer_user(flask_app):
    """Create a viewer user for testing."""
    with flask_app.test_client() as _test_client:
        with unittest.mock.patch("pytest_config.TestConfig", TestConfig):
            response = _test_client.post(
                "/auth/signup",
                json={
                    "email_address": "viewer@gmail.com",
                    "password": "Testingyeshello11!",
                    "code": pytest.global_viewer_token,
                },
            )

            assert response.status_code == 201


@pytest.fixture(scope="session")
def clients(flask_app):
    """Signs in all clients needed for testing"""
    ctx = flask_app.app_context()
    ctx.push()

    _logged_in_client = flask_app.test_client()
    _admin_client = flask_app.test_client()
    _editor_client = flask_app.test_client()
    _viewer_client = flask_app.test_client()

    with unittest.mock.patch("pytest_config.TestConfig", TestConfig):
        response = _logged_in_client.post(
            "/auth/login",
            json={
                "email_address": "test@fairhub.io",
                "password": "Testingyeshello11!",
            },
        )
        assert response.status_code == 200

        response = _admin_client.post(
            "/auth/login",
            json={
                "email_address": "admin@gmail.com",
                "password": "Testingyeshello11!",
            },
        )
        assert response.status_code == 200

        response = _editor_client.post(
            "/auth/login",
            json={
                "email_address": "editor@gmail.com",
                "password": "Testingyeshello11!",
            },
        )
        assert response.status_code == 200

        response = _viewer_client.post(
            "/auth/login",
            json={
                "email_address": "viewer@gmail.com",
                "password": "Testingyeshello11!",
            },
        )
        assert response.status_code == 200

    yield _logged_in_client, _admin_client, _editor_client, _viewer_client

    ctx.pop()
