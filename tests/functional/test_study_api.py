"""Tests for API endpoints related to studies"""
import json
import os

from app import create_app


def test_should_return_studies():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/study' endpoint is requested (GET)
    THEN check that the response is valid
    """

    # Set the environment to testing
    os.environ["FLASK_ENV"] = "testing"
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get("/study")

        # Convert the response data from JSON to a Python dictionary
        response_data = json.loads(response.data)

        # Check the response is correct
        assert response.status_code == 200
