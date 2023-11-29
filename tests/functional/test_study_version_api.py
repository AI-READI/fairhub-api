# pylint: disable=too-many-lines
"""Tests for the Study Metadata API endpoints"""
import json

import pytest


# ------------------- VERSION ADD ------------------- #
def test_get_version_study_metadata(clients):
    """
    Given a Flask application configured for testing
    WHEN the /study/{study_id}/dataset/{dataset_id}/version/{version_id}/study-metadata
    endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_dataset_version_id  # type: ignore

    _logged_in_client.post(
        f"/study/{study_id}/metadata/arm",
        json=[
            {
                "label": "Label1",
                "type": "Experimental",
                "description": "Arm Description",
                "intervention_list": ["intervention1", "intervention2"],
            }
        ],
    )
    _logged_in_client.post(
        f"/study/{study_id}/metadata/available-ipd",
        json=[
            {
                "identifier": "identifier1",
                "type": "Clinical Study Report",
                "url": "google.com",
                "comment": "comment1",
            }
        ],
    )
    _logged_in_client.post(
        f"/study/{study_id}/metadata/central-contact",
        json=[
            {
                "name": "central-contact",
                "affiliation": "affiliation",
                "role": "role",
                "phone": "808",
                "phone_ext": "909",
                "email_address": "sample@gmail.com",
            }
        ],
    )
    _logged_in_client.post(
        f"/study/{study_id}/metadata/location",
        json=[
            {
                "facility": "test",
                "status": "Withdrawn",
                "city": "city",
                "state": "ca",
                "zip": "test",
                "country": "yes",
            }
        ],
    )
    _logged_in_client.post(
        f"/study/{study_id}/metadata/identification",
        json={
            "primary": {
                "identifier": "test",
                "identifier_type": "test",
                "identifier_domain": "domain",
                "identifier_link": "link",
            },
            "secondary": [
                {
                    "identifier": "test",
                    "identifier_type": "test",
                    "identifier_domain": "dodfasdfmain",
                    "identifier_link": "link",
                }
            ],
        },
    )
    _logged_in_client.post(
        f"/study/{study_id}/metadata/intervention",
        json=[
            {
                "type": "Device",
                "name": "name test",
                "description": "desc",
                "arm_group_label_list": ["test", "one"],
                "other_name_list": ["uhh", "yes"],
            }
        ],
    )
    _logged_in_client.post(
        f"/study/{study_id}/metadata/link",
        json=[{"url": "google.com", "title": "google link"}],
    )
    _logged_in_client.post(
        f"/study/{study_id}/metadata/overall-official",
        json=[{"name": "test", "affiliation": "aff", "role": "Study Chair"}],
    )
    _logged_in_client.post(
        f"/study/{study_id}/metadata/reference",
        json=[
            {
                "identifier": "reference identifier",
                "type": "Yes",
                "citation": "reference citation",
            }
        ],
    )

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/study-metadata"
    )
    response_data = json.loads(response.data)
    # print(response_data)
    assert response.status_code == 200
    assert response_data["available_ipd"][0]["identifier"] == "identifier1"
    assert response_data["available_ipd"][0]["url"] == "google.com"
    assert response_data["arms"][0]["label"] == "Label1"

    assert response_data["contacts"][0]["name"] == "central-contact"
    assert response_data["contacts"][0]["affiliation"] == "affiliation"

    assert response_data["secondary_identifiers"][0]["identifier"] == "test"
    assert response_data["secondary_identifiers"][0]["identifier_type"] == "test"
    assert response_data["interventions"][0]["type"] == "Device"
    assert response_data["interventions"][0]["name"] == "name test"
    assert response_data["links"][0]["title"] == "google link"
    assert response_data["links"][0]["url"] == "google.com"
    assert response_data["locations"][0]["country"] == "yes"
    assert response_data["locations"][0]["facility"] == "test"
    assert response_data["overall_officials"][0]["name"] == "test"
    assert response_data["overall_officials"][0]["role"] == "Study Chair"
    assert response_data["overall_officials"][0]["affiliation"] == "aff"
    assert response_data["references"][0]["identifier"] == "reference identifier"
    assert response_data["references"][0]["citation"] == "reference citation"

    assert response_data["description"]["brief_summary"] == "editor-brief_summary"
    assert response_data["design"]["design_allocation"] == "editor-dfasdfasd"

    assert response_data["design"]["study_type"] == "Interventional"
    assert response_data["design"]["design_intervention_model"] == "Treatment"
    assert response_data["design"]["design_primary_purpose"] == "Parallel Assignment"
    assert response_data["design"]["design_masking"] == "Double"
    assert response_data["design"]["design_masking_description"] == "tewsfdasf"
    assert response_data["design"]["design_who_masked_list"] == [
        "Participant",
        "Care Provider",
    ]
    assert response_data["design"]["phase_list"] == ["N/A"]
    assert response_data["design"]["enrollment_count"] == 3
    assert response_data["design"]["enrollment_type"] == "Actual"
    assert response_data["design"]["number_arms"] == 2
    assert response_data["design"]["design_observational_model_list"] == [
        "Cohort",
        "Case-Control",
    ]
    assert response_data["design"]["design_time_perspective_list"] == ["Other"]
    assert response_data["design"]["bio_spec_retention"] == "None Retained"
    assert response_data["design"]["target_duration"] == "rewrwe"
    assert response_data["design"]["number_groups_cohorts"] == 1
    assert response_data["eligibility"]["gender"] == "All"
    assert response_data["eligibility"]["gender_based"] == "Yes"
    assert response_data["eligibility"]["minimum_age_value"] == 18
    assert response_data["primary_identifier"]["identifier"] == "test"
    assert response_data["primary_identifier"]["identifier_type"] == "test"
    assert response_data["status"]["overall_status"] == "Withdrawn"
    assert response_data["status"]["start_date"] == "2023-11-15 00:00:00"
    assert (
        response_data["sponsors"]["responsible_party_investigator_name"]
        == "editor sponsor name"
    )
    assert response_data["sponsors"]["responsible_party_type"] == "Sponsor"
    assert response_data["sponsors"]["lead_sponsor_name"] == "editor sponsor name"
    assert response_data["collaborators"] == ["editor-collaborator1123"]
    assert response_data["conditions"] == [
        "true",
        "editor-conditions string",
        "editor-keywords string",
        "editor-size string",
    ]

    assert response_data["ipd_sharing"]["ipd_sharing"] == "Yes"
    assert response_data["ipd_sharing"]["ipd_sharing_info_type_list"] == [
        "Study Protocol",
        "Analytical Code",
    ]

    assert response_data["oversight"] is True


def test_get_version_dataset_metadata(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/dataset-metadata'
    endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_dataset_version_id  # type: ignore

    contributor_response = _logged_in_client.post(
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
    creator_response = _logged_in_client.post(
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

    date_response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date",
        json=[{"date": 20210101, "type": "Type", "information": "Info"}],
    )
    funder_response = _logged_in_client.post(
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
    rights_response = _logged_in_client.post(
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
    subject_response = _logged_in_client.post(
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
    alt_identifier_response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "identifier test",
                "type": "ARK",
            }
        ],
    )
    related_item_response = _logged_in_client.post(
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
    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/dataset-metadata"
    )

    assert contributor_response.status_code == 201
    assert creator_response.status_code == 201
    assert date_response.status_code == 201
    assert funder_response.status_code == 201
    assert rights_response.status_code == 201
    assert subject_response.status_code == 201
    assert alt_identifier_response.status_code == 201
    assert related_item_response.status_code == 201
    assert response.status_code == 200
    response_data = json.loads(response.data)

    # seach for main title index in response_data[n]["titles"]
    # pylint: disable=line-too-long
    main_title_0 = next(
        (
            index
            for (index, d) in enumerate(response_data["related_items"][0]["titles"])
            if d["type"] == "MainTitle"
        ),
        None,
    )
    # seach for subtitle index in response_data["related_items"][0]["titles"]
    sub_title_0 = next(
        (
            index
            for (index, d) in enumerate(response_data["related_items"][0]["titles"])
            if d["type"] == "Subtitle"
        ),
        None,
    )

    assert response_data["contributors"][0]["name"] == "Name here"
    assert response_data["contributors"][0]["name_type"] == "Personal"
    assert response_data["contributors"][0]["contributor_type"] == "Con Type"
    assert response_data["dates"][0]["date"] == "01-01-1970"
    assert response_data["dates"][0]["type"] == "Type"
    assert response_data["creators"][0]["name"] == "Name here"
    assert response_data["creators"][0]["name_type"] == "Personal"
    assert response_data["funders"][0]["name"] == "Admin Name"
    assert response_data["funders"][0]["identifier"] == "Identifier"
    assert response_data["rights"][0]["identifier"] == "Admin Identifier"
    assert response_data["rights"][0]["rights"] == "Admin Rights"
    assert response_data["subjects"][0]["subject"] == "Subject"
    assert response_data["about"]["language"] == "English"

    assert response_data["about"]["resource_type"] == "Editor Resource Type"
    assert response_data["about"]["size"] == ["Size"]
    assert response_data["access"]["type"] == "editor type"
    assert response_data["access"]["description"] == "editor description"
    assert response_data["consent"]["noncommercial"] is True
    assert response_data["consent"]["geog_restrict"] is True
    assert response_data["consent"]["research_type"] is True
    assert response_data["de_identification"]["direct"] is True
    assert response_data["de_identification"]["type"] == "Level"
    assert response_data["publisher"]["publisher"] == "Publisher"
    assert (
        response_data["publisher"]["managing_organization_name"]
        == "Managing Editor Organization Name"
    )

    assert response_data["identifiers"][0]["identifier"] == "identifier test"
    assert response_data["identifiers"][0]["type"] == "ARK"
    assert response_data["related_items"][0]["publication_year"] == "1970"
    assert response_data["related_items"][0]["publisher"] == "Publisher"
    assert response_data["related_items"][0]["contributors"][0]["name"] == "Ndafsdame"
    assert (
        response_data["related_items"][0]["contributors"][0]["contributor_type"]
        == "Con Type"
    )
    assert response_data["related_items"][0]["creators"][0]["name"] == "Name"
    assert response_data["related_items"][0]["creators"][0]["name_type"] == "Personal"
    assert response_data["related_items"][0]["titles"][main_title_0]["title"] == "Title"
    assert (
        response_data["related_items"][0]["titles"][main_title_0]["type"] == "MainTitle"
    )
    assert response_data["related_items"][0]["titles"][sub_title_0]["title"] == "Title"
    assert (
        response_data["related_items"][0]["titles"][sub_title_0]["type"] == "Subtitle"
    )
    assert (
        response_data["related_items"][0]["identifiers"][0]["identifier"]
        == "Identifier"
    )
    assert response_data["related_items"][0]["identifiers"][0]["type"] == "ARK"
    assert response_data["related_items"][0]["type"] == "Type"


def test_get_version_readme(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/readme'
    endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_dataset_version_id  # type: ignore

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme"
    )

    assert response.status_code == 200


def test_put_version_readme(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/readme'
    endpoint is requested (PUT)
    THEN check that the response is valid and retrieves the design metadata
    """
    # create a new dataset and delete it afterwards
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_dataset_version_id  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme",
        json={"readme": "readme test"},
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["readme"] == "readme test"


def test_put_version_changelog(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/changelog'
    endpoint is requested (PUT)
    THEN check that the response is valid and retrieves the design metadata
    """
    # create a new dataset and delete it afterwards
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_dataset_version_id  # type: ignore
    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog",
        json={"changelog": "changelog test"},
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data == "changelog test"


def test_get_version_changelog(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/study/<study_id>/dataset/<dataset_id>/version/<version_id>/changelog'
    endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id  # type: ignore
    version_id = pytest.global_dataset_version_id  # type: ignore

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog"
    )

    assert response.status_code == 200
