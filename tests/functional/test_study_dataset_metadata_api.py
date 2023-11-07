"""Tests for the Dataset's Metadata API endpoints"""
import json

import pytest


# ------------------- ACCESS METADATA ------------------- #
def test_get_dataset_access_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/access' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset access metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access"
    )
    assert response.status_code == 200


def test_put_dataset_access_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/access' endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset access metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    response = _test_client.put(
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


# ------------------- ALTERNATIVE IDENTIFIER METADATA ------------------- #
def test_post_alternative_identifier(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset alternative identifier
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    response = _test_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "identifier test",
                "type": "type test",
            }
        ],
    )

    assert response.status_code == 200

    response_data = json.loads(response.data)
    pytest.global_alternative_identifier_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "identifier test"
    assert response_data[0]["type"] == "type test"


def test_get_alternative_identifier(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset alternative identifier content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )
    assert response.status_code == 200


def test_delete_alternative_identifier(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset alternative identifier content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    identifier_id = pytest.global_alternative_identifier_id
    response = _test_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{identifier_id}"
    )

    assert response.status_code == 200


# ------------------- CONSENT METADATA ------------------- #
def test_get_dataset_consent_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/consent' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset consent metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/consent"
    )
    assert response.status_code == 200


def test_put_dataset_consent_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/consent' endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset consent metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    response = _test_client.put(
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


# ------------------- CONTRIBUTOR METADATA ------------------- #
def test_post_dataset_contributor_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/contributor'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset contributor metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    response = _test_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor",
        json=[{
            "name": "Name here",
            "name_type": "Name type",
            "name_identifier": "Name identifier",
            "name_identifier_scheme": "Name Scheme ID",
            "name_identifier_scheme_uri": "Name ID Scheme URI",
            "creator": False,
            "contributor_type": "Con Type",
            "affiliations": {
                "leader": True,
                "type": "CEO"
            }
        }],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_contributor_id = response_data[0]["id"]

    assert response_data[0]["name"] == "Name here"
    assert response_data[0]["name_type"] == "Name type"
    assert response_data[0]["name_identifier"] == "Name identifier"
    assert response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert response_data[0]["creator"] is False
    assert response_data[0]["contributor_type"] == "Con Type"
    assert response_data[0]["affiliations"]["leader"] is True
    assert response_data[0]["affiliations"]["type"] == "CEO"


def test_get_dataset_contributor_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/contributor'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset contributor metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor"
    )
    assert response.status_code == 200


def test_delete_dataset_contributor_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/contributor'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset contributor metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    contributor_id = pytest.global_dataset_contributor_id
    response = _test_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor/{contributor_id}"
    )

    assert response.status_code == 200


# ------------------- CREATOR METADATA ------------------- #
def test_get_dataset_creator_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/creator' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset creator metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator"
    )

    assert response.status_code == 200


def test_post_dataset_creator_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/creator' endpoint is requested (POST)
    Then check that the response is valid and creates the dataset creator metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator",
        json={
            "name": "Name here",
            "name_type": "Name type",
            "name_identifier": "Name identifier",
            "name_identifier_scheme": "Name Scheme ID",
            "name_identifier_scheme_uri": "Name ID Scheme URI",
            "creator": True,
            "contributor_type": "Con Type",
            "affiliations": {
                "leader": True,
                "type": "CEO"
            }
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_creator_id = response_data[0]["id"]

    assert response_data[0]["name"] == "Name here"
    assert response_data[0]["name_type"] == "Name type"
    assert response_data[0]["name_identifier"] == "Name identifier"
    assert response_data[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert response_data[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert response_data[0]["creator"] is True
    assert response_data[0]["contributor_type"] == "Con Type"
    assert response_data[0]["affiliations"]["leader"] is True
    assert response_data[0]["affiliations"]["type"] == "CEO"


def test_delete_dataset_creator_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/creator'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset creator metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    creator_id = pytest.global_dataset_creator_id

    response = _test_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{creator_id}"
    )

    assert response.status_code == 200
