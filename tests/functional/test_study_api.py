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

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["title"] == "Study Title"
    assert response_data["image"] == "https://api.dicebear.com/6.x/adventurer/svg"
    pytest.global_study_id = response_data


def test_invite_study_contributor(_test_invite_study_contributor):
    """Invite contributors to study."""
    print("Contributors invited to study")


def test_create_admin_user(_create_admin_user):
    """Admin User created for permissions testing"""
    print("Admin user created for testing")


def test_create_editor_user(_create_editor_user):
    """Editor User created for permissions testing"""
    print("Editor user created for testing")


def test_viewer_editor_user(_create_viewer_user):
    """Viewer User created for permissions testing"""
    print("Viewer user created for testing")


def test_signin_all_clients(clients):
    """Signs in all clients for verifying permissions before testing continues."""
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    print("All clients signed in for testing")


def test_get_all_studies(clients):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/study' endpoint is requested (GET)
    THEN check that the response is valid
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    response = _logged_in_client.get("/study")

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert len(response_data) == 1  # Only one study created


def test_update_study(clients):
    """
    GIVEN a study ID
    WHEN the '/study' endpoint is requested (PUT)
    THEN check that the study is updated with the inputed data
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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
    print(response_data)
    pytest.global_study_id = response_data

    assert response_data["title"] == "Study Title Updated"
    assert response_data["image"] == pytest.global_study_id["image"]  # type: ignore
    assert response_data["id"] == pytest.global_study_id["id"]  # type: ignore


def test_get_study_by_id(clients):
    """
    GIVEN a study ID
    WHEN the '/study/{study_id}' endpoint is requested (GET)
    THEN check that the response is valid
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    response = _logged_in_client.get(f"/study/{pytest.global_study_id['id']}")  # type: ignore # pylint: disable=line-too-long # noqa: E501

    # Convert the response data from JSON to a Python dictionary
    assert response.status_code == 200
    response_data = json.loads(response.data)

    # Check the response is correct
    assert response_data["id"] == pytest.global_study_id["id"]  # type: ignore
    assert response_data["title"] == pytest.global_study_id["title"]  # type: ignore
    assert response_data["image"] == pytest.global_study_id["image"]  # type: ignore


def test_delete_studies_created(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/study/{study_id}' endpoint is requested (DELETE)
    THEN check that the response is valid (200)
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    # create study first to then delete
    response = _logged_in_client.post(
        "/study",
        json={
            "title": "Delete Me",
            "image": "https://api.dicebear.com/6.x/adventurer/svg",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    study_id = response_data["id"]

    viewer_response = _viewer_client.delete(f"/study/{study_id}")
    print(viewer_response.status_code)
    print(viewer_response.data)

    # delete study
    response = _logged_in_client.delete(f"/study/{study_id}")

    assert response.status_code == 200
