# pylint: disable=too-many-lines
"""Tests for the Dataset's Metadata API endpoints"""
import json
from time import sleep

import pytest


# ------------------- ACCESS METADATA ------------------- #
def test_put_dataset_access_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/access' endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset access metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access",
        json={
            "type": "type",
            "description": "description",
            "url": "google.com",
            "url_last_checked": 123,
        },
    )

    response_data = json.loads(response.data)
    assert response.status_code == 200

    assert response_data["type"] == "type"
    assert response_data["description"] == "description"
    assert response_data["url"] == "google.com"
    assert response_data["url_last_checked"] == 123

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access",
        json={
            "type": "admin type",
            "description": "admin description",
            "url": "google.com",
            "url_last_checked": 123,
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["type"] == "admin type"
    assert admin_response_data["description"] == "admin description"
    assert admin_response_data["url"] == "google.com"
    assert admin_response_data["url_last_checked"] == 123

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access",
        json={
            "type": "editor type",
            "description": "editor description",
            "url": "google.com",
            "url_last_checked": 123,
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["type"] == "editor type"
    assert editor_response_data["description"] == "editor description"
    assert editor_response_data["url"] == "google.com"
    assert editor_response_data["url_last_checked"] == 123

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access",
        json={
            "type": "viewer type",
            "description": "viewer description",
            "url": "google.com",
            "url_last_checked": 123,
        },
    )

    assert viewer_response.status_code == 403


def test_get_dataset_access_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/access' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset access metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # Since editor was the last successful PUT request, the response data should match
    assert response_data["type"] == "editor type"
    assert response_data["description"] == "editor description"
    assert response_data["url"] == "google.com"
    assert response_data["url_last_checked"] == 123

    assert admin_response_data["type"] == "editor type"
    assert admin_response_data["description"] == "editor description"
    assert admin_response_data["url"] == "google.com"
    assert admin_response_data["url_last_checked"] == 123

    assert editor_response_data["type"] == "editor type"
    assert editor_response_data["description"] == "editor description"
    assert editor_response_data["url"] == "google.com"
    assert editor_response_data["url_last_checked"] == 123

    assert viewer_response_data["type"] == "editor type"
    assert viewer_response_data["description"] == "editor description"
    assert viewer_response_data["url"] == "google.com"
    assert viewer_response_data["url_last_checked"] == 123


# ------------------- ALTERNATIVE IDENTIFIER METADATA ------------------- #
def test_post_alternative_identifier(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset alternative identifier
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "identifier test",
                "type": "ARK",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_alternative_identifier_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "identifier test"
    assert response_data[0]["type"] == "ARK"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "admin test",
                "type": "ARK",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)
    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "editor test",
                "type": "ARK",
            }
        ],
    )
    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "viewer test",
                "type": "ARK",
            }
        ],
    )

    assert admin_response.status_code == 201
    assert editor_response.status_code == 201
    assert viewer_response.status_code == 403

    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    pytest.global_alternative_identifier_id_admin = admin_response_data[0]["id"]
    pytest.global_alternative_identifier_id_editor = editor_response_data[0]["id"]

    assert admin_response_data[0]["identifier"] == "admin test"
    assert admin_response_data[0]["type"] == "ARK"
    assert editor_response_data[0]["identifier"] == "editor test"
    assert editor_response_data[0]["type"] == "ARK"


