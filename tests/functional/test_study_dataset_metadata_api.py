# pylint: disable=too-many-lines
"""Tests for the Dataset's Metadata API endpoints"""
import json

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

    print(admin_response.status_code)
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

    print(editor_response.status_code)
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

    print(viewer_response.status_code)
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
                "name": "Name here",
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_contributor_id = response_data[0]["id"]

    assert response_data[0]["name"] == "Name here"
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
                "name": "Admin Name here",
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

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_contributor_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["name"] == "Admin Name here"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor",
        json=[
            {
                "name": "Editor Name here",
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

    assert editor_response_data[0]["name"] == "Editor Name here"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor",
        json=[
            {
                "name": "Viewer Name here",
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

    print("$$$$$$$$$$")
    print(response.status_code)
    print("$$$$$$$$$$`")
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
                "name": "Name here",
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_creator_id = response_data[0]["id"]

    assert response_data[0]["name"] == "Name here"
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
                "name": "admin Name here",
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

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_creator_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["name"] == "admin Name here"
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
                "name": "Editor Name here",
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

    assert editor_response_data[0]["name"] == "Editor Name here"
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
                "name": "Viewer Name here",
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
    assert response_data[0]["name"] == "Name here"
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
    assert response_data[1]["name"] == "admin Name here"
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
    assert response_data[2]["name"] == "Editor Name here"
    assert response_data[2]["name_type"] == "Personal"
    assert response_data[2]["name_identifier"] == "Name identifier"
    assert response_data[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert response_data[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert response_data[2]["creator"] is True
    assert response_data[2]["affiliations"][0]["name"] == "Test"
    assert response_data[2]["affiliations"][0]["identifier"] == "yes"
    assert response_data[2]["affiliations"][0]["scheme"] == "uh"
    assert response_data[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert admin_response_data[0]["name"] == "Name here"
    assert admin_response_data[0]["name_type"] == "Personal"
    assert admin_response_data[0]["name_identifier"] == "Name identifier"
    assert admin_response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_response_data[0]["creator"] is True
    assert admin_response_data[0]["affiliations"][0]["name"] == "Test"
    assert admin_response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert admin_response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert admin_response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert admin_response_data[1]["name"] == "admin Name here"
    assert admin_response_data[1]["name_type"] == "Personal"
    assert admin_response_data[1]["name_identifier"] == "Name identifier"
    assert admin_response_data[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_response_data[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_response_data[1]["creator"] is True
    assert admin_response_data[1]["affiliations"][0]["name"] == "Test"
    assert admin_response_data[1]["affiliations"][0]["identifier"] == "yes"
    assert admin_response_data[1]["affiliations"][0]["scheme"] == "uh"
    assert admin_response_data[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert admin_response_data[2]["name"] == "Editor Name here"
    assert admin_response_data[2]["name_type"] == "Personal"
    assert admin_response_data[2]["name_identifier"] == "Name identifier"
    assert admin_response_data[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_response_data[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_response_data[2]["creator"] is True
    assert admin_response_data[2]["affiliations"][0]["name"] == "Test"
    assert admin_response_data[2]["affiliations"][0]["identifier"] == "yes"
    assert admin_response_data[2]["affiliations"][0]["scheme"] == "uh"
    assert admin_response_data[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert editor_response_data[0]["name"] == "Name here"
    assert editor_response_data[0]["name_type"] == "Personal"
    assert editor_response_data[0]["name_identifier"] == "Name identifier"
    assert editor_response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_response_data[0]["creator"] is True
    assert editor_response_data[0]["affiliations"][0]["name"] == "Test"
    assert editor_response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert editor_response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert editor_response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert editor_response_data[1]["name"] == "admin Name here"
    assert editor_response_data[1]["name_type"] == "Personal"
    assert editor_response_data[1]["name_identifier"] == "Name identifier"
    assert editor_response_data[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_response_data[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_response_data[1]["creator"] is True
    assert editor_response_data[1]["affiliations"][0]["name"] == "Test"
    assert editor_response_data[1]["affiliations"][0]["identifier"] == "yes"
    assert editor_response_data[1]["affiliations"][0]["scheme"] == "uh"
    assert editor_response_data[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert editor_response_data[2]["name"] == "Editor Name here"
    assert editor_response_data[2]["name_type"] == "Personal"
    assert editor_response_data[2]["name_identifier"] == "Name identifier"
    assert editor_response_data[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_response_data[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_response_data[2]["creator"] is True
    assert editor_response_data[2]["affiliations"][0]["name"] == "Test"
    assert editor_response_data[2]["affiliations"][0]["identifier"] == "yes"
    assert editor_response_data[2]["affiliations"][0]["scheme"] == "uh"
    assert editor_response_data[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert viewer_response_data[0]["name"] == "Name here"
    assert viewer_response_data[0]["name_type"] == "Personal"
    assert viewer_response_data[0]["name_identifier"] == "Name identifier"
    assert viewer_response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert viewer_response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert viewer_response_data[0]["creator"] is True
    assert viewer_response_data[0]["affiliations"][0]["name"] == "Test"
    assert viewer_response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert viewer_response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert viewer_response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[1]["name"] == "admin Name here"
    assert viewer_response_data[1]["name_type"] == "Personal"
    assert viewer_response_data[1]["name_identifier"] == "Name identifier"
    assert viewer_response_data[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert viewer_response_data[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert viewer_response_data[1]["creator"] is True
    assert viewer_response_data[1]["affiliations"][0]["name"] == "Test"
    assert viewer_response_data[1]["affiliations"][0]["identifier"] == "yes"
    assert viewer_response_data[1]["affiliations"][0]["scheme"] == "uh"
    assert viewer_response_data[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[2]["name"] == "Editor Name here"
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_description_id = response_data[0]["id"]

    assert response_data[0]["description"] == "Owner Description"
    assert response_data[0]["type"] == "Methods"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description",
        json=[{"description": "Admin Description", "type": "Methods"}],
    )

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

    print(response_data)
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

    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204
    assert viewer_response.status_code == 403


# ------------------- FUNDER METADATA ------------------- #
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

    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{funder_id}"
    )

    assert response.status_code == 204


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


# ------------------- RECORD KEYS METADATA ------------------- #
def test_put_dataset_record_keys_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    record keys metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys",
        json={"type": "Record Type", "details": "Details for Record Keys"},
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["type"] == "Record Type"
    assert response_data["details"] == "Details for Record Keys"

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys",
        json={"type": "Record Type", "details": "Admin Details for Record Keys"},
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["type"] == "Record Type"
    assert admin_response_data["details"] == "Admin Details for Record Keys"

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys",
        json={"type": "Record Type", "details": "Editor Details for Record Keys"},
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["type"] == "Record Type"
    assert editor_response_data["details"] == "Editor Details for Record Keys"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys",
        json={"type": "Record Type", "details": "Viewer Details for Record Keys"},
    )

    assert viewer_response.status_code == 403


def test_get_dataset_record_keys_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    record keys metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys"
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
    assert response_data["type"] == "Record Type"
    assert response_data["details"] == "Editor Details for Record Keys"

    assert admin_response_data["type"] == "Record Type"
    assert admin_response_data["details"] == "Editor Details for Record Keys"

    assert editor_response_data["type"] == "Record Type"
    assert editor_response_data["details"] == "Editor Details for Record Keys"

    assert viewer_response_data["type"] == "Record Type"
    assert viewer_response_data["details"] == "Editor Details for Record Keys"


# ------------------- RELATED ITEM METADATA ------------------- #
def test_post_dataset_related_item_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/related-item'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    related item metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item",
        json=[
            {
                "contributors": [
                    {
                        "name": "Ndafsdame",
                        "contributor_type": "Con Type",
                        "name_type": "Personal",
                    }
                ],
                "creators": [{"name": "Name", "name_type": "Personal"}],
                "edition": "Edition",
                "first_page": "First Page",
                "identifiers": [
                    {
                        "identifier": "Identifier",
                        "metadata_scheme": "Metadata Scheme",
                        "scheme_type": "Scheme Type",
                        "scheme_uri": "Scheme URI",
                        "type": "ARK",
                    }
                ],
                "issue": "Issue",
                "last_page": "Last Page",
                "number_type": "Number Type",
                "number_value": "Number Value",
                "publication_year": 2013,
                "publisher": "Publisher",
                "relation_type": "Relation Type",
                "titles": [
                    {"title": "Title", "type": "MainTitle"},
                    {"title": "Title", "type": "Subtitle"},
                ],
                "type": "Type",
                "volume": "Volume",
            }
        ],
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    # seach for main title index in response_data[n]["titles"]
    main_title_0 = next(
        (
            index
            for (index, d) in enumerate(response_data[0]["titles"])
            if d["type"] == "MainTitle"
        ),
        None,
    )
    # seach for subtitle index in response_data[n]["titles"]
    sub_title_0 = next(
        (
            index
            for (index, d) in enumerate(response_data[0]["titles"])
            if d["type"] == "Subtitle"
        ),
        None,
    )
    pytest.global_dataset_related_item_id = response_data[0]["id"]
    pytest.global_dataset_related_item_contributor_id = response_data[0][
        "contributors"
    ][0]["id"]
    pytest.global_dataset_related_item_creator_id = response_data[0]["creators"][0][
        "id"
    ]
    pytest.global_dataset_related_item_identifier_id = response_data[0]["identifiers"][
        0
    ]["id"]
    # pylint: disable=line-too-long
    pytest.global_dataset_related_item_main_title_id = response_data[0]["titles"][
        main_title_0
    ]["id"]
    pytest.global_dataset_related_item_sub_title_id = response_data[0]["titles"][
        sub_title_0
    ]["id"]

    assert response_data[0]["contributors"][0]["name"] == "Ndafsdame"
    assert response_data[0]["contributors"][0]["contributor_type"] == "Con Type"
    assert response_data[0]["contributors"][0]["name_type"] == "Personal"
    assert response_data[0]["creators"][0]["name"] == "Name"
    assert response_data[0]["creators"][0]["name_type"] == "Personal"
    assert response_data[0]["edition"] == "Edition"
    assert response_data[0]["first_page"] == "First Page"
    assert response_data[0]["identifiers"][0]["identifier"] == "Identifier"
    assert response_data[0]["identifiers"][0]["metadata_scheme"] == "Metadata Scheme"
    assert response_data[0]["identifiers"][0]["scheme_type"] == "Scheme Type"
    assert response_data[0]["identifiers"][0]["scheme_uri"] == "Scheme URI"
    assert response_data[0]["identifiers"][0]["type"] == "ARK"
    assert response_data[0]["issue"] == "Issue"
    assert response_data[0]["last_page"] == "Last Page"
    assert response_data[0]["number_type"] == "Number Type"
    assert response_data[0]["number_value"] == "Number Value"
    assert response_data[0]["publication_year"] == 2013
    assert response_data[0]["publisher"] == "Publisher"
    assert response_data[0]["relation_type"] == "Relation Type"
    assert response_data[0]["titles"][main_title_0]["title"] == "Title"
    assert response_data[0]["titles"][main_title_0]["type"] == "MainTitle"
    assert response_data[0]["titles"][sub_title_0]["title"] == "Title"
    assert response_data[0]["titles"][sub_title_0]["type"] == "Subtitle"
    assert response_data[0]["type"] == "Type"
    assert response_data[0]["volume"] == "Volume"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item",
        json=[
            {
                "contributors": [
                    {
                        "name": "Admin Ndafsdame",
                        "contributor_type": "Admin Con Type",
                        "name_type": "Personal",
                    }
                ],
                "creators": [{"name": "Admin Name", "name_type": "Personal"}],
                "edition": "Admin Edition",
                "first_page": "Admin First Page",
                "identifiers": [
                    {
                        "identifier": "Admin Identifier",
                        "metadata_scheme": "Admin Metadata Scheme",
                        "scheme_type": "Admin Scheme Type",
                        "scheme_uri": "Admin Scheme URI",
                        "type": "ARK",
                    }
                ],
                "issue": "Admin Issue",
                "last_page": "Admin Last Page",
                "number_type": "Admin Number Type",
                "number_value": "Admin Number Value",
                "publication_year": 2013,
                "publisher": "Admin Publisher",
                "relation_type": "Admin Relation Type",
                "titles": [{"title": "Admin Title", "type": "AlternativeTitle"}],
                "type": "Admin Type",
                "volume": "Admin Volume",
            }
        ],
    )

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_related_item_id_admin = admin_response_data[1]["id"]
    pytest.global_dataset_related_item_contributor_id_admin = admin_response_data[1][
        "contributors"
    ][0]["id"]
    pytest.global_dataset_related_item_creator_id_admin = admin_response_data[1][
        "creators"
    ][0]["id"]
    pytest.global_dataset_related_item_identifier_id_admin = admin_response_data[1][
        "identifiers"
    ][0]["id"]
    pytest.global_dataset_related_item_title_id_admin = admin_response_data[1][
        "titles"
    ][0]["id"]

    assert admin_response_data[1]["contributors"][0]["name"] == "Admin Ndafsdame"
    assert (
        admin_response_data[1]["contributors"][0]["contributor_type"]
        == "Admin Con Type"
    )
    assert admin_response_data[1]["contributors"][0]["name_type"] == "Personal"
    assert admin_response_data[1]["creators"][0]["name"] == "Admin Name"
    assert admin_response_data[1]["creators"][0]["name_type"] == "Personal"
    assert admin_response_data[1]["edition"] == "Admin Edition"
    assert admin_response_data[1]["first_page"] == "Admin First Page"
    assert admin_response_data[1]["identifiers"][0]["identifier"] == "Admin Identifier"
    assert (
        admin_response_data[1]["identifiers"][0]["metadata_scheme"]
        == "Admin Metadata Scheme"
    )
    assert (
        admin_response_data[1]["identifiers"][0]["scheme_type"] == "Admin Scheme Type"
    )
    assert admin_response_data[1]["identifiers"][0]["scheme_uri"] == "Admin Scheme URI"
    assert admin_response_data[1]["identifiers"][0]["type"] == "ARK"
    assert admin_response_data[1]["issue"] == "Admin Issue"
    assert admin_response_data[1]["last_page"] == "Admin Last Page"
    assert admin_response_data[1]["number_type"] == "Admin Number Type"
    assert admin_response_data[1]["number_value"] == "Admin Number Value"
    assert admin_response_data[1]["publication_year"] == 2013
    assert admin_response_data[1]["publisher"] == "Admin Publisher"
    assert admin_response_data[1]["relation_type"] == "Admin Relation Type"
    assert admin_response_data[1]["titles"][0]["title"] == "Admin Title"
    assert admin_response_data[1]["titles"][0]["type"] == "AlternativeTitle"
    assert admin_response_data[1]["type"] == "Admin Type"
    assert admin_response_data[1]["volume"] == "Admin Volume"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item",
        json=[
            {
                "contributors": [
                    {
                        "name": "Editor Ndafsdame",
                        "contributor_type": "Editor Con Type",
                        "name_type": "Personal",
                    }
                ],
                "creators": [{"name": "Editor Name", "name_type": "Personal"}],
                "edition": "Editor Edition",
                "first_page": "Editor First Page",
                "identifiers": [
                    {
                        "identifier": "Editor Identifier",
                        "metadata_scheme": "Editor Metadata Scheme",
                        "scheme_type": "Editor Scheme Type",
                        "scheme_uri": "Editor Scheme URI",
                        "type": "ARK",
                    }
                ],
                "issue": "Editor Issue",
                "last_page": "Editor Last Page",
                "number_type": "Editor Number Type",
                "number_value": "Editor Number Value",
                "publication_year": 2013,
                "publisher": "Editor Publisher",
                "relation_type": "Editor Relation Type",
                "titles": [{"title": "Editor Title", "type": "Subtitle"}],
                "type": "Editor Type",
                "volume": "Editor Volume",
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_related_item_id_editor = editor_response_data[2]["id"]
    pytest.global_dataset_related_item_contributor_id_editor = editor_response_data[2][
        "contributors"
    ][0]["id"]
    pytest.global_dataset_related_item_creator_id_editor = editor_response_data[2][
        "creators"
    ][0]["id"]
    pytest.global_dataset_related_item_identifier_id_editor = editor_response_data[2][
        "identifiers"
    ][0]["id"]
    pytest.global_dataset_related_item_title_id_editor = editor_response_data[2][
        "titles"
    ][0]["id"]

    assert editor_response_data[2]["contributors"][0]["name"] == "Editor Ndafsdame"
    assert (
        editor_response_data[2]["contributors"][0]["contributor_type"]
        == "Editor Con Type"
    )
    assert editor_response_data[2]["contributors"][0]["name_type"] == "Personal"
    assert editor_response_data[2]["creators"][0]["name"] == "Editor Name"
    assert editor_response_data[2]["creators"][0]["name_type"] == "Personal"
    assert editor_response_data[2]["edition"] == "Editor Edition"
    assert editor_response_data[2]["first_page"] == "Editor First Page"
    assert (
        editor_response_data[2]["identifiers"][0]["identifier"] == "Editor Identifier"
    )
    assert (
        editor_response_data[2]["identifiers"][0]["metadata_scheme"]
        == "Editor Metadata Scheme"
    )
    assert (
        editor_response_data[2]["identifiers"][0]["scheme_type"] == "Editor Scheme Type"
    )
    assert (
        editor_response_data[2]["identifiers"][0]["scheme_uri"] == "Editor Scheme URI"
    )
    assert editor_response_data[2]["identifiers"][0]["type"] == "ARK"
    assert editor_response_data[2]["issue"] == "Editor Issue"
    assert editor_response_data[2]["last_page"] == "Editor Last Page"
    assert editor_response_data[2]["number_type"] == "Editor Number Type"
    assert editor_response_data[2]["number_value"] == "Editor Number Value"
    assert editor_response_data[2]["publication_year"] == 2013
    assert editor_response_data[2]["publisher"] == "Editor Publisher"
    assert editor_response_data[2]["relation_type"] == "Editor Relation Type"
    assert editor_response_data[2]["titles"][0]["title"] == "Editor Title"
    assert editor_response_data[2]["titles"][0]["type"] == "Subtitle"
    assert editor_response_data[2]["type"] == "Editor Type"
    assert editor_response_data[2]["volume"] == "Editor Volume"

    viewer_client = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item",
        json=[
            {
                "contributors": [
                    {
                        "name": "Viewer Ndafsdame",
                        "contributor_type": "Viewer Con Type",
                        "name_type": "Personal",
                    }
                ],
                "creators": [{"name": "Viewer Name", "name_type": "Personal"}],
                "edition": "Viewer Edition",
                "first_page": "Viewer First Page",
                "identifiers": [
                    {
                        "identifier": "Viewer Identifier",
                        "metadata_scheme": "Viewer Metadata Scheme",
                        "scheme_type": "Viewer Scheme Type",
                        "scheme_uri": "Viewer Scheme URI",
                        "type": "ARK",
                    }
                ],
                "issue": "Viewer Issue",
                "last_page": "Viewer Last Page",
                "number_type": "Viewer Number Type",
                "number_value": "Viewer Number Value",
                "publication_year": 2013,
                "publisher": "Viewer Publisher",
                "relation_type": "Viewer Relation Type",
                "titles": [{"title": "Viewer Title", "type": "Subtitle"}],
                "type": "Viewer Type",
                "volume": "Viewer Volume",
            }
        ],
    )

    assert viewer_client.status_code == 403


def test_get_dataset_related_item_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    related item metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # seach for main title index in response_data[n]["titles"]
    # pylint: disable=line-too-long
    main_title_0 = next(
        (
            index
            for (index, d) in enumerate(response_data[0]["titles"])
            if d["type"] == "MainTitle"
        ),
        None,
    )
    # seach for subtitle index in response_data[n]["titles"]
    sub_title_0 = next(
        (
            index
            for (index, d) in enumerate(response_data[0]["titles"])
            if d["type"] == "Subtitle"
        ),
        None,
    )
    a_main_title_0 = next(
        (
            index
            for (index, d) in enumerate(admin_response_data[0]["titles"])
            if d["type"] == "MainTitle"
        ),
        None,
    )
    a_sub_title_0 = next(
        (
            index
            for (index, d) in enumerate(admin_response_data[0]["titles"])
            if d["type"] == "Subtitle"
        ),
        None,
    )
    e_main_title_0 = next(
        (
            index
            for (index, d) in enumerate(editor_response_data[0]["titles"])
            if d["type"] == "MainTitle"
        ),
        None,
    )
    e_sub_title_0 = next(
        (
            index
            for (index, d) in enumerate(editor_response_data[0]["titles"])
            if d["type"] == "Subtitle"
        ),
        None,
    )
    v_main_title_0 = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data[0]["titles"])
            if d["type"] == "MainTitle"
        ),
        None,
    )
    v_sub_title_0 = next(
        (
            index
            for (index, d) in enumerate(viewer_response_data[0]["titles"])
            if d["type"] == "Subtitle"
        ),
        None,
    )

    assert response_data[0]["contributors"][0]["name"] == "Ndafsdame"
    assert response_data[0]["contributors"][0]["contributor_type"] == "Con Type"
    assert response_data[0]["contributors"][0]["name_type"] == "Personal"
    assert response_data[0]["creators"][0]["name"] == "Name"
    assert response_data[0]["creators"][0]["name_type"] == "Personal"
    assert response_data[0]["edition"] == "Edition"
    assert response_data[0]["first_page"] == "First Page"
    assert response_data[0]["identifiers"][0]["identifier"] == "Identifier"
    assert response_data[0]["identifiers"][0]["metadata_scheme"] == "Metadata Scheme"
    assert response_data[0]["identifiers"][0]["scheme_type"] == "Scheme Type"
    assert response_data[0]["identifiers"][0]["scheme_uri"] == "Scheme URI"
    assert response_data[0]["identifiers"][0]["type"] == "ARK"
    assert response_data[0]["issue"] == "Issue"
    assert response_data[0]["last_page"] == "Last Page"
    assert response_data[0]["number_type"] == "Number Type"
    assert response_data[0]["number_value"] == "Number Value"
    assert response_data[0]["publication_year"] == 2013
    assert response_data[0]["publisher"] == "Publisher"
    assert response_data[0]["relation_type"] == "Relation Type"
    assert response_data[0]["titles"][main_title_0]["title"] == "Title"
    assert response_data[0]["titles"][main_title_0]["type"] == "MainTitle"
    assert response_data[0]["titles"][sub_title_0]["title"] == "Title"
    assert response_data[0]["titles"][sub_title_0]["type"] == "Subtitle"
    assert response_data[0]["type"] == "Type"
    assert response_data[0]["volume"] == "Volume"
    assert response_data[1]["contributors"][0]["name"] == "Admin Ndafsdame"
    assert response_data[1]["contributors"][0]["contributor_type"] == "Admin Con Type"
    assert response_data[1]["contributors"][0]["name_type"] == "Personal"
    assert response_data[1]["creators"][0]["name"] == "Admin Name"
    assert response_data[1]["creators"][0]["name_type"] == "Personal"
    assert response_data[1]["edition"] == "Admin Edition"
    assert response_data[1]["first_page"] == "Admin First Page"
    assert response_data[1]["identifiers"][0]["identifier"] == "Admin Identifier"
    assert (
        response_data[1]["identifiers"][0]["metadata_scheme"] == "Admin Metadata Scheme"
    )
    assert response_data[1]["identifiers"][0]["scheme_type"] == "Admin Scheme Type"
    assert response_data[1]["identifiers"][0]["scheme_uri"] == "Admin Scheme URI"
    assert response_data[1]["identifiers"][0]["type"] == "ARK"
    assert response_data[1]["issue"] == "Admin Issue"
    assert response_data[1]["last_page"] == "Admin Last Page"
    assert response_data[1]["number_type"] == "Admin Number Type"
    assert response_data[1]["number_value"] == "Admin Number Value"
    assert response_data[1]["publication_year"] == 2013
    assert response_data[1]["publisher"] == "Admin Publisher"
    assert response_data[1]["relation_type"] == "Admin Relation Type"
    assert response_data[1]["titles"][0]["title"] == "Admin Title"
    assert response_data[1]["titles"][0]["type"] == "AlternativeTitle"
    assert response_data[1]["type"] == "Admin Type"
    assert response_data[1]["volume"] == "Admin Volume"
    assert response_data[2]["contributors"][0]["name"] == "Editor Ndafsdame"
    assert response_data[2]["contributors"][0]["contributor_type"] == "Editor Con Type"
    assert response_data[2]["contributors"][0]["name_type"] == "Personal"
    assert response_data[2]["creators"][0]["name"] == "Editor Name"
    assert response_data[2]["creators"][0]["name_type"] == "Personal"
    assert response_data[2]["edition"] == "Editor Edition"
    assert response_data[2]["first_page"] == "Editor First Page"
    assert response_data[2]["identifiers"][0]["identifier"] == "Editor Identifier"
    assert (
        response_data[2]["identifiers"][0]["metadata_scheme"]
        == "Editor Metadata Scheme"
    )
    assert response_data[2]["identifiers"][0]["scheme_type"] == "Editor Scheme Type"
    assert response_data[2]["identifiers"][0]["scheme_uri"] == "Editor Scheme URI"
    assert response_data[2]["identifiers"][0]["type"] == "ARK"
    assert response_data[2]["issue"] == "Editor Issue"
    assert response_data[2]["last_page"] == "Editor Last Page"
    assert response_data[2]["number_type"] == "Editor Number Type"
    assert response_data[2]["number_value"] == "Editor Number Value"
    assert response_data[2]["publication_year"] == 2013
    assert response_data[2]["publisher"] == "Editor Publisher"
    assert response_data[2]["relation_type"] == "Editor Relation Type"
    assert response_data[2]["titles"][0]["title"] == "Editor Title"
    assert response_data[2]["titles"][0]["type"] == "Subtitle"
    assert response_data[2]["type"] == "Editor Type"
    assert response_data[2]["volume"] == "Editor Volume"

    assert admin_response_data[0]["contributors"][0]["name"] == "Ndafsdame"
    assert admin_response_data[0]["contributors"][0]["contributor_type"] == "Con Type"
    assert admin_response_data[0]["contributors"][0]["name_type"] == "Personal"
    assert admin_response_data[0]["creators"][0]["name"] == "Name"
    assert admin_response_data[0]["creators"][0]["name_type"] == "Personal"
    assert admin_response_data[0]["edition"] == "Edition"
    assert admin_response_data[0]["first_page"] == "First Page"
    assert admin_response_data[0]["identifiers"][0]["identifier"] == "Identifier"
    assert (
        admin_response_data[0]["identifiers"][0]["metadata_scheme"] == "Metadata Scheme"
    )
    assert admin_response_data[0]["identifiers"][0]["scheme_type"] == "Scheme Type"
    assert admin_response_data[0]["identifiers"][0]["scheme_uri"] == "Scheme URI"
    assert admin_response_data[0]["identifiers"][0]["type"] == "ARK"
    assert admin_response_data[0]["issue"] == "Issue"
    assert admin_response_data[0]["last_page"] == "Last Page"
    assert admin_response_data[0]["number_type"] == "Number Type"
    assert admin_response_data[0]["number_value"] == "Number Value"
    assert admin_response_data[0]["publication_year"] == 2013
    assert admin_response_data[0]["publisher"] == "Publisher"
    assert admin_response_data[0]["relation_type"] == "Relation Type"
    assert admin_response_data[0]["titles"][a_main_title_0]["title"] == "Title"
    assert admin_response_data[0]["titles"][a_main_title_0]["type"] == "MainTitle"
    assert admin_response_data[0]["titles"][a_sub_title_0]["title"] == "Title"
    assert admin_response_data[0]["titles"][a_sub_title_0]["type"] == "Subtitle"
    assert admin_response_data[0]["type"] == "Type"
    assert admin_response_data[0]["volume"] == "Volume"
    assert admin_response_data[1]["contributors"][0]["name"] == "Admin Ndafsdame"
    assert (
        admin_response_data[1]["contributors"][0]["contributor_type"]
        == "Admin Con Type"
    )
    assert admin_response_data[1]["contributors"][0]["name_type"] == "Personal"
    assert admin_response_data[1]["creators"][0]["name"] == "Admin Name"
    assert admin_response_data[1]["creators"][0]["name_type"] == "Personal"
    assert admin_response_data[1]["edition"] == "Admin Edition"
    assert admin_response_data[1]["first_page"] == "Admin First Page"
    assert admin_response_data[1]["identifiers"][0]["identifier"] == "Admin Identifier"
    assert (
        admin_response_data[1]["identifiers"][0]["metadata_scheme"]
        == "Admin Metadata Scheme"
    )
    assert (
        admin_response_data[1]["identifiers"][0]["scheme_type"] == "Admin Scheme Type"
    )
    assert admin_response_data[1]["identifiers"][0]["scheme_uri"] == "Admin Scheme URI"
    assert admin_response_data[1]["identifiers"][0]["type"] == "ARK"
    assert admin_response_data[1]["issue"] == "Admin Issue"
    assert admin_response_data[1]["last_page"] == "Admin Last Page"
    assert admin_response_data[1]["number_type"] == "Admin Number Type"
    assert admin_response_data[1]["number_value"] == "Admin Number Value"
    assert admin_response_data[1]["publication_year"] == 2013
    assert admin_response_data[1]["publisher"] == "Admin Publisher"
    assert admin_response_data[1]["relation_type"] == "Admin Relation Type"
    assert admin_response_data[1]["titles"][0]["title"] == "Admin Title"
    assert admin_response_data[1]["titles"][0]["type"] == "AlternativeTitle"
    assert admin_response_data[1]["type"] == "Admin Type"
    assert admin_response_data[1]["volume"] == "Admin Volume"
    assert admin_response_data[2]["contributors"][0]["name"] == "Editor Ndafsdame"
    assert (
        admin_response_data[2]["contributors"][0]["contributor_type"]
        == "Editor Con Type"
    )
    assert admin_response_data[2]["contributors"][0]["name_type"] == "Personal"
    assert admin_response_data[2]["creators"][0]["name"] == "Editor Name"
    assert admin_response_data[2]["creators"][0]["name_type"] == "Personal"
    assert admin_response_data[2]["edition"] == "Editor Edition"
    assert admin_response_data[2]["first_page"] == "Editor First Page"
    assert admin_response_data[2]["identifiers"][0]["identifier"] == "Editor Identifier"
    assert (
        admin_response_data[2]["identifiers"][0]["metadata_scheme"]
        == "Editor Metadata Scheme"
    )
    assert (
        admin_response_data[2]["identifiers"][0]["scheme_type"] == "Editor Scheme Type"
    )
    assert admin_response_data[2]["identifiers"][0]["scheme_uri"] == "Editor Scheme URI"
    assert admin_response_data[2]["identifiers"][0]["type"] == "ARK"
    assert admin_response_data[2]["issue"] == "Editor Issue"
    assert admin_response_data[2]["last_page"] == "Editor Last Page"
    assert admin_response_data[2]["number_type"] == "Editor Number Type"
    assert admin_response_data[2]["number_value"] == "Editor Number Value"
    assert admin_response_data[2]["publication_year"] == 2013
    assert admin_response_data[2]["publisher"] == "Editor Publisher"
    assert admin_response_data[2]["relation_type"] == "Editor Relation Type"
    assert admin_response_data[2]["titles"][0]["title"] == "Editor Title"
    assert admin_response_data[2]["titles"][0]["type"] == "Subtitle"
    assert admin_response_data[2]["type"] == "Editor Type"
    assert admin_response_data[2]["volume"] == "Editor Volume"

    assert editor_response_data[0]["contributors"][0]["name"] == "Ndafsdame"
    assert editor_response_data[0]["contributors"][0]["contributor_type"] == "Con Type"
    assert editor_response_data[0]["contributors"][0]["name_type"] == "Personal"
    assert editor_response_data[0]["creators"][0]["name"] == "Name"
    assert editor_response_data[0]["creators"][0]["name_type"] == "Personal"
    assert editor_response_data[0]["edition"] == "Edition"
    assert editor_response_data[0]["first_page"] == "First Page"
    assert editor_response_data[0]["identifiers"][0]["identifier"] == "Identifier"
    assert (
        editor_response_data[0]["identifiers"][0]["metadata_scheme"]
        == "Metadata Scheme"
    )
    assert editor_response_data[0]["identifiers"][0]["scheme_type"] == "Scheme Type"
    assert editor_response_data[0]["identifiers"][0]["scheme_uri"] == "Scheme URI"
    assert editor_response_data[0]["identifiers"][0]["type"] == "ARK"
    assert editor_response_data[0]["issue"] == "Issue"
    assert editor_response_data[0]["last_page"] == "Last Page"
    assert editor_response_data[0]["number_type"] == "Number Type"
    assert editor_response_data[0]["number_value"] == "Number Value"
    assert editor_response_data[0]["publication_year"] == 2013
    assert editor_response_data[0]["publisher"] == "Publisher"
    assert editor_response_data[0]["relation_type"] == "Relation Type"
    assert editor_response_data[0]["titles"][e_main_title_0]["title"] == "Title"
    assert editor_response_data[0]["titles"][e_main_title_0]["type"] == "MainTitle"
    assert editor_response_data[0]["titles"][e_sub_title_0]["title"] == "Title"
    assert editor_response_data[0]["titles"][e_sub_title_0]["type"] == "Subtitle"
    assert editor_response_data[0]["type"] == "Type"
    assert editor_response_data[0]["volume"] == "Volume"
    assert editor_response_data[1]["contributors"][0]["name"] == "Admin Ndafsdame"
    assert (
        editor_response_data[1]["contributors"][0]["contributor_type"]
        == "Admin Con Type"
    )
    assert editor_response_data[1]["contributors"][0]["name_type"] == "Personal"
    assert editor_response_data[1]["creators"][0]["name"] == "Admin Name"
    assert editor_response_data[1]["creators"][0]["name_type"] == "Personal"
    assert editor_response_data[1]["edition"] == "Admin Edition"
    assert editor_response_data[1]["first_page"] == "Admin First Page"
    assert editor_response_data[1]["identifiers"][0]["identifier"] == "Admin Identifier"
    assert (
        editor_response_data[1]["identifiers"][0]["metadata_scheme"]
        == "Admin Metadata Scheme"
    )
    assert (
        editor_response_data[1]["identifiers"][0]["scheme_type"] == "Admin Scheme Type"
    )
    assert editor_response_data[1]["identifiers"][0]["scheme_uri"] == "Admin Scheme URI"
    assert editor_response_data[1]["identifiers"][0]["type"] == "ARK"
    assert editor_response_data[1]["issue"] == "Admin Issue"
    assert editor_response_data[1]["last_page"] == "Admin Last Page"
    assert editor_response_data[1]["number_type"] == "Admin Number Type"
    assert editor_response_data[1]["number_value"] == "Admin Number Value"
    assert editor_response_data[1]["publication_year"] == 2013
    assert editor_response_data[1]["publisher"] == "Admin Publisher"
    assert editor_response_data[1]["relation_type"] == "Admin Relation Type"
    assert editor_response_data[1]["titles"][0]["title"] == "Admin Title"
    assert editor_response_data[1]["titles"][0]["type"] == "AlternativeTitle"
    assert editor_response_data[1]["type"] == "Admin Type"
    assert editor_response_data[1]["volume"] == "Admin Volume"
    assert editor_response_data[2]["contributors"][0]["name"] == "Editor Ndafsdame"
    assert (
        editor_response_data[2]["contributors"][0]["contributor_type"]
        == "Editor Con Type"
    )
    assert editor_response_data[2]["contributors"][0]["name_type"] == "Personal"
    assert editor_response_data[2]["creators"][0]["name"] == "Editor Name"
    assert editor_response_data[2]["creators"][0]["name_type"] == "Personal"
    assert editor_response_data[2]["edition"] == "Editor Edition"
    assert editor_response_data[2]["first_page"] == "Editor First Page"
    assert (
        editor_response_data[2]["identifiers"][0]["identifier"] == "Editor Identifier"
    )
    assert (
        editor_response_data[2]["identifiers"][0]["metadata_scheme"]
        == "Editor Metadata Scheme"
    )
    assert (
        editor_response_data[2]["identifiers"][0]["scheme_type"] == "Editor Scheme Type"
    )
    assert (
        editor_response_data[2]["identifiers"][0]["scheme_uri"] == "Editor Scheme URI"
    )
    assert editor_response_data[2]["identifiers"][0]["type"] == "ARK"
    assert editor_response_data[2]["issue"] == "Editor Issue"
    assert editor_response_data[2]["last_page"] == "Editor Last Page"
    assert editor_response_data[2]["number_type"] == "Editor Number Type"
    assert editor_response_data[2]["number_value"] == "Editor Number Value"
    assert editor_response_data[2]["publication_year"] == 2013
    assert editor_response_data[2]["publisher"] == "Editor Publisher"
    assert editor_response_data[2]["relation_type"] == "Editor Relation Type"
    assert editor_response_data[2]["titles"][0]["title"] == "Editor Title"
    assert editor_response_data[2]["titles"][0]["type"] == "Subtitle"
    assert editor_response_data[2]["type"] == "Editor Type"
    assert editor_response_data[2]["volume"] == "Editor Volume"

    assert viewer_response_data[0]["contributors"][0]["name"] == "Ndafsdame"
    assert viewer_response_data[0]["contributors"][0]["contributor_type"] == "Con Type"
    assert viewer_response_data[0]["contributors"][0]["name_type"] == "Personal"
    assert viewer_response_data[0]["creators"][0]["name"] == "Name"
    assert viewer_response_data[0]["creators"][0]["name_type"] == "Personal"
    assert viewer_response_data[0]["edition"] == "Edition"
    assert viewer_response_data[0]["first_page"] == "First Page"
    assert viewer_response_data[0]["identifiers"][0]["identifier"] == "Identifier"
    assert (
        viewer_response_data[0]["identifiers"][0]["metadata_scheme"]
        == "Metadata Scheme"
    )
    assert viewer_response_data[0]["identifiers"][0]["scheme_type"] == "Scheme Type"
    assert viewer_response_data[0]["identifiers"][0]["scheme_uri"] == "Scheme URI"
    assert viewer_response_data[0]["identifiers"][0]["type"] == "ARK"
    assert viewer_response_data[0]["issue"] == "Issue"
    assert viewer_response_data[0]["last_page"] == "Last Page"
    assert viewer_response_data[0]["number_type"] == "Number Type"
    assert viewer_response_data[0]["number_value"] == "Number Value"
    assert viewer_response_data[0]["publication_year"] == 2013
    assert viewer_response_data[0]["publisher"] == "Publisher"
    assert viewer_response_data[0]["relation_type"] == "Relation Type"
    assert viewer_response_data[0]["titles"][v_main_title_0]["title"] == "Title"
    assert viewer_response_data[0]["titles"][v_main_title_0]["type"] == "MainTitle"
    assert viewer_response_data[0]["titles"][v_sub_title_0]["title"] == "Title"
    assert viewer_response_data[0]["titles"][v_sub_title_0]["type"] == "Subtitle"
    assert viewer_response_data[0]["type"] == "Type"
    assert viewer_response_data[0]["volume"] == "Volume"
    assert viewer_response_data[1]["contributors"][0]["name"] == "Admin Ndafsdame"
    assert (
        viewer_response_data[1]["contributors"][0]["contributor_type"]
        == "Admin Con Type"
    )
    assert viewer_response_data[1]["contributors"][0]["name_type"] == "Personal"
    assert viewer_response_data[1]["creators"][0]["name"] == "Admin Name"
    assert viewer_response_data[1]["creators"][0]["name_type"] == "Personal"
    assert viewer_response_data[1]["edition"] == "Admin Edition"
    assert viewer_response_data[1]["first_page"] == "Admin First Page"
    assert viewer_response_data[1]["identifiers"][0]["identifier"] == "Admin Identifier"
    assert (
        viewer_response_data[1]["identifiers"][0]["metadata_scheme"]
        == "Admin Metadata Scheme"
    )
    assert (
        viewer_response_data[1]["identifiers"][0]["scheme_type"] == "Admin Scheme Type"
    )
    assert viewer_response_data[1]["identifiers"][0]["scheme_uri"] == "Admin Scheme URI"
    assert viewer_response_data[1]["identifiers"][0]["type"] == "ARK"
    assert viewer_response_data[1]["issue"] == "Admin Issue"
    assert viewer_response_data[1]["last_page"] == "Admin Last Page"
    assert viewer_response_data[1]["number_type"] == "Admin Number Type"
    assert viewer_response_data[1]["number_value"] == "Admin Number Value"
    assert viewer_response_data[1]["publication_year"] == 2013
    assert viewer_response_data[1]["publisher"] == "Admin Publisher"
    assert viewer_response_data[1]["relation_type"] == "Admin Relation Type"
    assert viewer_response_data[1]["titles"][0]["title"] == "Admin Title"
    assert viewer_response_data[1]["titles"][0]["type"] == "AlternativeTitle"
    assert viewer_response_data[1]["type"] == "Admin Type"
    assert viewer_response_data[1]["volume"] == "Admin Volume"
    assert viewer_response_data[2]["contributors"][0]["name"] == "Editor Ndafsdame"
    assert (
        viewer_response_data[2]["contributors"][0]["contributor_type"]
        == "Editor Con Type"
    )
    assert viewer_response_data[2]["contributors"][0]["name_type"] == "Personal"
    assert viewer_response_data[2]["creators"][0]["name"] == "Editor Name"
    assert viewer_response_data[2]["creators"][0]["name_type"] == "Personal"
    assert viewer_response_data[2]["edition"] == "Editor Edition"
    assert viewer_response_data[2]["first_page"] == "Editor First Page"
    assert (
        viewer_response_data[2]["identifiers"][0]["identifier"] == "Editor Identifier"
    )
    assert (
        viewer_response_data[2]["identifiers"][0]["metadata_scheme"]
        == "Editor Metadata Scheme"
    )
    assert (
        viewer_response_data[2]["identifiers"][0]["scheme_type"] == "Editor Scheme Type"
    )
    assert (
        viewer_response_data[2]["identifiers"][0]["scheme_uri"] == "Editor Scheme URI"
    )
    assert viewer_response_data[2]["identifiers"][0]["type"] == "ARK"
    assert viewer_response_data[2]["issue"] == "Editor Issue"
    assert viewer_response_data[2]["last_page"] == "Editor Last Page"
    assert viewer_response_data[2]["number_type"] == "Editor Number Type"
    assert viewer_response_data[2]["number_value"] == "Editor Number Value"
    assert viewer_response_data[2]["publication_year"] == 2013
    assert viewer_response_data[2]["publisher"] == "Editor Publisher"
    assert viewer_response_data[2]["relation_type"] == "Editor Relation Type"
    assert viewer_response_data[2]["titles"][0]["title"] == "Editor Title"
    assert viewer_response_data[2]["titles"][0]["type"] == "Subtitle"
    assert viewer_response_data[2]["type"] == "Editor Type"
    assert viewer_response_data[2]["volume"] == "Editor Volume"


def test_delete_dataset_related_item_contributor_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    related item metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    related_item_id = pytest.global_dataset_related_item_id
    contributor_id = pytest.global_dataset_related_item_contributor_id
    admin_con_id = pytest.global_dataset_related_item_contributor_id_admin
    editor_con_id = pytest.global_dataset_related_item_contributor_id_editor

    # pylint: disable=line-too-long
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/contributor/{contributor_id}"
    )
    # pylint: disable=line-too-long
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/contributor/{contributor_id}"
    )
    # pylint: disable=line-too-long
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/contributor/{admin_con_id}"
    )
    # pylint: disable=line-too-long
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/contributor/{editor_con_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


def test_delete_dataset_related_item_creator_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    related item metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    related_item_id = pytest.global_dataset_related_item_id
    creator_id = pytest.global_dataset_related_item_creator_id
    admin_creator_id = pytest.global_dataset_related_item_creator_id_admin
    editor_creator_id = pytest.global_dataset_related_item_creator_id_editor

    # pylint: disable=line-too-long
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/creator/{creator_id}"
    )
    # pylint: disable=line-too-long
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/creator/{creator_id}"
    )
    # pylint: disable=line-too-long
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/creator/{admin_creator_id}"
    )
    # pylint: disable=line-too-long
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/creator/{editor_creator_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


def test_delete_dataset_related_item_identifier_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    related item metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    related_item_id = pytest.global_dataset_related_item_id
    identifier_id = pytest.global_dataset_related_item_identifier_id
    admin_id_id = pytest.global_dataset_related_item_identifier_id_admin
    editor_id_id = pytest.global_dataset_related_item_identifier_id_editor

    # pylint: disable=line-too-long
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/identifier/{identifier_id}"
    )
    # pylint: disable=line-too-long
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/identifier/{identifier_id}"
    )
    # pylint: disable=line-too-long
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/identifier/{admin_id_id}"
    )
    # pylint: disable=line-too-long
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/identifier/{editor_id_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


def test_delete_dataset_related_item_title_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    related item metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    related_item_id = pytest.global_dataset_related_item_id
    main_title_id = pytest.global_dataset_related_item_main_title_id
    sub_title_id = pytest.global_dataset_related_item_sub_title_id
    admin_t_id = pytest.global_dataset_related_item_title_id_admin
    editor_t_id = pytest.global_dataset_related_item_title_id_editor

    # pylint: disable=line-too-long
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/title/{main_title_id}"
    )
    main_response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/title/{main_title_id}"
    )
    sub_response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/title/{sub_title_id}"
    )
    # pylint: disable=line-too-long
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/title/{admin_t_id}"
    )
    # pylint: disable=line-too-long
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/title/{editor_t_id}"
    )

    assert viewer_response.status_code == 403
    assert main_response.status_code == 403  # Main title cannot be deleted
    assert sub_response.status_code == 204  # Main title cannot be deleted
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


def test_delete_dataset_related_item_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    related item metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    related_item_id = pytest.global_dataset_related_item_id
    admin_ri_id = pytest.global_dataset_related_item_id_admin
    editor_ri_id = pytest.global_dataset_related_item_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{admin_ri_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{editor_ri_id}"
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
            }
        ],
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_rights_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "Identifier"
    assert response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert response_data[0]["rights"] == "Rights"
    assert response_data[0]["uri"] == "URI"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights",
        json=[
            {
                "identifier": "Admin Identifier",
                "identifier_scheme": "Admin Identifier Scheme",
                "rights": "Admin Rights",
                "uri": "Admin URI",
            }
        ],
    )

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_rights_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["identifier"] == "Admin Identifier"
    assert admin_response_data[0]["identifier_scheme"] == "Admin Identifier Scheme"
    assert admin_response_data[0]["rights"] == "Admin Rights"
    assert admin_response_data[0]["uri"] == "Admin URI"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights",
        json=[
            {
                "identifier": "Editor Identifier",
                "identifier_scheme": "Editor Identifier Scheme",
                "rights": "Editor Rights",
                "uri": "Editor URI",
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

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights",
        json=[
            {
                "identifier": "Viewer Identifier",
                "identifier_scheme": "Viewer Identifier Scheme",
                "rights": "Viewer Rights",
                "uri": "Viewer URI",
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
    print("ASDKJL:KJ --------------------------------------")
    print(response_data)
    print("ASDKJL:KJ --------------------------------------")

    assert response_data[0]["identifier"] == "Identifier"
    assert response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert response_data[0]["rights"] == "Rights"
    assert response_data[0]["uri"] == "URI"
    assert response_data[1]["identifier"] == "Admin Identifier"
    assert response_data[1]["identifier_scheme"] == "Admin Identifier Scheme"
    assert response_data[1]["rights"] == "Admin Rights"
    assert response_data[1]["uri"] == "Admin URI"
    assert response_data[2]["identifier"] == "Editor Identifier"
    assert response_data[2]["identifier_scheme"] == "Editor Identifier Scheme"
    assert response_data[2]["rights"] == "Editor Rights"
    assert response_data[2]["uri"] == "Editor URI"

    assert admin_response_data[0]["identifier"] == "Identifier"
    assert admin_response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert admin_response_data[0]["rights"] == "Rights"
    assert admin_response_data[0]["uri"] == "URI"
    assert admin_response_data[1]["identifier"] == "Admin Identifier"
    assert admin_response_data[1]["identifier_scheme"] == "Admin Identifier Scheme"
    assert admin_response_data[1]["rights"] == "Admin Rights"
    assert admin_response_data[1]["uri"] == "Admin URI"
    assert admin_response_data[2]["identifier"] == "Editor Identifier"
    assert admin_response_data[2]["identifier_scheme"] == "Editor Identifier Scheme"
    assert admin_response_data[2]["rights"] == "Editor Rights"
    assert admin_response_data[2]["uri"] == "Editor URI"

    assert editor_response_data[0]["identifier"] == "Identifier"
    assert editor_response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert editor_response_data[0]["rights"] == "Rights"
    assert editor_response_data[0]["uri"] == "URI"
    assert editor_response_data[1]["identifier"] == "Admin Identifier"
    assert editor_response_data[1]["identifier_scheme"] == "Admin Identifier Scheme"
    assert editor_response_data[1]["rights"] == "Admin Rights"
    assert editor_response_data[1]["uri"] == "Admin URI"
    assert editor_response_data[2]["identifier"] == "Editor Identifier"
    assert editor_response_data[2]["identifier_scheme"] == "Editor Identifier Scheme"
    assert editor_response_data[2]["rights"] == "Editor Rights"
    assert editor_response_data[2]["uri"] == "Editor URI"

    assert viewer_response_data[0]["identifier"] == "Identifier"
    assert viewer_response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert viewer_response_data[0]["rights"] == "Rights"
    assert viewer_response_data[0]["uri"] == "URI"
    assert viewer_response_data[1]["identifier"] == "Admin Identifier"
    assert viewer_response_data[1]["identifier_scheme"] == "Admin Identifier Scheme"
    assert viewer_response_data[1]["rights"] == "Admin Rights"
    assert viewer_response_data[1]["uri"] == "Admin URI"
    assert viewer_response_data[2]["identifier"] == "Editor Identifier"
    assert viewer_response_data[2]["identifier_scheme"] == "Editor Identifier Scheme"
    assert viewer_response_data[2]["rights"] == "Editor Rights"
    assert viewer_response_data[2]["uri"] == "Editor URI"


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

    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/rights/{rights_id}"
    )

    assert response.status_code == 204


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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_title_id = response_data[0]["id"]

    assert response_data[0]["title"] == "Owner Title"
    assert response_data[0]["type"] == "Subtitle"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title",
        json=[{"title": "Admin Title", "type": "Subtitle"}],
    )

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
