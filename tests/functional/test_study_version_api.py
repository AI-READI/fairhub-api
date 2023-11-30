# pylint: disable=too-many-lines
"""Tests for the Study Metadata API endpoints"""
import json

import pytest


# ------------------- VERSION ADD ------------------- #
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

    arm_response = _logged_in_client.post(
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
    avail_ipd_response = _logged_in_client.post(
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
    cc_response = _logged_in_client.post(
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
    location_response = _logged_in_client.post(
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
    id_response = _logged_in_client.post(
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
    intervention_response = _logged_in_client.post(
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
    link_response = _logged_in_client.post(
        f"/study/{study_id}/metadata/link",
        json=[{"url": "google.com", "title": "google link"}],
    )
    of_response = _logged_in_client.post(
        f"/study/{study_id}/metadata/overall-official",
        json=[{"name": "test", "affiliation": "aff", "role": "Study Chair"}],
    )
    reference_response = _logged_in_client.post(
        f"/study/{study_id}/metadata/reference",
        json=[
            {
                "identifier": "reference identifier",
                "type": "Yes",
                "citation": "reference citation",
            }
        ],
    )

    assert arm_response.status_code == 201
    assert avail_ipd_response.status_code == 201
    assert cc_response.status_code == 201
    assert location_response.status_code == 201
    assert id_response.status_code == 201
    assert intervention_response.status_code == 201
    assert link_response.status_code == 201
    assert of_response.status_code == 201
    assert reference_response.status_code == 201

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/study-metadata"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/study-metadata"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/study-metadata"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/study-metadata"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403
    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)

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

    assert admin_response_data["available_ipd"][0]["identifier"] == "identifier1"
    assert admin_response_data["available_ipd"][0]["url"] == "google.com"
    assert admin_response_data["arms"][0]["label"] == "Label1"

    assert admin_response_data["contacts"][0]["name"] == "central-contact"
    assert admin_response_data["contacts"][0]["affiliation"] == "affiliation"

    assert admin_response_data["secondary_identifiers"][0]["identifier"] == "test"
    assert admin_response_data["secondary_identifiers"][0]["identifier_type"] == "test"
    assert admin_response_data["interventions"][0]["type"] == "Device"
    assert admin_response_data["interventions"][0]["name"] == "name test"
    assert admin_response_data["links"][0]["title"] == "google link"
    assert admin_response_data["links"][0]["url"] == "google.com"
    assert admin_response_data["locations"][0]["country"] == "yes"
    assert admin_response_data["locations"][0]["facility"] == "test"
    assert admin_response_data["overall_officials"][0]["name"] == "test"
    assert admin_response_data["overall_officials"][0]["role"] == "Study Chair"
    assert admin_response_data["overall_officials"][0]["affiliation"] == "aff"
    assert admin_response_data["references"][0]["identifier"] == "reference identifier"
    assert admin_response_data["references"][0]["citation"] == "reference citation"

    assert admin_response_data["description"]["brief_summary"] == "editor-brief_summary"
    assert admin_response_data["design"]["design_allocation"] == "editor-dfasdfasd"

    assert admin_response_data["design"]["study_type"] == "Interventional"
    assert admin_response_data["design"]["design_intervention_model"] == "Treatment"
    assert (
        admin_response_data["design"]["design_primary_purpose"] == "Parallel Assignment"
    )
    assert admin_response_data["design"]["design_masking"] == "Double"
    assert admin_response_data["design"]["design_masking_description"] == "tewsfdasf"
    assert admin_response_data["design"]["design_who_masked_list"] == [
        "Participant",
        "Care Provider",
    ]
    assert admin_response_data["design"]["phase_list"] == ["N/A"]
    assert admin_response_data["design"]["enrollment_count"] == 3
    assert admin_response_data["design"]["enrollment_type"] == "Actual"
    assert admin_response_data["design"]["number_arms"] == 2
    assert admin_response_data["design"]["design_observational_model_list"] == [
        "Cohort",
        "Case-Control",
    ]
    assert admin_response_data["design"]["design_time_perspective_list"] == ["Other"]
    assert admin_response_data["design"]["bio_spec_retention"] == "None Retained"
    assert admin_response_data["design"]["target_duration"] == "rewrwe"
    assert admin_response_data["design"]["number_groups_cohorts"] == 1
    assert admin_response_data["eligibility"]["gender"] == "All"
    assert admin_response_data["eligibility"]["gender_based"] == "Yes"
    assert admin_response_data["eligibility"]["minimum_age_value"] == 18
    assert admin_response_data["primary_identifier"]["identifier"] == "test"
    assert admin_response_data["primary_identifier"]["identifier_type"] == "test"
    assert admin_response_data["status"]["overall_status"] == "Withdrawn"
    assert admin_response_data["status"]["start_date"] == "2023-11-15 00:00:00"
    assert (
        admin_response_data["sponsors"]["responsible_party_investigator_name"]
        == "editor sponsor name"
    )
    assert admin_response_data["sponsors"]["responsible_party_type"] == "Sponsor"
    assert admin_response_data["sponsors"]["lead_sponsor_name"] == "editor sponsor name"
    assert admin_response_data["collaborators"] == ["editor-collaborator1123"]
    assert admin_response_data["conditions"] == [
        "true",
        "editor-conditions string",
        "editor-keywords string",
        "editor-size string",
    ]

    assert admin_response_data["ipd_sharing"]["ipd_sharing"] == "Yes"
    assert admin_response_data["ipd_sharing"]["ipd_sharing_info_type_list"] == [
        "Study Protocol",
        "Analytical Code",
    ]

    assert admin_response_data["oversight"] is True

    assert editor_response_data["available_ipd"][0]["identifier"] == "identifier1"
    assert editor_response_data["available_ipd"][0]["url"] == "google.com"
    assert editor_response_data["arms"][0]["label"] == "Label1"

    assert editor_response_data["contacts"][0]["name"] == "central-contact"
    assert editor_response_data["contacts"][0]["affiliation"] == "affiliation"

    assert editor_response_data["secondary_identifiers"][0]["identifier"] == "test"
    assert editor_response_data["secondary_identifiers"][0]["identifier_type"] == "test"
    assert editor_response_data["interventions"][0]["type"] == "Device"
    assert editor_response_data["interventions"][0]["name"] == "name test"
    assert editor_response_data["links"][0]["title"] == "google link"
    assert editor_response_data["links"][0]["url"] == "google.com"
    assert editor_response_data["locations"][0]["country"] == "yes"
    assert editor_response_data["locations"][0]["facility"] == "test"
    assert editor_response_data["overall_officials"][0]["name"] == "test"
    assert editor_response_data["overall_officials"][0]["role"] == "Study Chair"
    assert editor_response_data["overall_officials"][0]["affiliation"] == "aff"
    assert editor_response_data["references"][0]["identifier"] == "reference identifier"
    assert editor_response_data["references"][0]["citation"] == "reference citation"

    assert (
        editor_response_data["description"]["brief_summary"] == "editor-brief_summary"
    )
    assert editor_response_data["design"]["design_allocation"] == "editor-dfasdfasd"

    assert editor_response_data["design"]["study_type"] == "Interventional"
    assert editor_response_data["design"]["design_intervention_model"] == "Treatment"
    assert (
        editor_response_data["design"]["design_primary_purpose"]
        == "Parallel Assignment"
    )
    assert editor_response_data["design"]["design_masking"] == "Double"
    assert editor_response_data["design"]["design_masking_description"] == "tewsfdasf"
    assert editor_response_data["design"]["design_who_masked_list"] == [
        "Participant",
        "Care Provider",
    ]
    assert editor_response_data["design"]["phase_list"] == ["N/A"]
    assert editor_response_data["design"]["enrollment_count"] == 3
    assert editor_response_data["design"]["enrollment_type"] == "Actual"
    assert editor_response_data["design"]["number_arms"] == 2
    assert editor_response_data["design"]["design_observational_model_list"] == [
        "Cohort",
        "Case-Control",
    ]
    assert editor_response_data["design"]["design_time_perspective_list"] == ["Other"]
    assert editor_response_data["design"]["bio_spec_retention"] == "None Retained"
    assert editor_response_data["design"]["target_duration"] == "rewrwe"
    assert editor_response_data["design"]["number_groups_cohorts"] == 1
    assert editor_response_data["eligibility"]["gender"] == "All"
    assert editor_response_data["eligibility"]["gender_based"] == "Yes"
    assert editor_response_data["eligibility"]["minimum_age_value"] == 18
    assert editor_response_data["primary_identifier"]["identifier"] == "test"
    assert editor_response_data["primary_identifier"]["identifier_type"] == "test"
    assert editor_response_data["status"]["overall_status"] == "Withdrawn"
    assert editor_response_data["status"]["start_date"] == "2023-11-15 00:00:00"
    assert (
        editor_response_data["sponsors"]["responsible_party_investigator_name"]
        == "editor sponsor name"
    )
    assert editor_response_data["sponsors"]["responsible_party_type"] == "Sponsor"
    assert (
        editor_response_data["sponsors"]["lead_sponsor_name"] == "editor sponsor name"
    )
    assert editor_response_data["collaborators"] == ["editor-collaborator1123"]
    assert editor_response_data["conditions"] == [
        "true",
        "editor-conditions string",
        "editor-keywords string",
        "editor-size string",
    ]

    assert editor_response_data["ipd_sharing"]["ipd_sharing"] == "Yes"
    assert editor_response_data["ipd_sharing"]["ipd_sharing_info_type_list"] == [
        "Study Protocol",
        "Analytical Code",
    ]

    assert editor_response_data["oversight"] is True


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

    assert contributor_response.status_code == 201
    assert creator_response.status_code == 201
    assert date_response.status_code == 201
    assert funder_response.status_code == 201
    assert rights_response.status_code == 201
    assert subject_response.status_code == 201
    assert alt_identifier_response.status_code == 201
    assert related_item_response.status_code == 201

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/dataset-metadata"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/dataset-metadata"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/dataset-metadata"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/dataset-metadata"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403
    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)

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
    a_main_title_0 = next(
        (
            index
            for (index, d) in enumerate(
                admin_response_data["related_items"][0]["titles"]
            )
            if d["type"] == "MainTitle"
        ),
        None,
    )
    a_sub_title_0 = next(
        (
            index
            for (index, d) in enumerate(
                admin_response_data["related_items"][0]["titles"]
            )
            if d["type"] == "Subtitle"
        ),
        None,
    )
    e_main_title_0 = next(
        (
            index
            for (index, d) in enumerate(
                editor_response_data["related_items"][0]["titles"]
            )
            if d["type"] == "MainTitle"
        ),
        None,
    )
    e_sub_title_0 = next(
        (
            index
            for (index, d) in enumerate(
                editor_response_data["related_items"][0]["titles"]
            )
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
    assert response_data["funders"][0]["name"] == "Name"
    assert response_data["funders"][0]["identifier"] == "Identifier"
    assert response_data["rights"][0]["identifier"] == "Identifier"
    assert response_data["rights"][0]["rights"] == "Rights"
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

    assert admin_response_data["contributors"][0]["name"] == "Name here"
    assert admin_response_data["contributors"][0]["name_type"] == "Personal"
    assert admin_response_data["contributors"][0]["contributor_type"] == "Con Type"
    assert admin_response_data["dates"][0]["date"] == "01-01-1970"
    assert admin_response_data["dates"][0]["type"] == "Type"
    assert admin_response_data["creators"][0]["name"] == "Name here"
    assert admin_response_data["creators"][0]["name_type"] == "Personal"
    assert admin_response_data["funders"][0]["name"] == "Name"
    assert admin_response_data["funders"][0]["identifier"] == "Identifier"
    assert admin_response_data["rights"][0]["identifier"] == "Identifier"
    assert admin_response_data["rights"][0]["rights"] == "Rights"
    assert admin_response_data["subjects"][0]["subject"] == "Subject"
    assert admin_response_data["about"]["language"] == "English"

    assert admin_response_data["about"]["resource_type"] == "Editor Resource Type"
    assert admin_response_data["about"]["size"] == ["Size"]
    assert admin_response_data["access"]["type"] == "editor type"
    assert admin_response_data["access"]["description"] == "editor description"
    assert admin_response_data["consent"]["noncommercial"] is True
    assert admin_response_data["consent"]["geog_restrict"] is True
    assert admin_response_data["consent"]["research_type"] is True
    assert admin_response_data["de_identification"]["direct"] is True
    assert admin_response_data["de_identification"]["type"] == "Level"
    assert admin_response_data["publisher"]["publisher"] == "Publisher"
    assert (
        admin_response_data["publisher"]["managing_organization_name"]
        == "Managing Editor Organization Name"
    )

    assert admin_response_data["identifiers"][0]["identifier"] == "identifier test"
    assert admin_response_data["identifiers"][0]["type"] == "ARK"
    assert admin_response_data["related_items"][0]["publication_year"] == "1970"
    assert admin_response_data["related_items"][0]["publisher"] == "Publisher"
    assert (
        admin_response_data["related_items"][0]["contributors"][0]["name"]
        == "Ndafsdame"
    )
    assert (
        admin_response_data["related_items"][0]["contributors"][0]["contributor_type"]
        == "Con Type"
    )
    assert admin_response_data["related_items"][0]["creators"][0]["name"] == "Name"
    assert (
        admin_response_data["related_items"][0]["creators"][0]["name_type"]
        == "Personal"
    )
    assert (
        admin_response_data["related_items"][0]["titles"][a_main_title_0]["title"]
        == "Title"
    )
    assert (
        admin_response_data["related_items"][0]["titles"][a_main_title_0]["type"]
        == "MainTitle"
    )
    assert (
        admin_response_data["related_items"][0]["titles"][a_sub_title_0]["title"]
        == "Title"
    )
    assert (
        admin_response_data["related_items"][0]["titles"][a_sub_title_0]["type"]
        == "Subtitle"
    )
    assert (
        admin_response_data["related_items"][0]["identifiers"][0]["identifier"]
        == "Identifier"
    )
    assert admin_response_data["related_items"][0]["identifiers"][0]["type"] == "ARK"
    assert admin_response_data["related_items"][0]["type"] == "Type"

    assert editor_response_data["contributors"][0]["name"] == "Name here"
    assert editor_response_data["contributors"][0]["name_type"] == "Personal"
    assert editor_response_data["contributors"][0]["contributor_type"] == "Con Type"
    assert editor_response_data["dates"][0]["date"] == "01-01-1970"
    assert editor_response_data["dates"][0]["type"] == "Type"
    assert editor_response_data["creators"][0]["name"] == "Name here"
    assert editor_response_data["creators"][0]["name_type"] == "Personal"
    assert editor_response_data["funders"][0]["name"] == "Name"
    assert editor_response_data["funders"][0]["identifier"] == "Identifier"
    assert editor_response_data["rights"][0]["identifier"] == "Identifier"
    assert editor_response_data["rights"][0]["rights"] == "Rights"
    assert editor_response_data["subjects"][0]["subject"] == "Subject"
    assert editor_response_data["about"]["language"] == "English"

    assert editor_response_data["about"]["resource_type"] == "Editor Resource Type"
    assert editor_response_data["about"]["size"] == ["Size"]
    assert editor_response_data["access"]["type"] == "editor type"
    assert editor_response_data["access"]["description"] == "editor description"
    assert editor_response_data["consent"]["noncommercial"] is True
    assert editor_response_data["consent"]["geog_restrict"] is True
    assert editor_response_data["consent"]["research_type"] is True
    assert editor_response_data["de_identification"]["direct"] is True
    assert editor_response_data["de_identification"]["type"] == "Level"
    assert editor_response_data["publisher"]["publisher"] == "Publisher"
    assert (
        editor_response_data["publisher"]["managing_organization_name"]
        == "Managing Editor Organization Name"
    )

    assert editor_response_data["identifiers"][0]["identifier"] == "identifier test"
    assert editor_response_data["identifiers"][0]["type"] == "ARK"
    assert editor_response_data["related_items"][0]["publication_year"] == "1970"
    assert editor_response_data["related_items"][0]["publisher"] == "Publisher"
    assert (
        editor_response_data["related_items"][0]["contributors"][0]["name"]
        == "Ndafsdame"
    )
    assert (
        editor_response_data["related_items"][0]["contributors"][0]["contributor_type"]
        == "Con Type"
    )
    assert editor_response_data["related_items"][0]["creators"][0]["name"] == "Name"
    assert (
        editor_response_data["related_items"][0]["creators"][0]["name_type"]
        == "Personal"
    )
    assert (
        editor_response_data["related_items"][0]["titles"][e_main_title_0]["title"]
        == "Title"
    )
    assert (
        editor_response_data["related_items"][0]["titles"][e_main_title_0]["type"]
        == "MainTitle"
    )
    assert (
        editor_response_data["related_items"][0]["titles"][e_sub_title_0]["title"]
        == "Title"
    )
    assert (
        editor_response_data["related_items"][0]["titles"][e_sub_title_0]["type"]
        == "Subtitle"
    )
    assert (
        editor_response_data["related_items"][0]["identifiers"][0]["identifier"]
        == "Identifier"
    )
    assert editor_response_data["related_items"][0]["identifiers"][0]["type"] == "ARK"
    assert editor_response_data["related_items"][0]["type"] == "Type"


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
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403
    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)

    assert response_data["readme"] == ""
    assert admin_response_data["readme"] == ""
    assert editor_response_data["readme"] == ""


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
    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme",
        json={"readme": "readme test"},
    )
    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme",
        json={"readme": "readme test"},
    )
    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/readme",
        json={"readme": "readme test"},
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403
    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)

    assert response_data["readme"] == "readme test"
    assert admin_response_data["readme"] == "readme test"
    assert editor_response_data["readme"] == "readme test"


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
    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog",
        json={"changelog": "changelog test"},
    )
    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog",
        json={"changelog": "changelog test"},
    )
    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog",
        json={"changelog": "changelog test"},
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403
    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)

    assert response_data["changelog"] == "changelog test"
    assert admin_response_data["changelog"] == "changelog test"
    assert editor_response_data["changelog"] == "changelog test"


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
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/changelog"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403
    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)

    assert response_data["changelog"] == "changelog test"
    assert admin_response_data["changelog"] == "changelog test"
    assert editor_response_data["changelog"] == "changelog test"


def test_delete_dataset_version(clients):
    """
    Given a Flask application configured for testing, study ID, dataset ID and version ID
    When the '/study/{study_id}/dataset/{dataset_id}/version/{version_id}'
    is requested (DELETE)
    Then check that the response is valid and deletes the dataset version
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]
    dataset_id = pytest.global_dataset_id
    version_id = pytest.global_dataset_version_id

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}"
    )

    assert viewer_response.status_code == 403
    assert editor_response.status_code == 403
    assert response.status_code == 204
