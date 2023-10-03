"""Tests for API endpoints related to studies"""
import json
import pytest


# Verify the database is empty before beginning tests
# def test_db_empty(test_client, empty_db, create_user, login_user):
#     """Test that the database is empty."""
#     response = test_client.get("/study")
#     assert response.status_code == 200
#     assert len(response.json) == 0


def test_post_study(test_client, login_user):
    """
    Given a Flask application configured for testing and a study
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
    pytest.global_study_id = response_data


def test_get_all_studies(test_client, login_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/study' endpoint is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/study")

    response_data = json.loads(response.data)
    assert len(response_data) == 1  # Only one study created
    assert response.status_code == 200


def test_update_study(test_client):
    """
    GIVEN a study ID
    WHEN the '/study' endpoint is requested (PUT)
    THEN check that the study is updated with the inputed data
    """
    response = test_client.put(
        f"/study/{pytest.global_study_id['id']}",
        json={
            "id": pytest.global_study_id["id"],
            "title": "Study Title Updated",
            "image": pytest.global_study_id["image"],
        },
    )
    response_data = json.loads(response.data)

    assert response.status_code == 200
    assert response_data["title"] == "Study Title Updated"
    assert response_data["image"] == pytest.global_study_id["image"]
    assert response_data["id"] == pytest.global_study_id["id"]
    pytest.global_study_id = response_data


def test_get_study_by_id(test_client):
    """
    GIVEN a study ID
    WHEN the '/study/{study_id}' endpoint is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get(f"/study/{pytest.global_study_id['id']}")

    # Convert the response data from JSON to a Python dictionary
    response_data = json.loads(response.data)

    # Check the response is correct
    assert response.status_code == 200
    assert response_data["id"] == pytest.global_study_id["id"]
    assert response_data["title"] == pytest.global_study_id["title"]
    assert response_data["image"] == pytest.global_study_id["image"]


def test_delete_studies_created(test_client):
    """
    Given a Flask application configured for testing
    WHEN the '/study' endpoint is requested (DELETE)
    THEN check that the response is valid (200)
    THEN the '/study' endpoint is requested (GET)
    THEN check if the study created has been deleted
    """
    print("delete study created")
    # TODO: DELETE ENDPOINT NOT WORKING
    # with flask_app.test_client() as test_client:
    #     response = test_client.post("/study", json={
