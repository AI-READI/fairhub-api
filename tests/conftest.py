"""Defines fixtures available to all tests."""
import pytest

from app import create_app


@pytest.fixture()
def app():
    """An application for the tests."""
    config = {
        "TESTING": True,
        "FAIRHUB_DATABASE_URL": "postgresql://admin:root@localhost:5432/fairhub_local"
    }
    testing_config = True

    flask_app = create_app(config)

    flask_app.config.update(
        {
            "TESTING": True,
            "FAIRHUB_DATABASE_URL": "postgresql://admin:root@localhost:5432/fairhub_local"
        }
    )

    # other setup can go here

    yield flask_app

    # clean up / reset resources here


@pytest.fixture()
def client(flask_app):
    """A test client for the app."""
    return flask_app.test_client()


@pytest.fixture()
def runner(flask_app):
    """A test runner for the app's Click commands."""
    return flask_app.test_cli_runner()
