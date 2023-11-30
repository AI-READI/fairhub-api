"""Tests for API endpoints related to datasets"""
import json

import pytest


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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_id = response_data["id"]

    assert response_data["title"] == "Dataset Title"
    assert response_data["description"] == "Dataset Description"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset",
        json={
            "title": "Admin Dataset Title",
            "description": "Admin Dataset Description",
        },
    )

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_id_admin = admin_response_data["id"]
    assert admin_response_data["title"] == "Admin Dataset Title"
    assert admin_response_data["description"] == "Admin Dataset Description"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset",
        json={
            "title": "Editor Dataset Title",
            "description": "Editor Dataset Description",
        },
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_id_editor = editor_response_data["id"]

    assert editor_response_data["title"] == "Editor Dataset Title"
    assert editor_response_data["description"] == "Editor Dataset Description"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset",
        json={
            "title": "Viewer Dataset Title",
            "description": "Viewer Dataset Description",
        },
    )

    # response will be 403 due to Viewer permissions
    assert viewer_response.status_code == 403


def test_get_all_dataset_from_study(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/dataset/{study_id}' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the dataset content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/dataset")
    admin_response = _admin_client.get(f"/study/{study_id}/dataset")
    editor_response = _editor_client.get(f"/study/{study_id}/dataset")
    viewer_response = _viewer_client.get(f"/study/{study_id}/dataset")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # Three datasets should be returned
    assert len(response_data) == 3
    assert len(admin_response_data) == 3
    assert len(editor_response_data) == 3
    assert len(viewer_response_data) == 3

    assert response_data[0]["title"] == "Dataset Title"
    assert response_data[0]["description"] == "Dataset Description"
    assert response_data[1]["title"] == "Admin Dataset Title"
    assert response_data[1]["description"] == "Admin Dataset Description"
    assert response_data[2]["title"] == "Editor Dataset Title"
    assert response_data[2]["description"] == "Editor Dataset Description"

    assert admin_response_data[0]["title"] == "Dataset Title"
    assert admin_response_data[0]["description"] == "Dataset Description"
    assert admin_response_data[1]["title"] == "Admin Dataset Title"
    assert admin_response_data[1]["description"] == "Admin Dataset Description"
    assert admin_response_data[2]["title"] == "Editor Dataset Title"
    assert admin_response_data[2]["description"] == "Editor Dataset Description"

    assert editor_response_data[0]["title"] == "Dataset Title"
    assert editor_response_data[0]["description"] == "Dataset Description"
    assert editor_response_data[1]["title"] == "Admin Dataset Title"
    assert editor_response_data[1]["description"] == "Admin Dataset Description"
    assert editor_response_data[2]["title"] == "Editor Dataset Title"
    assert editor_response_data[2]["description"] == "Editor Dataset Description"

    assert viewer_response_data[0]["title"] == "Dataset Title"
    assert viewer_response_data[0]["description"] == "Dataset Description"
    assert viewer_response_data[1]["title"] == "Admin Dataset Title"
    assert viewer_response_data[1]["description"] == "Admin Dataset Description"
    assert viewer_response_data[2]["title"] == "Editor Dataset Title"
    assert viewer_response_data[2]["description"] == "Editor Dataset Description"


def test_get_dataset_from_study(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/dataset/{study_id}/{dataset_id}' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    admin_dataset_id = pytest.global_dataset_id_admin
    editor_dataset_id = pytest.global_dataset_id_editor

    response = _logged_in_client.get(f"/study/{study_id}/dataset/{dataset_id}")
    admin_response = _admin_client.get(f"/study/{study_id}/dataset/{dataset_id}")
    editor_response = _editor_client.get(f"/study/{study_id}/dataset/{dataset_id}")
    viewer_response = _viewer_client.get(f"/study/{study_id}/dataset/{dataset_id}")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["title"] == "Dataset Title"
    assert response_data["description"] == "Dataset Description"
    assert admin_response_data["title"] == "Dataset Title"
    assert admin_response_data["description"] == "Dataset Description"
    assert editor_response_data["title"] == "Dataset Title"
    assert editor_response_data["description"] == "Dataset Description"
    assert viewer_response_data["title"] == "Dataset Title"
    assert viewer_response_data["description"] == "Dataset Description"

    response = _logged_in_client.get(f"/study/{study_id}/dataset/{admin_dataset_id}")
    admin_response = _admin_client.get(f"/study/{study_id}/dataset/{admin_dataset_id}")
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{admin_dataset_id}"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{admin_dataset_id}"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["title"] == "Admin Dataset Title"
    assert response_data["description"] == "Admin Dataset Description"
    assert admin_response_data["title"] == "Admin Dataset Title"
    assert admin_response_data["description"] == "Admin Dataset Description"
    assert editor_response_data["title"] == "Admin Dataset Title"
    assert editor_response_data["description"] == "Admin Dataset Description"
    assert viewer_response_data["title"] == "Admin Dataset Title"
    assert viewer_response_data["description"] == "Admin Dataset Description"

    response = _logged_in_client.get(f"/study/{study_id}/dataset/{editor_dataset_id}")
    admin_response = _admin_client.get(f"/study/{study_id}/dataset/{editor_dataset_id}")
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{editor_dataset_id}"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{editor_dataset_id}"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["title"] == "Editor Dataset Title"
    assert response_data["description"] == "Editor Dataset Description"
    assert admin_response_data["title"] == "Editor Dataset Title"
    assert admin_response_data["description"] == "Editor Dataset Description"
    assert editor_response_data["title"] == "Editor Dataset Title"
    assert editor_response_data["description"] == "Editor Dataset Description"
    assert viewer_response_data["title"] == "Editor Dataset Title"
    assert viewer_response_data["description"] == "Editor Dataset Description"


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
    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset",
        json={
            "title": "Admin Delete Me",
            "description": "Dataset Description",
        },
    )
    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset",
        json={
            "title": "Editor Delete Me",
            "description": "Dataset Description",
        },
    )

    assert response.status_code == 201
    assert admin_response.status_code == 201
    assert editor_response.status_code == 201

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    dataset_id = response_data["id"]
    admin_dataset_id = admin_response_data["id"]
    editor_dataset_id = editor_response_data["id"]

    # delete temporary datasets
    viewer_response = _viewer_client.delete(f"/study/{study_id}/dataset/{dataset_id}")
    delete_response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}",
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{admin_dataset_id}",
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{editor_dataset_id}",
    )

    assert viewer_response.status_code == 403
    assert delete_response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204

    # delete original datasets created by admin and editor as they won't be used in other tests
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{pytest.global_dataset_id_admin}",
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{pytest.global_dataset_id_editor}",
    )

    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


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

    assert response.status_code == 201
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
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version",
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version",
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version",
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403
    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)

    assert len(response_data) == 1
    assert len(admin_response_data) == 1
    assert len(editor_response_data) == 1

    assert response_data[0]["title"] == "Dataset Version 1.0"
    assert response_data[0]["published"] is False
    assert response_data[0]["doi"] == "doi:test"
    assert response_data[0]["changelog"] == "changelog testing here"

    assert admin_response_data[0]["title"] == "Dataset Version 1.0"
    assert admin_response_data[0]["published"] is False
    assert admin_response_data[0]["doi"] == "doi:test"
    assert admin_response_data[0]["changelog"] == "changelog testing here"

    assert editor_response_data[0]["title"] == "Dataset Version 1.0"
    assert editor_response_data[0]["published"] is False
    assert editor_response_data[0]["doi"] == "doi:test"
    assert editor_response_data[0]["changelog"] == "changelog testing here"


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
