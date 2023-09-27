"""Tests for API endpoints related to studies"""
import json
import pytest

@pytest.fixture()
def study_id():
    """A study ID for testing."""
    return ""


def test_post_studies(test_client, study_id):
    """
    Given a Flask application configured for testing
    WHEN the '/study' endpoint is requested (POST)
    THEN check that the response is valid
    """

    # Crate a test using the Flask application configured for testing
    response = test_client.post(
        "/study",
        json={
            "title": "Study Title",
            "image": "https://api.dicebear.com/6.x/adventurer/svg",
        },
    )
    response_data = json.loads(response.data)

    assert response.status_code == 200
    assert response_data["title"] == "Study Title"
    assert response_data["image"] == "https://api.dicebear.com/6.x/adventurer/svg"
    study_id = response_data["id"]


def test_get_studies(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/study' endpoint is requested (GET)
    THEN check that the response is valid
    """

    response = test_client.get("/study")
    
    # Convert the response data from JSON to a Python dictionary
    response_data = json.loads(response.data)
    
    print(response_data)
    # Check the response is correct
    assert response.status_code == 200

def test_update_study(test_client):
    """
    GIVEN a study ID
    WHEN the '/study' endpoint is requested (PUT)
    THEN check that the study is updated
    """


def test_get_study_by_id(test_client):
    """
    GIVEN a study ID
    WHEN the '/study/{study_id}' endpoint is requested (GET)
    THEN check that the response is valid
    """

def test_delete_studies_created(test_client):
    """
    Given a Flask application configured for testing
    WHEN the '/study' endpoint is requested (DELETE)
    THEN check that the response is valid (200)
    THEN the '/study' endpoint is requested (GET)
    THEN check if the study created has been deleted
    """

    # TODO: DELETE ENDPOINT NOT WORKING
    # with flask_app.test_client() as test_client:
    #     response = test_client.post("/study", json={
