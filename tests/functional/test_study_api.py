"""Tests for API endpoints related to studies"""
import json

import pytest


def test_post_study(_logged_in_client):
    """
    Given a Flask application configured for testing and a study
    WHEN the '/study' endpoint is requested (POST)
    THEN check that the response is valid
    """
    # Crate a test using the Flask application configured for testing
    response = _logged_in_client.post(
        "/study",
        json={
            "title": "Study Title",
            "image": "https://api.dicebear.com/6.x/adventurer/svg",
        },
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)

    assert response_data["title"] == "Study Title"
    assert response_data["image"] == "https://api.dicebear.com/6.x/adventurer/svg"
    pytest.global_study_id = response_data


def test_get_all_studies(_logged_in_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/study' endpoint is requested (GET)
    THEN check that the response is valid
    """
    response = _logged_in_client.get("/study")

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert len(response_data) == 1  # Only one study created


def test_update_study(_logged_in_client):
    """
    GIVEN a study ID
    WHEN the '/study' endpoint is requested (PUT)
    THEN check that the study is updated with the inputed data
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}",
        json={
            "title": "Study Title Updated",
            "image": pytest.global_study_id["image"],  # type: ignore
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_study_id = response_data

    assert response_data["title"] == "Study Title Updated"
    assert response_data["image"] == pytest.global_study_id["image"]  # type: ignore
    assert response_data["id"] == pytest.global_study_id["id"]  # type: ignore


def test_get_study_by_id(_logged_in_client):
    """
    GIVEN a study ID
    WHEN the '/study/{study_id}' endpoint is requested (GET)
    THEN check that the response is valid
    """
    response = _logged_in_client.get(f"/study/{pytest.global_study_id['id']}")  # type: ignore # pylint: disable=line-too-long # noqa: E501

    # Convert the response data from JSON to a Python dictionary
    assert response.status_code == 200
    response_data = json.loads(response.data)

    # Check the response is correct
    assert response_data["id"] == pytest.global_study_id["id"]  # type: ignore
    assert response_data["title"] == pytest.global_study_id["title"]  # type: ignore
    assert response_data["image"] == pytest.global_study_id["image"]  # type: ignore


def test_delete_studies_created(_logged_in_client):
    """
    Given a Flask application configured for testing
    WHEN the '/study/{study_id}' endpoint is requested (DELETE)
    THEN check that the response is valid (200)
    """
    # create study first to then delete
    response = _logged_in_client.post(
        "/study",
        json={
            "title": "Delete Me",
            "image": "https://api.dicebear.com/6.x/adventurer/svg",
        },
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    study_id = response_data["id"]

    # delete study
    response = _logged_in_client.delete(f"/study/{study_id}")

    assert response.status_code == 200
