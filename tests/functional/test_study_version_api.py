# pylint: disable=too-many-lines
"""Tests for the Study Metadata API endpoints"""
import json

import pytest

# ------------------- VERSION ADD ------------------- #


def test_get_version_study_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing
    WHEN the /study/{study_id}/dataset/{dataset_id}/version/{version_id}/study-metadata endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_version_id  # type: ignore
    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/study-metadata"
    )

    assert response.status_code == 200


def test_get_version_dataset_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/dataset-metadata' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_version_id  # type: ignore

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/dataset-metadata"
    )

    assert response.status_code == 200


def test_get_version_readme(_logged_in_client):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/readme' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_version_id  # type: ignore

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme"
    )

    assert response.status_code == 200


def test_put_version_readme(_logged_in_client):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/readme' endpoint is requested (PUT)
    THEN check that the response is valid and retrieves the design metadata
    """
    # create a new dataset and delete it afterwards
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_version_id  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme",
        json={"readme": "readme test"},
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["readme"] == "readme test"


def test_put_version_changelog(_logged_in_client):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/changelog' endpoint is requested (PUT)
    THEN check that the response is valid and retrieves the design metadata
    """
    # create a new dataset and delete it afterwards
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_version_id  # type: ignore
    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog",
        json={"changelog": "changelog test"},
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data == "changelog test"


def test_get_version_changelog(_logged_in_client):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/changelog' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_version_id  # type: ignore

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog"
    )

    assert response.status_code == 200
