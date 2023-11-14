"""Tests for API endpoints related to server launch"""
import json


def test_server_launch(_test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/echo' endpoint is requested (GET)
    THEN check that the response shows that the server is active
    """
    # Create a test client using the Flask application configured for testing
    response = _test_client.get("/echo")

    # Convert the response data from JSON to a Python dictionary
    response_data = json.loads(response.data)

    # Check the response is correct
    assert response_data == "Server active!"


# Empty database before testing and create a user for testing
def test_db_empty(_test_client, _empty_db, _create_user):
    """Test that the database is empty."""
    print("Database empty")
    print("User created for testing")


def test_signin_user(_logged_in_client):
    """Signs in user before testing."""
    print("User signed in for testing")
