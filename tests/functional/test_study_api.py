"""Tests for API endpoints related to studies"""
import json

import pytest

@pytest.fixture()
def study_id():
    return ""

def test_post_studies(flask_app):
    """
    Given a Flask application configured for testing
    WHEN the '/study' endpoint is requested (POST)
    THEN check that the response is valid
    """

    # Crate a test using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.post("/study", json={
            "title": "Study Title",
            "image": "https://api.dicebear.com/6.x/adventurer/svg",
        })
      
        assert response.status_code == 200

        response_data = json.loads(response.data)
        study_id = response_data["id"]
        print("response_data")
        print(study_id)
        print("response_data")

def test_get_all_studies(flask_app):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/study' endpoint is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get("/study")

        # Convert the response data from JSON to a Python dictionary
        response_data = json.loads(response.data)
        print(response_data)

        # Check the response is correct
        assert response.status_code == 200

def test_get_study_by_id(flask_app, test_post_studies, study_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/study/{study_id}' endpoint is requested (GET)
    THEN check that the response is valid
    """
        
      # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        print("test_get_study_by_id")
        print(study_id[0]['id'])
        print("test_get_study_by_id")
        response = test_client.get(f"/study/{study_id[0]['id']}")

        # Convert the response data from JSON to a Python dictionary
        response_data = json.loads(response.data)
        print(response_data)
        # Check the response is correct
        assert response.status_code == 200

def test_delete_studies_created(flask_app):
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
            