def test_get_alternative_identifier(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset alternative identifier content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["identifier"] == "identifier test"
    assert response_data[0]["type"] == "ARK"
    assert response_data[1]["identifier"] == "admin test"
    assert response_data[1]["type"] == "ARK"
    assert response_data[2]["identifier"] == "editor test"
    assert response_data[2]["type"] == "ARK"

    assert admin_response_data[0]["identifier"] == "identifier test"
    assert admin_response_data[0]["type"] == "ARK"
    assert admin_response_data[1]["identifier"] == "admin test"
    assert admin_response_data[1]["type"] == "ARK"
    assert admin_response_data[2]["identifier"] == "editor test"
    assert admin_response_data[2]["type"] == "ARK"

    assert editor_response_data[0]["identifier"] == "identifier test"
    assert editor_response_data[0]["type"] == "ARK"
    assert editor_response_data[1]["identifier"] == "admin test"
    assert editor_response_data[1]["type"] == "ARK"
    assert editor_response_data[2]["identifier"] == "editor test"
    assert editor_response_data[2]["type"] == "ARK"

    assert viewer_response_data[0]["identifier"] == "identifier test"
    assert viewer_response_data[0]["type"] == "ARK"
    assert viewer_response_data[1]["identifier"] == "admin test"
    assert viewer_response_data[1]["type"] == "ARK"
    assert viewer_response_data[2]["identifier"] == "editor test"
    assert viewer_response_data[2]["type"] == "ARK"


def test_delete_alternative_identifier(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset alternative identifier content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    identifier_id = pytest.global_alternative_identifier_id
    admin_identifier_id = pytest.global_alternative_identifier_id_admin
    editor_identifier_id = pytest.global_alternative_identifier_id_editor

    # verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{identifier_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{identifier_id}"
    )
    # pylint: disable=line-too-long
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{admin_identifier_id}"
    )
    # pylint: disable=line-too-long
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{editor_identifier_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- CONSENT METADATA ------------------- #
def test_put_dataset_consent_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/consent' endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset consent metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/consent",
        json={
            "type": "test",
            "noncommercial": True,
            "geog_restrict": True,
            "research_type": True,
            "genetic_only": True,
            "no_methods": True,
            "details": "test",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["type"] == "test"
    assert response_data["noncommercial"] is True
    assert response_data["geog_restrict"] is True
    assert response_data["research_type"] is True
    assert response_data["genetic_only"] is True
    assert response_data["no_methods"] is True
    assert response_data["details"] == "test"

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/consent",
        json={
            "type": "admin test",
            "noncommercial": True,
            "geog_restrict": True,
            "research_type": True,
            "genetic_only": True,
            "no_methods": True,
            "details": "admin details test",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["type"] == "admin test"
    assert admin_response_data["details"] == "admin details test"

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/consent",
        json={
            "type": "editor test",
            "noncommercial": True,
            "geog_restrict": True,
            "research_type": True,
            "genetic_only": True,
            "no_methods": True,
            "details": "editor details test",
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["type"] == "editor test"
    assert editor_response_data["details"] == "editor details test"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/consent",
        json={
            "type": "viewer test",
            "noncommercial": True,
            "geog_restrict": True,
            "research_type": True,
            "genetic_only": True,
            "no_methods": True,
            "details": "viewer details test",
        },
    )

    assert viewer_response.status_code == 403


def test_get_dataset_consent_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/consent' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset consent metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/consent"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/consent"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/consent"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/consent"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # Editor was the last successful PUT request, so the response data should match
    assert response_data["type"] == "editor test"
    assert response_data["noncommercial"] is True
    assert response_data["geog_restrict"] is True
    assert response_data["research_type"] is True
    assert response_data["genetic_only"] is True
    assert response_data["no_methods"] is True
    assert response_data["details"] == "editor details test"

    assert admin_response_data["type"] == "editor test"
    assert admin_response_data["noncommercial"] is True
    assert admin_response_data["geog_restrict"] is True
    assert admin_response_data["research_type"] is True
    assert admin_response_data["genetic_only"] is True
    assert admin_response_data["no_methods"] is True
    assert admin_response_data["details"] == "editor details test"

    assert editor_response_data["type"] == "editor test"
    assert editor_response_data["noncommercial"] is True
    assert editor_response_data["geog_restrict"] is True
    assert editor_response_data["research_type"] is True
    assert editor_response_data["genetic_only"] is True
    assert editor_response_data["no_methods"] is True
    assert editor_response_data["details"] == "editor details test"

    assert viewer_response_data["type"] == "editor test"
    assert viewer_response_data["noncommercial"] is True
    assert viewer_response_data["geog_restrict"] is True
    assert viewer_response_data["research_type"] is True
    assert viewer_response_data["genetic_only"] is True
    assert viewer_response_data["no_methods"] is True
    assert viewer_response_data["details"] == "editor details test"


# ------------------- CONTRIBUTOR METADATA ------------------- #
def test_post_dataset_contributor_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/contributor'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset contributor metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor",
        json=[
            {
                "given_name": "Given Name here",
                "family_name": "Family Name here",
                "name_type": "Personal",
                "name_identifier": "Name identifier",
                "name_identifier_scheme": "Name Scheme ID",
                "name_identifier_scheme_uri": "Name ID Scheme URI",
                "contributor_type": "Con Type",
                "affiliations": [
                    {
                        "name": "Test",
                        "identifier": "yes",
                        "scheme": "uh",
                        "scheme_uri": "scheme uri",
                    }
                ],
            }
        ],
    )

    # Add a one second delay to prevent duplicate timestamps
    sleep(1)
    response_data = json.loads(response.data)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_contributor_id = response_data[0]["id"]

    assert response_data[0]["given_name"] == "Given Name here"
    assert response_data[0]["family_name"] == "Family Name here"
    assert response_data[0]["name_type"] == "Personal"
    assert response_data[0]["name_identifier"] == "Name identifier"
    assert response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert response_data[0]["creator"] is False
    assert response_data[0]["contributor_type"] == "Con Type"
    assert response_data[0]["affiliations"][0]["name"] == "Test"
    assert response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor",
        json=[
            {
                "given_name": "Admin Given Name here",
                "family_name": "Family Name here",
                "name_type": "Personal",
                "name_identifier": "Name identifier",
                "name_identifier_scheme": "Name Scheme ID",
                "name_identifier_scheme_uri": "Name ID Scheme URI",
                "contributor_type": "Con Type",
                "affiliations": [
                    {
                        "name": "Test",
                        "identifier": "yes",
                        "scheme": "uh",
                        "scheme_uri": "scheme uri",
                    }
                ],
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_contributor_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["given_name"] == "Admin Given Name here"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor",
        json=[
            {
                "given_name": "Editor Given Name here",
                "family_name": "Editor Family Name here",
                "name_type": "Personal",
                "name_identifier": "Name identifier",
                "name_identifier_scheme": "Name Scheme ID",
                "name_identifier_scheme_uri": "Name ID Scheme URI",
                "contributor_type": "Con Type",
                "affiliations": [
                    {
                        "name": "Test",
                        "identifier": "yes",
                        "scheme": "uh",
                        "scheme_uri": "scheme uri",
                    }
                ],
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_contributor_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["given_name"] == "Editor Given Name here"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor",
        json=[
            {
                "given_name": "Viewer Given Name here",
                "family_name": "Viewer Family Name here",
                "name_type": "Personal",
                "name_identifier": "Name identifier",
                "name_identifier_scheme": "Name Scheme ID",
                "name_identifier_scheme_uri": "Name ID Scheme URI",
                "contributor_type": "Con Type",
                "affiliations": [
                    {
                        "name": "Test",
                        "identifier": "yes",
                        "scheme": "uh",
                        "scheme_uri": "scheme uri",
                    }
                ],
            }
        ],
    )
    assert viewer_response.status_code == 403


def test_get_dataset_contributor_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/contributor'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset contributor metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


def test_delete_dataset_contributor_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/contributor'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset contributor metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    contributor_id = pytest.global_dataset_contributor_id
    admin_contributor_id = pytest.global_dataset_contributor_id_admin
    editor_contributor_id = pytest.global_dataset_contributor_id_editor

    # Verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor/{contributor_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor/{contributor_id}"
    )
    # pylint: disable=line-too-long
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor/{admin_contributor_id}"
    )
    # pylint: disable=line-too-long
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor/{editor_contributor_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- CREATOR METADATA ------------------- #
def test_post_dataset_creator_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/creator' endpoint is requested (POST)
    Then check that the response is valid and creates the dataset creator metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator",
        json=[
            {
                "given_name": "Given Name here",
                "family_name": "Family Name here",
                "name_type": "Personal",
                "name_identifier": "Name identifier",
                "name_identifier_scheme": "Name Scheme ID",
                "name_identifier_scheme_uri": "Name ID Scheme URI",
                "affiliations": [
                    {
                        "name": "Test",
                        "identifier": "yes",
                        "scheme": "uh",
                        "scheme_uri": "scheme uri",
                    }
                ],
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_creator_id = response_data[0]["id"]

    assert response_data[0]["given_name"] == "Given Name here"
    assert response_data[0]["family_name"] == "Family Name here"
    assert response_data[0]["name_type"] == "Personal"
    assert response_data[0]["name_identifier"] == "Name identifier"
    assert response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert response_data[0]["creator"] is True
    assert response_data[0]["affiliations"][0]["name"] == "Test"
    assert response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator",
        json=[
            {
                "given_name": "Admin Given Name here",
                "family_name": "Family Name here",
                "name_type": "Personal",
                "name_identifier": "Name identifier",
                "name_identifier_scheme": "Name Scheme ID",
                "name_identifier_scheme_uri": "Name ID Scheme URI",
                "affiliations": [
                    {
                        "name": "Test",
                        "identifier": "yes",
                        "scheme": "uh",
                        "scheme_uri": "scheme uri",
                    }
                ],
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_creator_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["given_name"] == "Admin Given Name here"
    assert admin_response_data[0]["family_name"] == "Family Name here"
    assert admin_response_data[0]["name_type"] == "Personal"
    assert admin_response_data[0]["name_identifier"] == "Name identifier"
    assert admin_response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_response_data[0]["creator"] is True
    assert admin_response_data[0]["affiliations"][0]["name"] == "Test"
    assert admin_response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert admin_response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert admin_response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator",
        json=[
            {
                "given_name": "Editor Given Name here",
                "family_name": "Family Name here",
                "name_type": "Personal",
                "name_identifier": "Name identifier",
                "name_identifier_scheme": "Name Scheme ID",
                "name_identifier_scheme_uri": "Name ID Scheme URI",
                "affiliations": [
                    {
                        "name": "Test",
                        "identifier": "yes",
                        "scheme": "uh",
                        "scheme_uri": "scheme uri",
                    }
                ],
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_creator_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["given_name"] == "Editor Given Name here"
    assert editor_response_data[0]["family_name"] == "Family Name here"
    assert editor_response_data[0]["name_type"] == "Personal"
    assert editor_response_data[0]["name_identifier"] == "Name identifier"
    assert editor_response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_response_data[0]["creator"] is True
    assert editor_response_data[0]["affiliations"][0]["name"] == "Test"
    assert editor_response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert editor_response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert editor_response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator",
        json=[
            {
                "given_name": "Viewer Given Name here",
                "family_name": "Family Name here",
                "name_type": "Personal",
                "name_identifier": "Name identifier",
                "name_identifier_scheme": "Name Scheme ID",
                "name_identifier_scheme_uri": "Name ID Scheme URI",
                "affiliations": [
                    {
                        "name": "Test",
                        "identifier": "yes",
                        "scheme": "uh",
                        "scheme_uri": "scheme uri",
                    }
                ],
            }
        ],
    )

    assert viewer_response.status_code == 403


def test_get_dataset_creator_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/creator' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset creator metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert len(response_data) == 3
    assert len(admin_response_data) == 3
    assert len(editor_response_data) == 3
    assert len(viewer_response_data) == 3

    assert response_data[0]["id"] == pytest.global_dataset_creator_id
    assert response_data[0]["given_name"] == "Given Name here"
    assert response_data[0]["family_name"] == "Family Name here"
    assert response_data[0]["name_type"] == "Personal"
    assert response_data[0]["name_identifier"] == "Name identifier"
    assert response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert response_data[0]["creator"] is True
    assert response_data[0]["affiliations"][0]["name"] == "Test"
    assert response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert response_data[1]["id"] == pytest.global_dataset_creator_id_admin
    assert response_data[1]["given_name"] == "Admin Given Name here"
    assert response_data[1]["family_name"] == "Family Name here"
    assert response_data[1]["name_type"] == "Personal"
    assert response_data[1]["name_identifier"] == "Name identifier"
    assert response_data[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert response_data[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert response_data[1]["creator"] is True
    assert response_data[1]["affiliations"][0]["name"] == "Test"
    assert response_data[1]["affiliations"][0]["identifier"] == "yes"
    assert response_data[1]["affiliations"][0]["scheme"] == "uh"
    assert response_data[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert response_data[2]["id"] == pytest.global_dataset_creator_id_editor
    assert response_data[2]["given_name"] == "Editor Given Name here"
    assert response_data[2]["family_name"] == "Family Name here"
    assert response_data[2]["name_type"] == "Personal"
    assert response_data[2]["name_identifier"] == "Name identifier"
    assert response_data[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert response_data[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert response_data[2]["creator"] is True
    assert response_data[2]["affiliations"][0]["name"] == "Test"
    assert response_data[2]["affiliations"][0]["identifier"] == "yes"
    assert response_data[2]["affiliations"][0]["scheme"] == "uh"
    assert response_data[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert admin_response_data[0]["given_name"] == "Given Name here"
    assert admin_response_data[0]["family_name"] == "Family Name here"
    assert admin_response_data[0]["name_type"] == "Personal"
    assert admin_response_data[0]["name_identifier"] == "Name identifier"
    assert admin_response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_response_data[0]["creator"] is True
    assert admin_response_data[0]["affiliations"][0]["name"] == "Test"
    assert admin_response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert admin_response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert admin_response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert admin_response_data[1]["given_name"] == "Admin Given Name here"
    assert admin_response_data[1]["family_name"] == "Family Name here"
    assert admin_response_data[1]["name_type"] == "Personal"
    assert admin_response_data[1]["name_identifier"] == "Name identifier"
    assert admin_response_data[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_response_data[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_response_data[1]["creator"] is True
    assert admin_response_data[1]["affiliations"][0]["name"] == "Test"
    assert admin_response_data[1]["affiliations"][0]["identifier"] == "yes"
    assert admin_response_data[1]["affiliations"][0]["scheme"] == "uh"
    assert admin_response_data[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert admin_response_data[2]["given_name"] == "Editor Given Name here"
    assert admin_response_data[2]["family_name"] == "Family Name here"
    assert admin_response_data[2]["name_type"] == "Personal"
    assert admin_response_data[2]["name_identifier"] == "Name identifier"
    assert admin_response_data[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_response_data[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_response_data[2]["creator"] is True
    assert admin_response_data[2]["affiliations"][0]["name"] == "Test"
    assert admin_response_data[2]["affiliations"][0]["identifier"] == "yes"
    assert admin_response_data[2]["affiliations"][0]["scheme"] == "uh"
    assert admin_response_data[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert editor_response_data[0]["given_name"] == "Given Name here"
    assert editor_response_data[0]["family_name"] == "Family Name here"
    assert editor_response_data[0]["name_type"] == "Personal"
    assert editor_response_data[0]["name_identifier"] == "Name identifier"
    assert editor_response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_response_data[0]["creator"] is True
    assert editor_response_data[0]["affiliations"][0]["name"] == "Test"
    assert editor_response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert editor_response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert editor_response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert editor_response_data[1]["given_name"] == "Admin Given Name here"
    assert editor_response_data[1]["family_name"] == "Family Name here"
    assert editor_response_data[1]["name_type"] == "Personal"
    assert editor_response_data[1]["name_identifier"] == "Name identifier"
    assert editor_response_data[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_response_data[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_response_data[1]["creator"] is True
    assert editor_response_data[1]["affiliations"][0]["name"] == "Test"
    assert editor_response_data[1]["affiliations"][0]["identifier"] == "yes"
    assert editor_response_data[1]["affiliations"][0]["scheme"] == "uh"
    assert editor_response_data[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert editor_response_data[2]["given_name"] == "Editor Given Name here"
    assert editor_response_data[2]["family_name"] == "Family Name here"
    assert editor_response_data[2]["name_type"] == "Personal"
    assert editor_response_data[2]["name_identifier"] == "Name identifier"
    assert editor_response_data[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_response_data[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_response_data[2]["creator"] is True
    assert editor_response_data[2]["affiliations"][0]["name"] == "Test"
    assert editor_response_data[2]["affiliations"][0]["identifier"] == "yes"
    assert editor_response_data[2]["affiliations"][0]["scheme"] == "uh"
    assert editor_response_data[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert viewer_response_data[0]["given_name"] == "Given Name here"
    assert viewer_response_data[0]["family_name"] == "Family Name here"
    assert viewer_response_data[0]["name_type"] == "Personal"
    assert viewer_response_data[0]["name_identifier"] == "Name identifier"
    assert viewer_response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert viewer_response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert viewer_response_data[0]["creator"] is True
    assert viewer_response_data[0]["affiliations"][0]["name"] == "Test"
    assert viewer_response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert viewer_response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert viewer_response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[1]["given_name"] == "Admin Given Name here"
    assert viewer_response_data[1]["family_name"] == "Family Name here"
    assert viewer_response_data[1]["name_type"] == "Personal"
    assert viewer_response_data[1]["name_identifier"] == "Name identifier"
    assert viewer_response_data[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert viewer_response_data[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert viewer_response_data[1]["creator"] is True
    assert viewer_response_data[1]["affiliations"][0]["name"] == "Test"
    assert viewer_response_data[1]["affiliations"][0]["identifier"] == "yes"
    assert viewer_response_data[1]["affiliations"][0]["scheme"] == "uh"
    assert viewer_response_data[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[2]["given_name"] == "Editor Given Name here"
    assert viewer_response_data[2]["family_name"] == "Family Name here"
    assert viewer_response_data[2]["name_type"] == "Personal"
    assert viewer_response_data[2]["name_identifier"] == "Name identifier"
    assert viewer_response_data[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert viewer_response_data[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert viewer_response_data[2]["creator"] is True
    assert viewer_response_data[2]["affiliations"][0]["name"] == "Test"
    assert viewer_response_data[2]["affiliations"][0]["identifier"] == "yes"
    assert viewer_response_data[2]["affiliations"][0]["scheme"] == "uh"
    assert viewer_response_data[2]["affiliations"][0]["scheme_uri"] == "scheme uri"


def test_delete_dataset_creator_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/creator'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset creator metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    creator_id = pytest.global_dataset_creator_id
    admin_creator_id = pytest.global_dataset_creator_id_admin
    editor_creator_id = pytest.global_dataset_creator_id_editor

    # Verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{creator_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{creator_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{admin_creator_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{editor_creator_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DATE METADATA ------------------- #
def test_post_dataset_date_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/date'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset date metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date",
        json=[{"date": 20210101, "type": "Type", "information": "Info"}],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_date_id = response_data[0]["id"]

    assert response_data[0]["date"] == 20210101
    assert response_data[0]["type"] == "Type"
    assert response_data[0]["information"] == "Info"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date",
        json=[{"date": 20210102, "type": "Type", "information": "Info"}],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_date_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["date"] == 20210102
    assert admin_response_data[0]["type"] == "Type"
    assert admin_response_data[0]["information"] == "Info"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date",
        json=[{"date": 20210103, "type": "Type", "information": "Info"}],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_date_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["date"] == 20210103
    assert editor_response_data[0]["type"] == "Type"
    assert editor_response_data[0]["information"] == "Info"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date",
        json=[{"date": 20210101, "type": "Type", "information": "Info"}],
    )

    assert viewer_response.status_code == 403


def test_get_dataset_date_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/date'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset date metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert len(response_data) == 3
    assert len(admin_response_data) == 3
    assert len(editor_response_data) == 3
    assert len(viewer_response_data) == 3

    assert response_data[0]["date"] == 20210101
    assert response_data[0]["type"] == "Type"
    assert response_data[0]["information"] == "Info"
    assert response_data[1]["date"] == 20210102
    assert response_data[1]["type"] == "Type"
    assert response_data[1]["information"] == "Info"
    assert response_data[2]["date"] == 20210103
    assert response_data[2]["type"] == "Type"

    assert admin_response_data[0]["date"] == 20210101
    assert admin_response_data[0]["type"] == "Type"
    assert admin_response_data[0]["information"] == "Info"
    assert admin_response_data[1]["date"] == 20210102
    assert admin_response_data[1]["type"] == "Type"
    assert admin_response_data[1]["information"] == "Info"
    assert admin_response_data[2]["date"] == 20210103
    assert admin_response_data[2]["type"] == "Type"

    assert editor_response_data[0]["date"] == 20210101
    assert editor_response_data[0]["type"] == "Type"
    assert editor_response_data[0]["information"] == "Info"
    assert editor_response_data[1]["date"] == 20210102
    assert editor_response_data[1]["type"] == "Type"
    assert editor_response_data[1]["information"] == "Info"
    assert editor_response_data[2]["date"] == 20210103
    assert editor_response_data[2]["type"] == "Type"

    assert viewer_response_data[0]["date"] == 20210101
    assert viewer_response_data[0]["type"] == "Type"
    assert viewer_response_data[0]["information"] == "Info"
    assert viewer_response_data[1]["date"] == 20210102
    assert viewer_response_data[1]["type"] == "Type"
    assert viewer_response_data[1]["information"] == "Info"
    assert viewer_response_data[2]["date"] == 20210103
    assert viewer_response_data[2]["type"] == "Type"


def test_delete_dataset_date_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/date'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset date metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    date_id = pytest.global_dataset_date_id
    admin_date_id = pytest.global_dataset_date_id_admin
    editor_date_id = pytest.global_dataset_date_id_editor

    # Verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{date_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{date_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{admin_date_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{editor_date_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DE-IDENTIFICATION LEVEL METADATA ------------------- #
def test_put_dataset_deidentification_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/de-identification'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    de-identification metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/de-identification-level",
        json={
            "type": "Level",
            "direct": True,
            "hipaa": True,
            "dates": True,
            "nonarr": True,
            "k_anon": True,
            "details": "Details",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["type"] == "Level"
    assert response_data["direct"] is True
    assert response_data["hipaa"] is True
    assert response_data["dates"] is True
    assert response_data["nonarr"] is True
    assert response_data["k_anon"] is True
    assert response_data["details"] == "Details"

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/de-identification-level",
        json={
            "type": "Level",
            "direct": True,
            "hipaa": True,
            "dates": True,
            "nonarr": True,
            "k_anon": True,
            "details": "Details",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["type"] == "Level"
    assert admin_response_data["direct"] is True
    assert admin_response_data["hipaa"] is True
    assert admin_response_data["dates"] is True
    assert admin_response_data["nonarr"] is True
    assert admin_response_data["k_anon"] is True
    assert admin_response_data["details"] == "Details"

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/de-identification-level",
        json={
            "type": "Level",
            "direct": True,
            "hipaa": True,
            "dates": True,
            "nonarr": True,
            "k_anon": True,
            "details": "Details",
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["type"] == "Level"
    assert editor_response_data["direct"] is True
    assert editor_response_data["hipaa"] is True
    assert editor_response_data["dates"] is True
    assert editor_response_data["nonarr"] is True
    assert editor_response_data["k_anon"] is True
    assert editor_response_data["details"] == "Details"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/de-identification-level",
        json={
            "type": "Level",
            "direct": True,
            "hipaa": True,
            "dates": True,
            "nonarr": True,
            "k_anon": True,
            "details": "Details",
        },
    )

    assert viewer_response.status_code == 403


def test_get_dataset_deidentification_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/de-identification'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    de-identification metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/de-identification-level"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/de-identification-level"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/de-identification-level"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/de-identification-level"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["type"] == "Level"
    assert response_data["direct"] is True
    assert response_data["hipaa"] is True
    assert response_data["dates"] is True
    assert response_data["nonarr"] is True
    assert response_data["k_anon"] is True
    assert response_data["details"] == "Details"

    assert admin_response_data["type"] == "Level"
    assert admin_response_data["direct"] is True
    assert admin_response_data["hipaa"] is True
    assert admin_response_data["dates"] is True
    assert admin_response_data["nonarr"] is True
    assert admin_response_data["k_anon"] is True
    assert admin_response_data["details"] == "Details"

    assert editor_response_data["type"] == "Level"
    assert editor_response_data["direct"] is True
    assert editor_response_data["hipaa"] is True
    assert editor_response_data["dates"] is True
    assert editor_response_data["nonarr"] is True
    assert editor_response_data["k_anon"] is True
    assert editor_response_data["details"] == "Details"

    assert viewer_response_data["type"] == "Level"
    assert viewer_response_data["direct"] is True
    assert viewer_response_data["hipaa"] is True
    assert viewer_response_data["dates"] is True
    assert viewer_response_data["nonarr"] is True
    assert viewer_response_data["k_anon"] is True
    assert viewer_response_data["details"] == "Details"


# ------------------- DESCRIPTION METADATA ------------------- #
def test_post_dataset_descriptions_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/description'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description",
        json=[{"description": "Owner Description", "type": "Methods"}],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_description_id = response_data[0]["id"]

    assert response_data[0]["description"] == "Owner Description"
    assert response_data[0]["type"] == "Methods"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description",
        json=[{"description": "Admin Description", "type": "Methods"}],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_description_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["description"] == "Admin Description"
    assert admin_response_data[0]["type"] == "Methods"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description",
        json=[{"description": "Editor Description", "type": "Methods"}],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_description_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["description"] == "Editor Description"
    assert editor_response_data[0]["type"] == "Methods"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description",
        json=[{"description": "Viewer Description", "type": "Methods"}],
    )

    assert viewer_response.status_code == 403


def test_get_dataset_descriptions_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/description'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # Dataset description is included in the responses
    assert len(response_data) == 4
    assert len(admin_response_data) == 4
    assert len(editor_response_data) == 4
    assert len(viewer_response_data) == 4

    # seacrch for type abstract index
    main_descrip = next(
        (index for (index, d) in enumerate(response_data) if d["type"] == "Abstract"),
        None,
    )
    a_main_descrip = next(
        (
            index
            for (index, d) in enumerate(admin_response_data)
            if d["type"] == "Abstract"
        ),
        None,
    )
    e_main_descrip = next(
        (
            index
            for (index, d) in enumerate(editor_response_data)
            if d["type"] == "Abstract"
        ),
        None,
    )
    v_main_descrip = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data)
            if d["type"] == "Abstract"
        ),
        None,
    )

    # search for owner description
    # pylint: disable=line-too-long
    own_descrip = next(
        (
            index
            for (index, d) in enumerate(response_data)
            if d["description"] == "Owner Description"
        ),
        None,
    )
    a_own_descrip = next(
        (
            index
            for (index, d) in enumerate(admin_response_data)
            if d["description"] == "Owner Description"
        ),
        None,
    )
    e_own_descrip = next(
        (
            index
            for (index, d) in enumerate(editor_response_data)
            if d["description"] == "Owner Description"
        ),
        None,
    )
    v_own_descrip = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data)
            if d["description"] == "Owner Description"
        ),
        None,
    )

    # search for admin description
    admin_descrip = next(
        (
            index
            for (index, d) in enumerate(response_data)
            if d["description"] == "Admin Description"
        ),
        None,
    )
    a_admin_descrip = next(
        (
            index
            for (index, d) in enumerate(admin_response_data)
            if d["description"] == "Admin Description"
        ),
        None,
    )
    e_admin_descrip = next(
        (
            index
            for (index, d) in enumerate(editor_response_data)
            if d["description"] == "Admin Description"
        ),
        None,
    )
    v_admin_descrip = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data)
            if d["description"] == "Admin Description"
        ),
        None,
    )

    # search for editor description
    edit_descrip = next(
        (
            index
            for (index, d) in enumerate(response_data)
            if d["description"] == "Editor Description"
        ),
        None,
    )
    a_edit_descrip = next(
        (
            index
            for (index, d) in enumerate(admin_response_data)
            if d["description"] == "Editor Description"
        ),
        None,
    )
    e_edit_descrip = next(
        (
            index
            for (index, d) in enumerate(editor_response_data)
            if d["description"] == "Editor Description"
        ),
        None,
    )
    v_edit_descrip = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data)
            if d["description"] == "Editor Description"
        ),
        None,
    )

    assert response_data[main_descrip]["description"] == "Dataset Description"
    assert response_data[main_descrip]["type"] == "Abstract"
    assert response_data[own_descrip]["description"] == "Owner Description"
    assert response_data[own_descrip]["type"] == "Methods"
    assert response_data[admin_descrip]["description"] == "Admin Description"
    assert response_data[admin_descrip]["type"] == "Methods"
    assert response_data[edit_descrip]["description"] == "Editor Description"
    assert response_data[edit_descrip]["type"] == "Methods"

    assert admin_response_data[a_main_descrip]["description"] == "Dataset Description"
    assert admin_response_data[a_main_descrip]["type"] == "Abstract"
    assert admin_response_data[a_own_descrip]["description"] == "Owner Description"
    assert admin_response_data[a_own_descrip]["type"] == "Methods"
    assert admin_response_data[a_admin_descrip]["description"] == "Admin Description"
    assert admin_response_data[a_admin_descrip]["type"] == "Methods"
    assert admin_response_data[a_edit_descrip]["description"] == "Editor Description"
    assert admin_response_data[a_edit_descrip]["type"] == "Methods"

    assert editor_response_data[e_main_descrip]["description"] == "Dataset Description"
    assert editor_response_data[e_main_descrip]["type"] == "Abstract"
    assert editor_response_data[e_own_descrip]["description"] == "Owner Description"
    assert editor_response_data[e_own_descrip]["type"] == "Methods"
    assert editor_response_data[e_admin_descrip]["description"] == "Admin Description"
    assert editor_response_data[e_admin_descrip]["type"] == "Methods"
    assert editor_response_data[e_edit_descrip]["description"] == "Editor Description"
    assert editor_response_data[e_edit_descrip]["type"] == "Methods"

    assert viewer_response_data[v_main_descrip]["description"] == "Dataset Description"
    assert viewer_response_data[v_main_descrip]["type"] == "Abstract"
    assert viewer_response_data[v_own_descrip]["description"] == "Owner Description"
    assert viewer_response_data[v_own_descrip]["type"] == "Methods"
    assert viewer_response_data[v_admin_descrip]["description"] == "Admin Description"
    assert viewer_response_data[v_admin_descrip]["type"] == "Methods"
    assert viewer_response_data[v_edit_descrip]["description"] == "Editor Description"
    assert viewer_response_data[v_edit_descrip]["type"] == "Methods"


def test_delete_dataset_description_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/description'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    description_id = pytest.global_dataset_description_id
    admin_description_id = pytest.global_dataset_description_id_admin
    editor_description_id = pytest.global_dataset_description_id_editor

    # Verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{description_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{description_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{admin_description_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{editor_description_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DATASET HEALTHSHEET MOTIVATION METADATA ------------------- #
def test_put_healthsheet_motivation_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation",
        json={"motivation": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["motivation"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation",
        json={"motivation": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation",
        json={"motivation": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation",
        json={"motivation": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_motivation_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["motivation"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# # ------------------- DATASET HEALTHSHEET COMPOSITION METADATA ------------------- #
def test_put_healthsheet_composition_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/composition'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet composition metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition",
        json={"composition": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["composition"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition",
        json={"composition": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition",
        json={"composition": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition",
        json={"composition": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_composition_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/composition'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["composition"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# ------------------- DATASET HEALTHSHEET COLLECTION METADATA ------------------- #
def test_put_healthsheet_collection_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/collection'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet collection metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection",
        json={"collection": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["collection"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection",
        json={"collection": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection",
        json={"collection": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection",
        json={"collection": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_collection_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/collection'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["collection"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# ------------------- DATASET HEALTHSHEET PREPROCESSING METADATA ------------------- #
def test_put_healthsheet_preprocessing_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet preprocessing metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing",
        json={"preprocessing": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["preprocessing"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing",
        json={"preprocessing": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing",
        json={"preprocessing": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing",
        json={"preprocessing": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_preprocessing_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["preprocessing"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# # ------------------- DATASET HEALTHSHEET USES METADATA ------------------- #
def test_put_healthsheet_uses_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/uses'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet uses metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses",
        json={"uses": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses",
        json={"uses": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert admin_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses",
        json={"uses": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses",
        json={"uses": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_uses_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/uses'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert admin_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# ------------------- DATASET HEALTHSHEET DISTRIBUTION METADATA ------------------- #
def test_put_healthsheet_distribution_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/distribution'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet distribution metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution",
        json={"distribution": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["distribution"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution",
        json={"distribution": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution",
        json={"distribution": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution",
        json={"distribution": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_distribution_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    distribution metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["distribution"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# ------------------- DATASET HEALTHSHEET MAINTENANCE METADATA ------------------- #
def test_put_healthsheet_maintenance_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/maintenance'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet maintenance metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance",
        json={"maintenance": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["maintenance"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance",
        json={"maintenance": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance",
        json={"maintenance": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance",
        json={"maintenance": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_maintenance_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    maintenance metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["maintenance"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# ------------------- DATASET FUNDER METADATA ------------------- #
def test_post_dataset_funder_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/funder'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    funder metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder",
        json=[
            {
                "name": "Name",
                "award_number": "award number",
                "award_title": "Award Title",
                "award_uri": "Award URI",
                "identifier": "Identifier",
                "identifier_scheme_uri": "Identifier Scheme URI",
                "identifier_type": "Identifier Type",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_funder_id = response_data[0]["id"]

    assert response_data[0]["name"] == "Name"
    assert response_data[0]["award_number"] == "award number"
    assert response_data[0]["award_title"] == "Award Title"
    assert response_data[0]["award_uri"] == "Award URI"
    assert response_data[0]["identifier"] == "Identifier"
    assert response_data[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert response_data[0]["identifier_type"] == "Identifier Type"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder",
        json=[
            {
                "name": "Admin Name",
                "award_number": "award number",
                "award_title": "Award Title",
                "award_uri": "Award URI",
                "identifier": "Identifier",
                "identifier_scheme_uri": "Identifier Scheme URI",
                "identifier_type": "Identifier Type",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_funder_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["name"] == "Admin Name"
    assert admin_response_data[0]["award_number"] == "award number"
    assert admin_response_data[0]["award_title"] == "Award Title"
    assert admin_response_data[0]["award_uri"] == "Award URI"
    assert admin_response_data[0]["identifier"] == "Identifier"
    assert admin_response_data[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert admin_response_data[0]["identifier_type"] == "Identifier Type"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder",
        json=[
            {
                "name": "Editor Name",
                "award_number": "award number",
                "award_title": "Award Title",
                "award_uri": "Award URI",
                "identifier": "Identifier",
                "identifier_scheme_uri": "Identifier Scheme URI",
                "identifier_type": "Identifier Type",
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_funder_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["name"] == "Editor Name"
    assert editor_response_data[0]["award_number"] == "award number"
    assert editor_response_data[0]["award_title"] == "Award Title"
    assert editor_response_data[0]["award_uri"] == "Award URI"
    assert editor_response_data[0]["identifier"] == "Identifier"
    assert (
        editor_response_data[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    )  # pylint: disable=line-too-long
    assert editor_response_data[0]["identifier_type"] == "Identifier Type"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder",
        json=[
            {
                "name": "Viewer Name",
                "award_number": "award number",
                "award_title": "Award Title",
                "award_uri": "Award URI",
                "identifier": "Identifier",
                "identifier_scheme_uri": "Identifier Scheme URI",
                "identifier_type": "Identifier Type",
            }
        ],
    )

    assert viewer_response.status_code == 403


def test_get_dataset_funder_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/funder'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    funder metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert len(response_data) == 3
    assert len(admin_response_data) == 3
    assert len(editor_response_data) == 3
    assert len(viewer_response_data) == 3

    assert response_data[0]["name"] == "Name"
    assert response_data[0]["award_number"] == "award number"
    assert response_data[0]["award_title"] == "Award Title"
    assert response_data[0]["award_uri"] == "Award URI"
    assert response_data[0]["identifier"] == "Identifier"
    assert response_data[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert response_data[0]["identifier_type"] == "Identifier Type"
    assert response_data[1]["name"] == "Admin Name"
    assert response_data[1]["award_number"] == "award number"
    assert response_data[1]["award_title"] == "Award Title"
    assert response_data[1]["award_uri"] == "Award URI"
    assert response_data[1]["identifier"] == "Identifier"
    assert response_data[1]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert response_data[1]["identifier_type"] == "Identifier Type"
    assert response_data[2]["name"] == "Editor Name"
    assert response_data[2]["award_number"] == "award number"
    assert response_data[2]["award_title"] == "Award Title"
    assert response_data[2]["award_uri"] == "Award URI"
    assert response_data[2]["identifier"] == "Identifier"
    assert response_data[2]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert response_data[2]["identifier_type"] == "Identifier Type"

    assert admin_response_data[0]["name"] == "Name"
    assert admin_response_data[0]["award_number"] == "award number"
    assert admin_response_data[0]["award_title"] == "Award Title"
    assert admin_response_data[0]["award_uri"] == "Award URI"
    assert admin_response_data[0]["identifier"] == "Identifier"
    assert admin_response_data[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert admin_response_data[0]["identifier_type"] == "Identifier Type"
    assert admin_response_data[1]["name"] == "Admin Name"
    assert admin_response_data[1]["award_number"] == "award number"
    assert admin_response_data[1]["award_title"] == "Award Title"
    assert admin_response_data[1]["award_uri"] == "Award URI"
    assert admin_response_data[1]["identifier"] == "Identifier"
    assert admin_response_data[1]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert admin_response_data[1]["identifier_type"] == "Identifier Type"
    assert admin_response_data[2]["name"] == "Editor Name"
    assert admin_response_data[2]["award_number"] == "award number"
    assert admin_response_data[2]["award_title"] == "Award Title"
    assert admin_response_data[2]["award_uri"] == "Award URI"
    assert admin_response_data[2]["identifier"] == "Identifier"
    assert admin_response_data[2]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert admin_response_data[2]["identifier_type"] == "Identifier Type"

    assert editor_response_data[0]["name"] == "Name"
    assert editor_response_data[0]["award_number"] == "award number"
    assert editor_response_data[0]["award_title"] == "Award Title"
    assert editor_response_data[0]["award_uri"] == "Award URI"
    assert editor_response_data[0]["identifier"] == "Identifier"
    assert editor_response_data[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert editor_response_data[0]["identifier_type"] == "Identifier Type"
    assert editor_response_data[1]["name"] == "Admin Name"
    assert editor_response_data[1]["award_number"] == "award number"
    assert editor_response_data[1]["award_title"] == "Award Title"
    assert editor_response_data[1]["award_uri"] == "Award URI"
    assert editor_response_data[1]["identifier"] == "Identifier"
    assert editor_response_data[1]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert editor_response_data[1]["identifier_type"] == "Identifier Type"
    assert editor_response_data[2]["name"] == "Editor Name"
    assert editor_response_data[2]["award_number"] == "award number"
    assert editor_response_data[2]["award_title"] == "Award Title"
    assert editor_response_data[2]["award_uri"] == "Award URI"
    assert editor_response_data[2]["identifier"] == "Identifier"
    assert editor_response_data[2]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert editor_response_data[2]["identifier_type"] == "Identifier Type"

    assert viewer_response_data[0]["name"] == "Name"
    assert viewer_response_data[0]["award_number"] == "award number"
    assert viewer_response_data[0]["award_title"] == "Award Title"
    assert viewer_response_data[0]["award_uri"] == "Award URI"
    assert viewer_response_data[0]["identifier"] == "Identifier"
    assert viewer_response_data[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert viewer_response_data[0]["identifier_type"] == "Identifier Type"
    assert viewer_response_data[1]["name"] == "Admin Name"
    assert viewer_response_data[1]["award_number"] == "award number"
    assert viewer_response_data[1]["award_title"] == "Award Title"
    assert viewer_response_data[1]["award_uri"] == "Award URI"
    assert viewer_response_data[1]["identifier"] == "Identifier"
    assert viewer_response_data[1]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert viewer_response_data[1]["identifier_type"] == "Identifier Type"
    assert viewer_response_data[2]["name"] == "Editor Name"
    assert viewer_response_data[2]["award_number"] == "award number"
    assert viewer_response_data[2]["award_title"] == "Award Title"
    assert viewer_response_data[2]["award_uri"] == "Award URI"
    assert viewer_response_data[2]["identifier"] == "Identifier"
    assert viewer_response_data[2]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert viewer_response_data[2]["identifier_type"] == "Identifier Type"


def test_delete_dataset_funder_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/funder'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    funder metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    funder_id = pytest.global_dataset_funder_id
    a_funder_id = pytest.global_dataset_funder_id_admin
    e_funder_id = pytest.global_dataset_funder_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{funder_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{funder_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{a_funder_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{e_funder_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- OTHER METADATA ------------------- #
def test_put_other_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    other metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other",
        json={
            "acknowledgement": "Yes",
            "language": "English",
            "resource_type": "Resource Type",
            "size": ["Size"],
            "standards_followed": "Standards Followed",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["acknowledgement"] == "Yes"
    assert response_data["language"] == "English"
    # assert (
    #     response_data["resource_type"] == "Resource Type"
    # )  # CURRENTLY NOT BEING RETURNED
    assert response_data["size"] == ["Size"]
    assert response_data["standards_followed"] == "Standards Followed"

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other",
        json={
            "acknowledgement": "Yes",
            "language": "English",
            "resource_type": "Admin Resource Type",
            "size": ["Size"],
            "standards_followed": "Standards Followed",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["acknowledgement"] == "Yes"
    assert admin_response_data["language"] == "English"
    # assert admin_response_data["resource_type"] == "Admin Resource Type"
    assert admin_response_data["size"] == ["Size"]
    assert admin_response_data["standards_followed"] == "Standards Followed"

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other",
        json={
            "acknowledgement": "Yes",
            "language": "English",
            "resource_type": "Editor Resource Type",
            "size": ["Size"],
            "standards_followed": "Standards Followed",
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["acknowledgement"] == "Yes"
    assert editor_response_data["language"] == "English"
    # assert editor_response_data["resource_type"] == "Editor Resource Type"
    assert editor_response_data["size"] == ["Size"]
    assert editor_response_data["standards_followed"] == "Standards Followed"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other",
        json={
            "acknowledgement": "Yes",
            "language": "English",
            "resource_type": "Viewer Resource Type",
            "size": ["Size"],
            "standards_followed": "Standards Followed",
        },
    )

    assert viewer_response.status_code == 403


def test_get_other_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    other metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # Editor was the last to update the metadata successfully so
    # the response should reflect that
    assert response_data["acknowledgement"] == "Yes"
    assert response_data["language"] == "English"
    # assert response_data["resource_type"] == "Editor Resource Type"
    assert response_data["size"] == ["Size"]
    assert response_data["standards_followed"] == "Standards Followed"

    assert admin_response_data["acknowledgement"] == "Yes"
    assert admin_response_data["language"] == "English"
    # assert admin_response_data["resource_type"] == "Editor Resource Type"
    assert admin_response_data["size"] == ["Size"]
    assert admin_response_data["standards_followed"] == "Standards Followed"

    assert editor_response_data["acknowledgement"] == "Yes"
    assert editor_response_data["language"] == "English"
    # assert editor_response_data["resource_type"] == "Editor Resource Type"
    assert editor_response_data["size"] == ["Size"]
    assert editor_response_data["standards_followed"] == "Standards Followed"

    assert viewer_response_data["acknowledgement"] == "Yes"
    assert viewer_response_data["language"] == "English"
    # assert viewer_response_data["resource_type"] == "Editor Resource Type"
    assert viewer_response_data["size"] == ["Size"]
    assert viewer_response_data["standards_followed"] == "Standards Followed"


# ------------------- PUBLICATION METADATA ------------------- #
def test_put_dataset_publisher_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    publisher metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/publisher",
        json={
            "publisher": "Publisher",
            "managing_organization_name": "Managing Organization Name",
            "managing_organization_ror_id": "Managing Organization ROR ID",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["publisher"] == "Publisher"
    assert response_data["managing_organization_name"] == "Managing Organization Name"
    assert (
        response_data["managing_organization_ror_id"] == "Managing Organization ROR ID"
    )

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/publisher",
        json={
            "publisher": "Publisher",
            "managing_organization_name": "Managing Admin Organization Name",
            "managing_organization_ror_id": "Managing Organization ROR ID",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["publisher"] == "Publisher"
    assert (
        admin_response_data["managing_organization_name"]
        == "Managing Admin Organization Name"
    )
    assert (
        admin_response_data["managing_organization_ror_id"]
        == "Managing Organization ROR ID"
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/publisher",
        json={
            "publisher": "Publisher",
            "managing_organization_name": "Managing Editor Organization Name",
            "managing_organization_ror_id": "Managing Organization ROR ID",
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["publisher"] == "Publisher"
    assert (
        editor_response_data["managing_organization_name"]
        == "Managing Editor Organization Name"
    )
    assert (
        editor_response_data["managing_organization_ror_id"]
        == "Managing Organization ROR ID"
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/publisher",
        json={
            "publisher": "Publisher",
            "managing_organization_name": "Managing Viewer Organization Name",
            "managing_organization_ror_id": "Managing Organization ROR ID",
        },
    )

    assert viewer_response.status_code == 403


def test_get_dataset_publisher_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    publisher metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/publisher"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/publisher"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/publisher"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/publisher"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # Editor was the last to update the metadata successfully so
    # the response should reflect that
    assert response_data["publisher"] == "Publisher"
    assert (
        response_data["managing_organization_name"]
        == "Managing Editor Organization Name"
    )
    assert (
        response_data["managing_organization_ror_id"] == "Managing Organization ROR ID"
    )

    assert admin_response_data["publisher"] == "Publisher"
    assert (
        admin_response_data["managing_organization_name"]
        == "Managing Editor Organization Name"
    )
    assert (
        admin_response_data["managing_organization_ror_id"]
        == "Managing Organization ROR ID"
    )

    assert editor_response_data["publisher"] == "Publisher"
    assert (
        editor_response_data["managing_organization_name"]
        == "Managing Editor Organization Name"
    )
    assert (
        editor_response_data["managing_organization_ror_id"]
        == "Managing Organization ROR ID"
    )

    assert viewer_response_data["publisher"] == "Publisher"
    assert (
        viewer_response_data["managing_organization_name"]
        == "Managing Editor Organization Name"
    )
    assert (
        viewer_response_data["managing_organization_ror_id"]
        == "Managing Organization ROR ID"
    )


# ------------------- RELATED IDENTIFIER METADATA ------------------- #
def test_post_dataset_related_identifier_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    related identifier metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier",
        json=[
            {
                "identifier": "test identifier",
                "identifier_type": "test identifier type",
                "relation_type": "test relation type",
                "related_metadata_scheme": "test",
                "scheme_uri": "test",
                "scheme_type": "test",
                "resource_type": "test"
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)

    pytest.global_dataset_related_identifier_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "test identifier"
    assert response_data[0]["identifier_type"] == "test identifier type"
    assert response_data[0]["relation_type"] == "test relation type"
    assert response_data[0]["related_metadata_scheme"] == "test"
    assert response_data[0]["scheme_uri"] == "test"
    assert response_data[0]["scheme_type"] == "test"
    assert response_data[0]["resource_type"] == "test"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier",
        json=[
            {
                "identifier": "admin test identifier",
                "identifier_type": "test identifier type",
                "relation_type": "test relation type",
                "related_metadata_scheme": "test",
                "scheme_uri": "test",
                "scheme_type": "test",
                "resource_type": "test"
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_related_identifier_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["identifier"] == "admin test identifier"
    assert admin_response_data[0]["identifier_type"] == "test identifier type"
    assert admin_response_data[0]["relation_type"] == "test relation type"
    assert admin_response_data[0]["related_metadata_scheme"] == "test"
    assert admin_response_data[0]["scheme_uri"] == "test"
    assert admin_response_data[0]["scheme_type"] == "test"
    assert admin_response_data[0]["resource_type"] == "test"
    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier",
        json=[
            {
                "identifier": "editor test identifier",
                "identifier_type": "test identifier type",
                "relation_type": "test relation type",
                "related_metadata_scheme": "test",
                "scheme_uri": "test",
                "scheme_type": "test",
                "resource_type": "test"
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_related_identifier_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["identifier"] == "editor test identifier"
    assert editor_response_data[0]["identifier_type"] == "test identifier type"
    assert editor_response_data[0]["relation_type"] == "test relation type"
    assert editor_response_data[0]["related_metadata_scheme"] == "test"
    assert editor_response_data[0]["scheme_uri"] == "test"
    assert editor_response_data[0]["scheme_type"] == "test"
    assert editor_response_data[0]["resource_type"] == "test"
    viewer_client = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier",
        json=[
            {
                "identifier": "viewer test identifier",
                "identifier_type": "test identifier type",
                "relation_type": "test relation type",
                "related_metadata_scheme": "test",
                "scheme_uri": "test",
                "scheme_type": "test",
                "resource_type": "test"
            }
        ],
    )

    assert viewer_client.status_code == 403


def test_get_dataset_related_identifier_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    related identifier metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # seach for main title and subtitle index in response_data[n]["titles"]
    # pylint: disable=line-too-long

    # assert len(response_data) == 3
    # assert len(admin_response_data) == 3
    # assert len(editor_response_data) == 3
    # assert len(viewer_response_data) == 3
    print(len(response_data), "lennnnnnnnnn")
    assert response_data[0]["identifier"] == "test identifier"
    assert response_data[0]["identifier_type"] == "test identifier type"
    assert response_data[0]["relation_type"] == "test relation type"
    assert response_data[0]["related_metadata_scheme"] == "test"
    assert response_data[0]["scheme_uri"] == "test"
    assert response_data[0]["scheme_type"] == "test"
    assert response_data[0]["resource_type"] == "test"
    assert response_data[1]["identifier"] == "admin test identifier"
    assert response_data[1]["identifier_type"] == "test identifier type"
    assert response_data[1]["relation_type"] == "test relation type"
    assert response_data[1]["related_metadata_scheme"] == "test"
    assert response_data[1]["scheme_uri"] == "test"
    assert response_data[1]["scheme_type"] == "test"
    assert response_data[1]["resource_type"] == "test"
    assert response_data[2]["identifier"] == "editor test identifier"
    assert response_data[2]["identifier_type"] == "test identifier type"
    assert response_data[2]["relation_type"] == "test relation type"
    assert response_data[2]["related_metadata_scheme"] == "test"
    assert response_data[2]["scheme_uri"] == "test"
    assert response_data[2]["scheme_type"] == "test"
    assert response_data[2]["resource_type"] == "test"

    assert admin_response_data[0]["identifier"] == "test identifier"
    assert admin_response_data[0]["identifier_type"] == "test identifier type"
    assert admin_response_data[0]["relation_type"] == "test relation type"
    assert admin_response_data[0]["related_metadata_scheme"] == "test"
    assert admin_response_data[0]["scheme_uri"] == "test"
    assert admin_response_data[0]["scheme_type"] == "test"
    assert admin_response_data[0]["resource_type"] == "test"
    assert admin_response_data[1]["identifier"] == "admin test identifier"
    assert admin_response_data[1]["identifier_type"] == "test identifier type"
    assert admin_response_data[1]["relation_type"] == "test relation type"
    assert admin_response_data[1]["related_metadata_scheme"] == "test"
    assert admin_response_data[1]["scheme_uri"] == "test"
    assert admin_response_data[1]["scheme_type"] == "test"
    assert admin_response_data[1]["resource_type"] == "test"
    assert admin_response_data[2]["identifier"] == "editor test identifier"
    assert admin_response_data[2]["identifier_type"] == "test identifier type"
    assert admin_response_data[2]["relation_type"] == "test relation type"
    assert admin_response_data[2]["related_metadata_scheme"] == "test"
    assert admin_response_data[2]["scheme_uri"] == "test"
    assert admin_response_data[2]["scheme_type"] == "test"
    assert admin_response_data[2]["resource_type"] == "test"

    assert editor_response_data[0]["identifier"] == "test identifier"
    assert editor_response_data[0]["identifier_type"] == "test identifier type"
    assert editor_response_data[0]["relation_type"] == "test relation type"
    assert editor_response_data[0]["related_metadata_scheme"] == "test"
    assert editor_response_data[0]["scheme_uri"] == "test"
    assert editor_response_data[0]["scheme_type"] == "test"
    assert editor_response_data[0]["resource_type"] == "test"
    assert editor_response_data[1]["identifier"] == "admin test identifier"
    assert editor_response_data[1]["identifier_type"] == "test identifier type"
    assert editor_response_data[1]["relation_type"] == "test relation type"
    assert editor_response_data[1]["related_metadata_scheme"] == "test"
    assert editor_response_data[1]["scheme_uri"] == "test"
    assert editor_response_data[1]["scheme_type"] == "test"
    assert editor_response_data[1]["resource_type"] == "test"
    assert editor_response_data[2]["identifier"] == "editor test identifier"
    assert editor_response_data[2]["identifier_type"] == "test identifier type"
    assert editor_response_data[2]["relation_type"] == "test relation type"
    assert editor_response_data[2]["related_metadata_scheme"] == "test"
    assert editor_response_data[2]["scheme_uri"] == "test"
    assert editor_response_data[2]["scheme_type"] == "test"
    assert editor_response_data[2]["resource_type"] == "test"

    assert viewer_response_data[0]["identifier"] == "test identifier"
    assert viewer_response_data[0]["identifier_type"] == "test identifier type"
    assert viewer_response_data[0]["relation_type"] == "test relation type"
    assert viewer_response_data[0]["related_metadata_scheme"] == "test"
    assert viewer_response_data[0]["scheme_uri"] == "test"
    assert viewer_response_data[0]["scheme_type"] == "test"
    assert viewer_response_data[0]["resource_type"] == "test"
    assert viewer_response_data[1]["identifier"] == "admin test identifier"
    assert viewer_response_data[1]["identifier_type"] == "test identifier type"
    assert viewer_response_data[1]["relation_type"] == "test relation type"
    assert viewer_response_data[1]["related_metadata_scheme"] == "test"
    assert viewer_response_data[1]["scheme_uri"] == "test"
    assert viewer_response_data[1]["scheme_type"] == "test"
    assert viewer_response_data[1]["resource_type"] == "test"
    assert viewer_response_data[2]["identifier"] == "editor test identifier"
    assert viewer_response_data[2]["identifier_type"] == "test identifier type"
    assert viewer_response_data[2]["relation_type"] == "test relation type"
    assert viewer_response_data[2]["related_metadata_scheme"] == "test"
    assert viewer_response_data[2]["scheme_uri"] == "test"
    assert viewer_response_data[2]["scheme_type"] == "test"
    assert viewer_response_data[2]["resource_type"] == "test"


def test_delete_dataset_related_identifier_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and retrieves the dataset
    related identifier metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    identifier_id = pytest.global_dataset_related_identifier_id
    a_identifier_id = pytest.global_dataset_related_identifier_id_admin
    e_identifier_id = pytest.global_dataset_related_identifier_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier/{identifier_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier/{identifier_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier/{a_identifier_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier/{e_identifier_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- RIGHTS METADATA ------------------- #
def test_post_dataset_rights_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    rights metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights",
        json=[
            {
                "identifier": "Identifier",
                "identifier_scheme": "Identifier Scheme",
                "rights": "Rights",
                "uri": "URI",
                "license_text": "license text",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_rights_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "Identifier"
    assert response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert response_data[0]["rights"] == "Rights"
    assert response_data[0]["uri"] == "URI"
    assert response_data[0]["license_text"] == "license text"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights",
        json=[
            {
                "identifier": "Admin Identifier",
                "identifier_scheme": "Admin Identifier Scheme",
                "rights": "Admin Rights",
                "uri": "Admin URI",
                "license_text": "license text",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_rights_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["identifier"] == "Admin Identifier"
    assert admin_response_data[0]["identifier_scheme"] == "Admin Identifier Scheme"
    assert admin_response_data[0]["rights"] == "Admin Rights"
    assert admin_response_data[0]["uri"] == "Admin URI"
    assert admin_response_data[0]["license_text"] == "license text"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights",
        json=[
            {
                "identifier": "Editor Identifier",
                "identifier_scheme": "Editor Identifier Scheme",
                "rights": "Editor Rights",
                "uri": "Editor URI",
                "license_text": "license text",
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_rights_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["identifier"] == "Editor Identifier"
    assert editor_response_data[0]["identifier_scheme"] == "Editor Identifier Scheme"
    assert editor_response_data[0]["rights"] == "Editor Rights"
    assert editor_response_data[0]["uri"] == "Editor URI"
    assert editor_response_data[0]["license_text"] == "license text"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights",
        json=[
            {
                "identifier": "Viewer Identifier",
                "identifier_scheme": "Viewer Identifier Scheme",
                "rights": "Viewer Rights",
                "uri": "Viewer URI",
                "license_text": "license text",
            }
        ],
    )

    assert viewer_response.status_code == 403


def test_get_dataset_rights_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    rights metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["identifier"] == "Identifier"
    assert response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert response_data[0]["rights"] == "Rights"
    assert response_data[0]["uri"] == "URI"
    assert response_data[0]["license_text"] == "license text"
    assert response_data[1]["identifier"] == "Admin Identifier"
    assert response_data[1]["identifier_scheme"] == "Admin Identifier Scheme"
    assert response_data[1]["rights"] == "Admin Rights"
    assert response_data[1]["uri"] == "Admin URI"
    assert response_data[1]["license_text"] == "license text"
    assert response_data[2]["identifier"] == "Editor Identifier"
    assert response_data[2]["identifier_scheme"] == "Editor Identifier Scheme"
    assert response_data[2]["rights"] == "Editor Rights"
    assert response_data[2]["uri"] == "Editor URI"
    assert response_data[2]["license_text"] == "license text"

    assert admin_response_data[0]["identifier"] == "Identifier"
    assert admin_response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert admin_response_data[0]["rights"] == "Rights"
    assert admin_response_data[0]["uri"] == "URI"
    assert admin_response_data[0]["license_text"] == "license text"
    assert admin_response_data[1]["identifier"] == "Admin Identifier"
    assert admin_response_data[1]["identifier_scheme"] == "Admin Identifier Scheme"
    assert admin_response_data[1]["rights"] == "Admin Rights"
    assert admin_response_data[1]["uri"] == "Admin URI"
    assert admin_response_data[1]["license_text"] == "license text"
    assert admin_response_data[2]["identifier"] == "Editor Identifier"
    assert admin_response_data[2]["identifier_scheme"] == "Editor Identifier Scheme"
    assert admin_response_data[2]["rights"] == "Editor Rights"
    assert admin_response_data[2]["uri"] == "Editor URI"
    assert admin_response_data[2]["license_text"] == "license text"

    assert editor_response_data[0]["identifier"] == "Identifier"
    assert editor_response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert editor_response_data[0]["rights"] == "Rights"
    assert editor_response_data[0]["uri"] == "URI"
    assert editor_response_data[0]["license_text"] == "license text"
    assert editor_response_data[1]["identifier"] == "Admin Identifier"
    assert editor_response_data[1]["identifier_scheme"] == "Admin Identifier Scheme"
    assert editor_response_data[1]["rights"] == "Admin Rights"
    assert editor_response_data[1]["uri"] == "Admin URI"
    assert editor_response_data[1]["license_text"] == "license text"
    assert editor_response_data[2]["identifier"] == "Editor Identifier"
    assert editor_response_data[2]["identifier_scheme"] == "Editor Identifier Scheme"
    assert editor_response_data[2]["rights"] == "Editor Rights"
    assert editor_response_data[2]["uri"] == "Editor URI"
    assert editor_response_data[2]["license_text"] == "license text"

    assert viewer_response_data[0]["identifier"] == "Identifier"
    assert viewer_response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert viewer_response_data[0]["rights"] == "Rights"
    assert viewer_response_data[0]["uri"] == "URI"
    assert viewer_response_data[0]["license_text"] == "license text"
    assert viewer_response_data[1]["identifier"] == "Admin Identifier"
    assert viewer_response_data[1]["identifier_scheme"] == "Admin Identifier Scheme"
    assert viewer_response_data[1]["rights"] == "Admin Rights"
    assert viewer_response_data[1]["uri"] == "Admin URI"
    assert viewer_response_data[1]["license_text"] == "license text"
    assert viewer_response_data[2]["identifier"] == "Editor Identifier"
    assert viewer_response_data[2]["identifier_scheme"] == "Editor Identifier Scheme"
    assert viewer_response_data[2]["rights"] == "Editor Rights"
    assert viewer_response_data[2]["uri"] == "Editor URI"
    assert viewer_response_data[2]["license_text"] == "license text"


def test_delete_dataset_rights_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/rights'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    rights metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    rights_id = pytest.global_dataset_rights_id
    a_rights_id = pytest.global_dataset_rights_id_admin
    e_rights_id = pytest.global_dataset_rights_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights/{rights_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights/{rights_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights/{a_rights_id}"
    )
    editor_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights/{e_rights_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- SUBJECTS METADATA ------------------- #
def test_post_dataset_subjects_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/subject'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    subjects metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject",
        json=[
            {
                "classification_code": "Classification Code",
                "scheme": "Scheme",
                "scheme_uri": "Scheme URI",
                "subject": "Subject",
                "value_uri": "Value URI",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_subject_id = response_data[0]["id"]

    assert response_data[0]["scheme"] == "Scheme"
    assert response_data[0]["scheme_uri"] == "Scheme URI"
    assert response_data[0]["subject"] == "Subject"
    assert response_data[0]["value_uri"] == "Value URI"
    assert response_data[0]["classification_code"] == "Classification Code"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject",
        json=[
            {
                "classification_code": "Classification Code",
                "scheme": "Admin Scheme",
                "scheme_uri": "Scheme URI",
                "subject": "Subject",
                "value_uri": "Admin Value URI",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_subject_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["scheme"] == "Admin Scheme"
    assert admin_response_data[0]["scheme_uri"] == "Scheme URI"
    assert admin_response_data[0]["subject"] == "Subject"
    assert admin_response_data[0]["value_uri"] == "Admin Value URI"
    assert admin_response_data[0]["classification_code"] == "Classification Code"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject",
        json=[
            {
                "classification_code": "Classification Code",
                "scheme": "Editor Scheme",
                "scheme_uri": "Scheme URI",
                "subject": "Subject",
                "value_uri": "Editor Value URI",
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_subject_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["scheme"] == "Editor Scheme"
    assert editor_response_data[0]["scheme_uri"] == "Scheme URI"
    assert editor_response_data[0]["subject"] == "Subject"
    assert editor_response_data[0]["value_uri"] == "Editor Value URI"
    assert editor_response_data[0]["classification_code"] == "Classification Code"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject",
        json=[
            {
                "classification_code": "Classification Code",
                "scheme": "Viewer Scheme",
                "scheme_uri": "Scheme URI",
                "subject": "Subject",
                "value_uri": "Viewer Value URI",
            }
        ],
    )

    assert viewer_response.status_code == 403


def test_get_dataset_subjects_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/subject'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    subjects metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject"
    )

    assert response.status_code == 200


def test_delete_dataset_subject_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/subject'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    subjects metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    subject_id = pytest.global_dataset_subject_id
    admin_sub_id = pytest.global_dataset_subject_id_admin
    editor_sub_id = pytest.global_dataset_subject_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject/{subject_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject/{subject_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject/{admin_sub_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject/{editor_sub_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- TITLE METADATA ------------------- #
def test_post_dataset_title_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/title'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    title metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title",
        json=[{"title": "Owner Title", "type": "Subtitle"}],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_title_id = response_data[0]["id"]

    assert response_data[0]["title"] == "Owner Title"
    assert response_data[0]["type"] == "Subtitle"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title",
        json=[{"title": "Admin Title", "type": "Subtitle"}],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_title_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["title"] == "Admin Title"
    assert admin_response_data[0]["type"] == "Subtitle"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title",
        json=[{"title": "Editor Title", "type": "Subtitle"}],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_title_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["title"] == "Editor Title"
    assert editor_response_data[0]["type"] == "Subtitle"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title",
        json=[{"title": "Viewer Title", "type": "Subtitle"}],
    )

    assert viewer_response.status_code == 403


def test_get_dataset_title_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/title'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    title metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert len(response_data) == 4
    assert len(admin_response_data) == 4
    assert len(editor_response_data) == 4
    assert len(viewer_response_data) == 4

    # search for maintitle index
    # pylint: disable=line-too-long
    main_title = next(
        (index for (index, d) in enumerate(response_data) if d["type"] == "MainTitle"),
        None,
    )
    a_main_title = next(
        (
            index
            for (index, d) in enumerate(admin_response_data)
            if d["type"] == "MainTitle"
        ),
        None,
    )
    e_main_title = next(
        (
            index
            for (index, d) in enumerate(editor_response_data)
            if d["type"] == "MainTitle"
        ),
        None,
    )
    v_main_title = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data)
            if d["type"] == "MainTitle"
        ),
        None,
    )
    # search for admin title index
    admin_title = next(
        (
            index
            for (index, d) in enumerate(response_data)
            if d["title"] == "Admin Title"
        ),
        None,
    )
    a_admin_title = next(
        (
            index
            for (index, d) in enumerate(admin_response_data)
            if d["title"] == "Admin Title"
        ),
        None,
    )
    e_admin_title = next(
        (
            index
            for (index, d) in enumerate(editor_response_data)
            if d["title"] == "Admin Title"
        ),
        None,
    )
    v_admin_title = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data)
            if d["title"] == "Admin Title"
        ),
        None,
    )

    # search for editor title index
    editor_title = next(
        (
            index
            for (index, d) in enumerate(response_data)
            if d["title"] == "Editor Title"
        ),
        None,
    )
    a_editor_title = next(
        (
            index
            for (index, d) in enumerate(admin_response_data)
            if d["title"] == "Editor Title"
        ),
        None,
    )
    e_editor_title = next(
        (
            index
            for (index, d) in enumerate(editor_response_data)
            if d["title"] == "Editor Title"
        ),
        None,
    )
    v_editor_title = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data)
            if d["title"] == "Editor Title"
        ),
        None,
    )

    # search for owner title index
    own_title = next(
        (
            index
            for (index, d) in enumerate(response_data)
            if d["title"] == "Owner Title"
        ),
        None,
    )
    a_own_title = next(
        (
            index
            for (index, d) in enumerate(admin_response_data)
            if d["title"] == "Owner Title"
        ),
        None,
    )
    e_own_title = next(
        (
            index
            for (index, d) in enumerate(editor_response_data)
            if d["title"] == "Owner Title"
        ),
        None,
    )
    v_own_title = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data)
            if d["title"] == "Owner Title"
        ),
        None,
    )

    assert response_data[main_title]["title"] == "Dataset Title"
    assert response_data[main_title]["type"] == "MainTitle"
    assert response_data[own_title]["title"] == "Owner Title"
    assert response_data[own_title]["type"] == "Subtitle"
    assert response_data[admin_title]["title"] == "Admin Title"
    assert response_data[admin_title]["type"] == "Subtitle"
    assert response_data[editor_title]["title"] == "Editor Title"
    assert response_data[editor_title]["type"] == "Subtitle"

    assert admin_response_data[a_main_title]["title"] == "Dataset Title"
    assert admin_response_data[a_main_title]["type"] == "MainTitle"
    assert admin_response_data[a_own_title]["title"] == "Owner Title"
    assert admin_response_data[a_own_title]["type"] == "Subtitle"
    assert admin_response_data[a_admin_title]["title"] == "Admin Title"
    assert admin_response_data[a_admin_title]["type"] == "Subtitle"
    assert admin_response_data[a_editor_title]["title"] == "Editor Title"
    assert admin_response_data[a_editor_title]["type"] == "Subtitle"

    assert editor_response_data[e_main_title]["title"] == "Dataset Title"
    assert editor_response_data[e_main_title]["type"] == "MainTitle"
    assert editor_response_data[e_own_title]["title"] == "Owner Title"
    assert editor_response_data[e_own_title]["type"] == "Subtitle"
    assert editor_response_data[e_admin_title]["title"] == "Admin Title"
    assert editor_response_data[e_admin_title]["type"] == "Subtitle"
    assert editor_response_data[e_editor_title]["title"] == "Editor Title"
    assert editor_response_data[e_editor_title]["type"] == "Subtitle"

    assert viewer_response_data[v_main_title]["title"] == "Dataset Title"
    assert viewer_response_data[v_main_title]["type"] == "MainTitle"
    assert viewer_response_data[v_own_title]["title"] == "Owner Title"
    assert viewer_response_data[v_own_title]["type"] == "Subtitle"
    assert viewer_response_data[v_admin_title]["title"] == "Admin Title"
    assert viewer_response_data[v_admin_title]["type"] == "Subtitle"
    assert viewer_response_data[v_editor_title]["title"] == "Editor Title"
    assert viewer_response_data[v_editor_title]["type"] == "Subtitle"


def test_delete_dataset_title_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/title/{title_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    title metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    title_id = pytest.global_dataset_title_id
    admin_title_id = pytest.global_dataset_title_id_admin
    editor_title_id = pytest.global_dataset_title_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title/{title_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title/{title_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title/{admin_title_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title/{editor_title_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204
