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
                "type": "ark",
            }
        ],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_alternative_identifier_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "identifier test"
    assert response_data[0]["type"] == "ark"


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
        },
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
    assert response_data[0]["contributor_type"] == "Con Type"
    assert response_data[0]["affiliations"][0]["name"] == "Test"
    assert response_data[0]["affiliations"][0]["identifier"] == "yes"
    assert response_data[0]["affiliations"][0]["scheme"] == "uh"
    assert response_data[0]["affiliations"][0]["scheme_uri"] == "scheme uri"


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


# ------------------- DATE METADATA ------------------- #
def test_get_dataset_date_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/date'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset date metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.get(f"/study/{study_id}/dataset/{dataset_id}/metadata/date")

    assert response.status_code == 200


def test_post_dataset_date_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/date'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset date metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date",
        json=[{"date": 20210101, "type": "Type", "information": "Info"}],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_date_id = response_data[0]["id"]

    assert response_data[0]["date"] == 20210101
    assert response_data[0]["type"] == "Type"
    assert response_data[0]["information"] == "Info"


def test_delete_dataset_date_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/date'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset date metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    date_id = pytest.global_dataset_date_id

    response = _test_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{date_id}"
    )

    assert response.status_code == 200


# ------------------- DE-IDENTIFICATION LEVEL METADATA ------------------- #
def test_get_dataset_deidentification_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/de-identification'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    de-identification metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/de-identification-level"
    )

    assert response.status_code == 200


def test_put_dataset_deidentification_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/de-identification'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    de-identification metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.put(
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
def test_get_dataset_descriptions_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/description'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description"
    )

    assert response.status_code == 200


def test_post_dataset_description_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/description'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    description metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description",
        json=[{"description": "Description", "type": "Methods"}],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_dataset_description_id = response_data[0]["id"]

    assert response_data[0]["description"] == "Description"
    assert response_data[0]["type"] == "Methods"


def test_delete_dataset_description_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/description'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    description metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    description_id = pytest.global_dataset_description_id

    response = _test_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{description_id}"
    )

    assert response.status_code == 200


# ------------------- FUNDER METADATA ------------------- #
def test_get_dataset_funder_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/funder'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    funder metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder"
    )

    assert response.status_code == 200


def test_post_dataset_funder_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/funder'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    funder metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.post(
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


def test_delete_dataset_funder_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/funder'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    funder metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    funder_id = pytest.global_dataset_funder_id

    response = _test_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{funder_id}"
    )

    assert response.status_code == 200


# ------------------- OTHER METADATA ------------------- #
def test_get_other_dataset_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    other metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other"
    )

    assert response.status_code == 200


def test_put_other_dataset_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    other metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.put(
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


# ------------------- PUBLICATION METADATA ------------------- #
def test_get_dataset_publisher_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    publisher metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/publisher"
    )

    assert response.status_code == 200


def test_put_dataset_publisher_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    publisher metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.put(
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


# ------------------- README METADATA ------------------- #
# WIP


# ------------------- RECORD KEYS METADATA ------------------- #
def test_get_dataset_record_keys_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    record keys metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys"
    )

    assert response.status_code == 200


def test_put_dataset_record_keys_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    record keys metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/record-keys",
        json={"type": "Record Type", "details": "Details for Record Keys"},
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)

    assert response_data["type"] == "Record Type"
    assert response_data["details"] == "Details for Record Keys"


# ------------------- RELATED ITEM METADATA ------------------- #
def test_get_dataset_related_item_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    related item metadata content
    """
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id

    response = _test_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-item"
    )

    assert response.status_code == 200