"""Tests for API endpoints related to datasets"""
import json

import pytest


def test_get_all_dataset_from_study(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/dataset/{study_id}' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the dataset content
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    response = _test_client.get(f"/study/{study_id}/dataset")
    response_data = json.loads(response.data)
    assert response.status_code == 200
    print(response_data)


def test_post_dataset(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/dataset/{study_id}' endpoint is requested (POST)
    THEN check that the response is valid and creates a dataset
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.post(
        f"/study/{study_id}/dataset",
        json={
            "title": "Dataset Title",
            "description": "Dataset Description",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_id = response_data["id"]
    print(pytest.global_dataset_id)


def test_get_dataset_from_study(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/dataset/{study_id}/{dataset_id}' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    response = _test_client.get(f"/study/{study_id}/dataset/{dataset_id}")
    response_data = json.loads(response.data)
    assert response.status_code == 200
    print(response_data)
