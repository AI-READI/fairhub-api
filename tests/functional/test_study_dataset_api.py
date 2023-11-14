"""Tests for API endpoints related to datasets"""
import json

import pytest


def test_get_all_dataset_from_study(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/dataset/{study_id}' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the dataset content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/dataset")

    assert response.status_code == 200
    # response_data = json.loads(response.data)
    # print(response_data)


def test_post_dataset(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/dataset/{study_id}' endpoint is requested (POST)
    THEN check that the response is valid and creates a dataset
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset",
        json={
            "title": "Dataset Title",
            "description": "Dataset Description",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_id = response_data["id"]


def test_get_dataset_from_study(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/dataset/{study_id}/{dataset_id}' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(f"/study/{study_id}/dataset/{dataset_id}")

    assert response.status_code == 200
    # response_data = json.loads(response.data)


def test_delete_dataset_from_study(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/dataset/{study_id}/{dataset_id}' endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    # create a new dataset and delete it afterwards
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset",
        json={
            "title": "Delete Me",
            "description": "Dataset Description",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    dataset_id = response_data["id"]

    # delete dataset
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}",
    )

    assert response.status_code == 200


def test_post_dataset_version(clients):
    """
    Given a Flask application configured for testing, study ID and a dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/version'
    endpoint is requested (POST)
    Then check that the response is valid and creates a dataset version
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/version",
        json={
            "title": "Dataset Version 1.0",
            "published": False,
            "doi": "doi:test",
            "changelog": "changelog testing here",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_version_id = response_data["id"]

    assert response_data["title"] == "Dataset Version 1.0"
    assert response_data["published"] is False
    assert response_data["doi"] == "doi:test"
    assert response_data["changelog"] == "changelog testing here"


def test_get_all_dataset_versions(clients):
    """
    Given a Flask application configured for testing, study ID and a dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/version' endpoint is requested (GET)
    Then check that the response is valid and retrieves all dataset versions
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version",
    )

    assert response.status_code == 200


def test_get_dataset_version(clients):
    """
    Given a Flask application configured for testing, study ID, dataset ID and version ID
    When the '/study/{study_id}/dataset/{dataset_id}/version/{version_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset version
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    version_id = pytest.global_dataset_version_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}",
    )

    assert response.status_code == 200


def test_put_dataset_version(clients):
    """
    Given a Flask application configured for testing, study ID, dataset ID and version ID
    When the '/study/{study_id}/dataset/{dataset_id}/version/{version_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset version
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    # study_id = pytest.global_study_id["id"]
    # dataset_id = pytest.global_dataset_id
    # version_id = pytest.global_dataset_version_id

    # response = _logged_in_client.put(
    #     f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}",
    #     json={}
    # )
    # WIP endpoint currently not implemented
