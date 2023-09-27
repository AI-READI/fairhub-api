"""Defines fixtures available to all tests."""
import os
import pytest

from app import create_app


@pytest.fixture(scope="module")
def flask_app():
    """An application for the tests."""
    config = {
        "TESTING": True,
        "FAIRHUB_DATABASE_URL": "postgresql://admin:root@localhost:5432/fairhub_local",
    }

    # Set the environment to testing
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app(config)

    flask_app.config.update(
        {
            "TESTING": True,
            "FAIRHUB_DATABASE_URL": "postgresql://admin:root@localhost:5432/fairhub_local",
        }
    )

    yield flask_app
