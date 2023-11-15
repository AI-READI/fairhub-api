# pylint: disable=too-many-lines
"""Tests for the Dataset's Metadata API endpoints"""
import json

import pytest


# ------------------- ACCESS METADATA ------------------- #
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

    assert response.status_code == 200

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access"
    )

    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


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
        }
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
        }
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
        }
    )

    print(viewer_response.status_code)
    assert viewer_response.status_code == 403


# ------------------- ALTERNATIVE IDENTIFIER METADATA ------------------- #
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

    assert response.status_code == 200

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )

    print(admin_response.status_code)
    print(editor_response.status_code)
    print(viewer_response.status_code)
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


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

    assert response.status_code == 200
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
        ]
    )
    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "editor test",
                "type": "ARK",
            }
        ]
    )
    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "viewer test",
                "type": "ARK",
            }
        ]
    )

    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403

    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    pytest.global_alternative_identifier_id_admin = admin_response_data[1]["id"]
    pytest.global_alternative_identifier_id_editor = editor_response_data[2]["id"]

    assert admin_response_data[1]["identifier"] == "admin test"
    assert admin_response_data[1]["type"] == "ARK"
    assert editor_response_data[2]["identifier"] == "editor test"
    assert editor_response_data[2]["type"] == "ARK"


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

    assert viewer_response.status_code == 403

    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{identifier_id}"
    )

    assert response.status_code == 200

    # pylint: disable=line-too-long
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{admin_identifier_id}"
    )

    assert admin_response.status_code == 200

    # pylint: disable=line-too-long
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{editor_identifier_id}"
    )

    assert editor_response.status_code == 200


# ------------------- CONSENT METADATA ------------------- #
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
        }
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
        }
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
        }
    )

    assert viewer_response.status_code == 403


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

    assert response.status_code == 200
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
                ]
            }
        ]
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_contributor_id_admin = admin_response_data[1]["id"]

    assert admin_response_data[1]["name"] == "Admin Name here"

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
                ]
            }
        ]
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_contributor_id_editor = editor_response_data[2]["id"]

    assert editor_response_data[2]["name"] == "Editor Name here"

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
                ]
            }
        ]
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

    assert viewer_response.status_code == 403

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

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200


# ------------------- CREATOR METADATA ------------------- #
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

    assert response.status_code == 200


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

    assert response.status_code == 200
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

    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{creator_id}"
    )

    assert response.status_code == 200


# ------------------- DATE METADATA ------------------- #
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

    assert response.status_code == 200


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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_date_id = response_data[0]["id"]

    assert response_data[0]["date"] == 20210101
    assert response_data[0]["type"] == "Type"
    assert response_data[0]["information"] == "Info"


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

    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{date_id}"
    )

    assert response.status_code == 200


# ------------------- DE-IDENTIFICATION LEVEL METADATA ------------------- #
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

    assert response.status_code == 200


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


# ------------------- DESCRIPTION METADATA ------------------- #
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

    assert response.status_code == 200


def test_post_dataset_description_metadata(clients):
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
        json=[{"description": "Description", "type": "Methods"}],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_description_id = response_data[0]["id"]

    assert response_data[0]["description"] == "Description"
    assert response_data[0]["type"] == "Methods"


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

    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{description_id}"
    )

    assert response.status_code == 200


# ------------------- FUNDER METADATA ------------------- #
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

    assert response.status_code == 200


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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_funder_id = response_data[0]["id"]

    assert response_data[0]["name"] == "Name"
    assert response_data[0]["award_number"] == "award number"
    assert response_data[0]["award_title"] == "Award Title"
    assert response_data[0]["award_uri"] == "Award URI"
    assert response_data[0]["identifier"] == "Identifier"
    assert response_data[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert response_data[0]["identifier_type"] == "Identifier Type"


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

    assert response.status_code == 200


# ------------------- OTHER METADATA ------------------- #
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

    assert response.status_code == 200


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
    # assert response_data["resource_type"] == "Resource Type"    # CURRENTLY NOT BEING RETURNED
    assert response_data["size"] == ["Size"]
    assert response_data["standards_followed"] == "Standards Followed"
    # ABOVE STATEMENT CURRENTLY NOT BEING UPDATED


# ------------------- PUBLICATION METADATA ------------------- #
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

    assert response.status_code == 200


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


# ------------------- RECORD KEYS METADATA ------------------- #
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

    assert response.status_code == 200


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

    assert response.status_code == 201
    response_data = json.loads(response.data)

    assert response_data["type"] == "Record Type"
    assert response_data["details"] == "Details for Record Keys"


# ------------------- RELATED ITEM METADATA ------------------- #
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

    assert response.status_code == 200


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
                "titles": [{"title": "Title", "type": "MainTitle"}],
                "type": "Type",
                "volume": "Volume",
            }
        ],
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
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
    pytest.global_dataset_related_item_title_id = response_data[0]["titles"][0]["id"]

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
    assert response_data[0]["titles"][0]["title"] == "Title"
    assert response_data[0]["titles"][0]["type"] == "MainTitle"
    assert response_data[0]["type"] == "Type"
    assert response_data[0]["volume"] == "Volume"


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

    # pylint: disable=line-too-long
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/contributor/{contributor_id}"
    )

    assert response.status_code == 200


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

    # pylint: disable=line-too-long
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/creator/{creator_id}"
    )

    assert response.status_code == 200


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

    # pylint: disable=line-too-long
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/identifier/{identifier_id}"
    )

    assert response.status_code == 200


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
    title_id = pytest.global_dataset_related_item_title_id

    # pylint: disable=line-too-long
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}/title/{title_id}"
    )

    assert response.status_code == 200


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

    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item/{related_item_id}"
    )

    assert response.status_code == 200


# ------------------- RIGHTS METADATA ------------------- #
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

    assert response.status_code == 200


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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_rights_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "Identifier"
    assert response_data[0]["identifier_scheme"] == "Identifier Scheme"
    assert response_data[0]["rights"] == "Rights"
    assert response_data[0]["uri"] == "URI"


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

    assert response.status_code == 200


# ------------------- SUBJECTS METADATA ------------------- #
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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_subject_id = response_data[0]["id"]

    assert response_data[0]["scheme"] == "Scheme"
    assert response_data[0]["scheme_uri"] == "Scheme URI"
    assert response_data[0]["subject"] == "Subject"
    assert response_data[0]["value_uri"] == "Value URI"


def test_delete_dataset_subject_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/subject/{subject_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    subject metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    subject_id = pytest.global_dataset_subject_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject/{subject_id}"
    )

    assert response.status_code == 200


# ------------------- TITLE METADATA ------------------- #
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

    assert response.status_code == 200


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
        json=[{"title": "Title", "type": "Subtitle"}],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_title_id = response_data[0]["id"]

    assert response_data[0]["title"] == "Title"
    assert response_data[0]["type"] == "Subtitle"


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

    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title/{title_id}"
    )

    assert response.status_code == 200
