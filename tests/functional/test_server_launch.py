"""Tests for API endpoints related to server launch"""
import json


def test_server_launch(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/echo' endpoint is requested (GET)
    THEN check that the response shows that the server is active
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get("/echo")

    # Temporary test until we have authentication
    # assert response.status_code == 403

    # Convert the response data from JSON to a Python dictionary
    response_data = json.loads(response.data)

    # Check the response is correct
    assert response_data == "Server active!"
