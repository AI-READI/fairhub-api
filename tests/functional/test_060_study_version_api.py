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
            "changelog": "changelog testing here",
        },
    )
    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_dataset_version_id = response_data["id"]
    assert response_data["title"] == "Dataset Version 1.0"
    assert response_data["published"] is False
    assert response_data["doi"] == f"10.36478/fairhub.{response_data['identifier']}"
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
    assert response_data[0]["changelog"] == "changelog testing here"
    assert (
        response_data[0]["doi"] == f"10.36478/fairhub.{response_data[0]['identifier']}"
    )

    assert admin_response_data[0]["title"] == "Dataset Version 1.0"
    assert admin_response_data[0]["published"] is False
    assert (
        admin_response_data[0]["doi"]
        == f"10.36478/fairhub.{response_data[0]['identifier']}"
    )
    assert admin_response_data[0]["changelog"] == "changelog testing here"

    assert editor_response_data[0]["title"] == "Dataset Version 1.0"
    assert editor_response_data[0]["published"] is False
    assert (
        editor_response_data[0]["doi"]
        == f"10.36478/fairhub.{response_data[0]['identifier']}"
    )
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
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403
    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)

    assert response_data["title"] == "Dataset Version 1.0"
    assert response_data["published"] is False
    assert response_data["changelog"] == "changelog testing here"
    assert response_data["doi"] == f"10.36478/fairhub.{response_data['identifier']}"

    assert admin_response_data["title"] == "Dataset Version 1.0"
    assert admin_response_data["published"] is False
    assert (
        admin_response_data["doi"] == f"10.36478/fairhub.{response_data['identifier']}"
    )
    assert admin_response_data["changelog"] == "changelog testing here"

    assert editor_response_data["title"] == "Dataset Version 1.0"
    assert editor_response_data["published"] is False
    assert (
        editor_response_data["doi"] == f"10.36478/fairhub.{response_data['identifier']}"
    )
    assert editor_response_data["changelog"] == "changelog testing here"


def test_put_dataset_version(clients):
    """
    Given a Flask application configured for testing, study ID, dataset ID and version ID
    When the '/study/{study_id}/dataset/{dataset_id}/version/{version_id}'
    is requested (PUT)
    Then check that the response is valid and updates the dataset version
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    version_id = pytest.global_dataset_version_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}",
        json={
            "title": "Dataset Version 2.0",
            "changelog": "Updating the changelog",
            "published": False,
            "readme": "readme testing here",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["title"] == "Dataset Version 2.0"
    assert response_data["changelog"] == "Updating the changelog"
    assert response_data["doi"] == f"10.36478/fairhub.{response_data['identifier']}"
    assert response_data["readme"] == ""
    assert response_data["published"] is False

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}",
        json={
            "title": "Dataset Version 3.0",
            "changelog": "Changelog modified by admin",
            "published": False,
            "readme": "readme modified by editor",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["title"] == "Dataset Version 3.0"
    assert admin_response_data["changelog"] == "Changelog modified by admin"
    assert admin_response_data["published"] is False
    assert (
        admin_response_data["doi"] == f"10.36478/fairhub.{response_data['identifier']}"
    )

    assert admin_response_data["readme"] == ""

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}",
        json={
            "title": "Dataset Version 4.0",
            "changelog": "Changelog modified by editor",
            "published": False,
            "readme": "readme modified by editor",
        },
    )

    assert editor_response.status_code == 403

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}",
        json={
            "title": "Dataset Version 5.0",
            "changelog": "Changelog modified by viewer",
            "published": False,
            "readme": "readme modified by viewer",
        },
    )

    assert viewer_response.status_code == 403


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

    cc_response = _logged_in_client.post(
        f"/study/{study_id}/metadata/central-contact",
        json=[
            {
                "affiliation": "affiliation",
                "phone": "808",
                "phone_ext": "909",
                "email_address": "sample@gmail.com",
                "first_name": "central-contact",
                "last_name": "central-contact",
                "degree": "degree",
                "identifier": "central-contact",
                "identifier_scheme": "id",
                "identifier_scheme_uri": "uri",
                "affiliation_identifier": "affiliation identifier",
                "affiliation_identifier_scheme": "affiliation identifier scheme",
                "affiliation_identifier_scheme_uri": "affiliation identifier scheme uri",
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
                "other_name_list": ["uhh", "yes"],
            }
        ],
    )
    collaborators_response = _logged_in_client.post(
        f"/study/{study_id}/metadata/collaborators",
        json=[
            {
                "name": "collaborator1123",
                "identifier": "collaborator1123",
                "identifier_scheme": "collaborator1123",
                "identifier_scheme_uri": "collaborator1123",
            }
        ],
    )
    conditions_response = _logged_in_client.post(
        f"/study/{study_id}/metadata/conditions",
        json=[
            {
                "name": "condition",
                "classification_code": "classification code",
                "scheme": "scheme",
                "scheme_uri": "scheme uri",
                "condition_uri": "condition",
            }
        ],
    )
    keywords_response = _logged_in_client.post(
        f"/study/{study_id}/metadata/keywords",
        json=[
            {
                "name": "keywords",
                "classification_code": "classification code",
                "scheme": "scheme",
                "scheme_uri": "scheme uri",
                "keyword_uri": "keywords",
            }
        ],
    )

    of_response = _logged_in_client.post(
        f"/study/{study_id}/metadata/overall-official",
        json=[
            {
                "first_name": "test",
                "last_name": "test",
                "degree": "aff",
                "identifier": "identifier",
                "identifier_scheme": "scheme",
                "identifier_scheme_uri": "uri",
                "affiliation": "aff",
                "affiliation_identifier": "identifier",
                "affiliation_identifier_scheme": "scheme",
                "affiliation_identifier_scheme_uri": "uri",
                "role": "chair",
            }
        ],
    )

    assert arm_response.status_code == 201
    assert cc_response.status_code == 201
    assert location_response.status_code == 201
    assert id_response.status_code == 201
    assert intervention_response.status_code == 201
    assert of_response.status_code == 201
    assert collaborators_response.status_code == 201
    assert conditions_response.status_code == 201
    assert keywords_response.status_code == 201

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
    viewer_response_data = json.loads(editor_response.data)

    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["central_contacts"][0]["phone"] == "808"
    assert response_data["central_contacts"][0]["first_name"] == "central-contact"
    assert response_data["central_contacts"][0]["last_name"] == "central-contact"
    assert response_data["central_contacts"][0]["affiliation"] == "affiliation"
    assert response_data["collaborators"][0]["name"] == "collaborator1123"
    assert response_data["conditions"][0]["name"] == "condition"
    assert response_data["keywords"][0]["name"] == "keywords"
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
    assert response_data["design"]["is_patient_registry"] == "yes"
    assert response_data["eligibility"]["sex"] == "All"
    assert response_data["eligibility"]["gender_based"] == "Yes"
    assert response_data["eligibility"]["maximum_age_value"] == 61
    assert response_data["primary_identifier"]["identifier"] == "test"
    assert response_data["primary_identifier"]["identifier_type"] == "test"
    assert response_data["secondary_identifiers"][0]["identifier"] == "test"
    assert response_data["secondary_identifiers"][0]["identifier_type"] == "test"
    assert response_data["interventions"][0]["type"] == "Device"
    assert response_data["interventions"][0]["name"] == "name test"
    assert response_data["locations"][0]["country"] == "yes"
    assert response_data["locations"][0]["facility"] == "test"
    assert response_data["overall_officials"][0]["first_name"] == "test"
    assert response_data["overall_officials"][0]["last_name"] == "test"
    assert response_data["overall_officials"][0]["role"] == "chair"
    assert response_data["overall_officials"][0]["affiliation"] == "aff"
    assert response_data["oversight"]["fda_regulated_drug"] == "drug"
    assert response_data["oversight"]["fda_regulated_device"] == "device"
    assert response_data["oversight"]["has_dmc"] == "yes"
    assert response_data["oversight"]["human_subject_review_status"] == "yes"
    assert response_data["sponsors"]["responsible_party_type"] == "Sponsor"
    assert (
        response_data["sponsors"]["responsible_party_investigator_first_name"] == "name"
    )
    assert (
        response_data["sponsors"]["responsible_party_investigator_last_name"]
        == "surname"
    )
    assert response_data["sponsors"]["lead_sponsor_name"] == "name"
    assert response_data["status"]["overall_status"] == "Withdrawn"
    assert response_data["status"]["start_date"] == "2023-11-15 00:00:00"

    assert admin_response_data["arms"][0]["label"] == "Label1"
    assert admin_response_data["central_contacts"][0]["phone"] == "808"
    assert admin_response_data["central_contacts"][0]["first_name"] == "central-contact"
    assert admin_response_data["central_contacts"][0]["last_name"] == "central-contact"
    assert admin_response_data["central_contacts"][0]["affiliation"] == "affiliation"
    assert admin_response_data["collaborators"][0]["name"] == "collaborator1123"
    assert admin_response_data["conditions"][0]["name"] == "condition"
    assert admin_response_data["keywords"][0]["name"] == "keywords"
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
    assert admin_response_data["design"]["is_patient_registry"] == "yes"
    assert admin_response_data["eligibility"]["sex"] == "All"
    assert admin_response_data["eligibility"]["gender_based"] == "Yes"
    assert admin_response_data["eligibility"]["maximum_age_value"] == 61
    assert admin_response_data["primary_identifier"]["identifier"] == "test"
    assert admin_response_data["primary_identifier"]["identifier_type"] == "test"
    assert admin_response_data["secondary_identifiers"][0]["identifier"] == "test"
    assert admin_response_data["secondary_identifiers"][0]["identifier_type"] == "test"
    assert admin_response_data["interventions"][0]["type"] == "Device"
    assert admin_response_data["interventions"][0]["name"] == "name test"
    assert admin_response_data["locations"][0]["country"] == "yes"
    assert admin_response_data["locations"][0]["facility"] == "test"
    assert admin_response_data["overall_officials"][0]["first_name"] == "test"
    assert admin_response_data["overall_officials"][0]["last_name"] == "test"
    assert admin_response_data["overall_officials"][0]["role"] == "chair"
    assert admin_response_data["overall_officials"][0]["affiliation"] == "aff"
    assert admin_response_data["oversight"]["fda_regulated_drug"] == "drug"
    assert admin_response_data["oversight"]["fda_regulated_device"] == "device"
    assert admin_response_data["oversight"]["has_dmc"] == "yes"
    assert admin_response_data["oversight"]["human_subject_review_status"] == "yes"
    assert admin_response_data["sponsors"]["responsible_party_type"] == "Sponsor"
    assert (
        admin_response_data["sponsors"]["responsible_party_investigator_first_name"]
        == "name"
    )
    assert (
        admin_response_data["sponsors"]["responsible_party_investigator_last_name"]
        == "surname"
    )
    assert admin_response_data["sponsors"]["lead_sponsor_name"] == "name"
    assert admin_response_data["status"]["overall_status"] == "Withdrawn"
    assert admin_response_data["status"]["start_date"] == "2023-11-15 00:00:00"

    assert editor_response_data["arms"][0]["label"] == "Label1"
    assert editor_response_data["central_contacts"][0]["phone"] == "808"
    assert (
        editor_response_data["central_contacts"][0]["first_name"] == "central-contact"
    )
    assert editor_response_data["central_contacts"][0]["last_name"] == "central-contact"
    assert editor_response_data["central_contacts"][0]["affiliation"] == "affiliation"
    assert editor_response_data["collaborators"][0]["name"] == "collaborator1123"
    assert editor_response_data["conditions"][0]["name"] == "condition"
    assert editor_response_data["keywords"][0]["name"] == "keywords"
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
    assert editor_response_data["design"]["is_patient_registry"] == "yes"
    assert editor_response_data["eligibility"]["sex"] == "All"
    assert editor_response_data["eligibility"]["gender_based"] == "Yes"
    assert editor_response_data["eligibility"]["maximum_age_value"] == 61
    assert editor_response_data["primary_identifier"]["identifier"] == "test"
    assert editor_response_data["primary_identifier"]["identifier_type"] == "test"
    assert editor_response_data["secondary_identifiers"][0]["identifier"] == "test"
    assert editor_response_data["secondary_identifiers"][0]["identifier_type"] == "test"
    assert editor_response_data["interventions"][0]["type"] == "Device"
    assert editor_response_data["interventions"][0]["name"] == "name test"
    assert editor_response_data["locations"][0]["country"] == "yes"
    assert editor_response_data["locations"][0]["facility"] == "test"
    assert editor_response_data["overall_officials"][0]["first_name"] == "test"
    assert editor_response_data["overall_officials"][0]["last_name"] == "test"
    assert editor_response_data["overall_officials"][0]["role"] == "chair"
    assert editor_response_data["overall_officials"][0]["affiliation"] == "aff"
    assert editor_response_data["oversight"]["fda_regulated_drug"] == "drug"
    assert editor_response_data["oversight"]["fda_regulated_device"] == "device"
    assert editor_response_data["oversight"]["has_dmc"] == "yes"
    assert editor_response_data["oversight"]["human_subject_review_status"] == "yes"
    assert editor_response_data["sponsors"]["responsible_party_type"] == "Sponsor"
    assert (
        editor_response_data["sponsors"]["responsible_party_investigator_first_name"]
        == "name"
    )
    assert (
        editor_response_data["sponsors"]["responsible_party_investigator_last_name"]
        == "surname"
    )
    assert editor_response_data["sponsors"]["lead_sponsor_name"] == "name"
    assert editor_response_data["status"]["overall_status"] == "Withdrawn"
    assert editor_response_data["status"]["start_date"] == "2023-11-15 00:00:00"

    assert viewer_response_data["arms"][0]["label"] == "Label1"
    assert viewer_response_data["central_contacts"][0]["phone"] == "808"
    assert (
        viewer_response_data["central_contacts"][0]["first_name"] == "central-contact"
    )
    assert viewer_response_data["central_contacts"][0]["last_name"] == "central-contact"
    assert viewer_response_data["central_contacts"][0]["affiliation"] == "affiliation"
    assert viewer_response_data["collaborators"][0]["name"] == "collaborator1123"
    assert viewer_response_data["conditions"][0]["name"] == "condition"
    assert viewer_response_data["keywords"][0]["name"] == "keywords"
    assert (
        viewer_response_data["description"]["brief_summary"] == "editor-brief_summary"
    )
    assert viewer_response_data["design"]["design_allocation"] == "editor-dfasdfasd"
    assert viewer_response_data["design"]["study_type"] == "Interventional"
    assert viewer_response_data["design"]["design_intervention_model"] == "Treatment"
    assert (
        viewer_response_data["design"]["design_primary_purpose"]
        == "Parallel Assignment"
    )
    assert viewer_response_data["design"]["design_masking"] == "Double"
    assert viewer_response_data["design"]["design_masking_description"] == "tewsfdasf"
    assert viewer_response_data["design"]["design_who_masked_list"] == [
        "Participant",
        "Care Provider",
    ]
    assert viewer_response_data["design"]["phase_list"] == ["N/A"]
    assert viewer_response_data["design"]["enrollment_count"] == 3
    assert viewer_response_data["design"]["enrollment_type"] == "Actual"
    assert viewer_response_data["design"]["number_arms"] == 2
    assert viewer_response_data["design"]["design_observational_model_list"] == [
        "Cohort",
        "Case-Control",
    ]
    assert viewer_response_data["design"]["design_time_perspective_list"] == ["Other"]
    assert viewer_response_data["design"]["bio_spec_retention"] == "None Retained"
    assert viewer_response_data["design"]["target_duration"] == "rewrwe"
    assert viewer_response_data["design"]["is_patient_registry"] == "yes"
    assert viewer_response_data["eligibility"]["sex"] == "All"
    assert viewer_response_data["eligibility"]["gender_based"] == "Yes"
    assert viewer_response_data["eligibility"]["maximum_age_value"] == 61
    assert viewer_response_data["primary_identifier"]["identifier"] == "test"
    assert viewer_response_data["primary_identifier"]["identifier_type"] == "test"
    assert viewer_response_data["secondary_identifiers"][0]["identifier"] == "test"
    assert viewer_response_data["secondary_identifiers"][0]["identifier_type"] == "test"
    assert viewer_response_data["interventions"][0]["type"] == "Device"
    assert viewer_response_data["interventions"][0]["name"] == "name test"
    assert viewer_response_data["locations"][0]["country"] == "yes"
    assert viewer_response_data["locations"][0]["facility"] == "test"
    assert viewer_response_data["overall_officials"][0]["first_name"] == "test"
    assert viewer_response_data["overall_officials"][0]["last_name"] == "test"
    assert viewer_response_data["overall_officials"][0]["role"] == "chair"
    assert viewer_response_data["overall_officials"][0]["affiliation"] == "aff"
    assert viewer_response_data["oversight"]["fda_regulated_drug"] == "drug"
    assert viewer_response_data["oversight"]["fda_regulated_device"] == "device"
    assert viewer_response_data["oversight"]["has_dmc"] == "yes"
    assert viewer_response_data["oversight"]["human_subject_review_status"] == "yes"
    assert viewer_response_data["sponsors"]["responsible_party_type"] == "Sponsor"
    assert (
        viewer_response_data["sponsors"]["responsible_party_investigator_first_name"]
        == "name"
    )
    assert (
        viewer_response_data["sponsors"]["responsible_party_investigator_last_name"]
        == "surname"
    )
    assert viewer_response_data["sponsors"]["lead_sponsor_name"] == "name"
    assert viewer_response_data["status"]["overall_status"] == "Withdrawn"
    assert viewer_response_data["status"]["start_date"] == "2023-11-15 00:00:00"


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
    creator_response = _logged_in_client.post(
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
                "identifier_scheme_uri": "Identifier Scheme",
                "rights": "Rights",
                "uri": "URI",
                "license_text": "license text",
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
    related_identifier_response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier",
        json=[
            {
                "identifier": "editor test identifier",
                "identifier_type": "test identifier type",
                "relation_type": "test relation type",
                "related_metadata_scheme": "test",
                "scheme_uri": "test",
                "scheme_type": "test",
                "resource_type": "test",
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
    assert related_identifier_response.status_code == 201

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

    assert response_data["contributors"][0]["last_name"] == "Family Name here"
    assert response_data["contributors"][0]["first_name"] == "Given Name here"
    assert response_data["contributors"][0]["name_type"] == "Personal"
    assert response_data["contributors"][0]["contributor_type"] == "Con Type"

    assert response_data["dates"][0]["date"] == "01-01-1970"
    assert response_data["dates"][0]["type"] == "Type"

    assert response_data["creators"][0]["last_name"] == "Family Name here"
    assert response_data["creators"][0]["first_name"] == "Given Name here"
    assert response_data["creators"][0]["name_type"] == "Personal"

    assert response_data["funders"][0]["name"] == "Name"
    assert response_data["funders"][0]["identifier"] == "Identifier"

    assert response_data["rights"][0]["identifier"] == "Identifier"
    assert response_data["rights"][0]["rights"] == "Rights"

    assert response_data["subjects"][0]["subject"] == "Subject"

    assert response_data["about"]["language"] == "English"

    assert response_data["about"]["resource_type"] == "Resource Type"
    assert response_data["about"]["size"] == ["Size"]

    assert response_data["access"]["type"] == "editor type"
    assert response_data["access"]["description"] == "editor description"

    assert response_data["consent"]["noncommercial"] is True
    assert response_data["consent"]["geog_restrict"] is True
    assert response_data["consent"]["research_type"] is True

    assert response_data["de_identification"]["direct"] is True
    assert response_data["de_identification"]["type"] == "Level"

    assert (
        response_data["managing_organization"]["name"]
        == "editor Managing Organization Name"
    )
    assert response_data["managing_organization"]["identifier"] == "identifier"
    assert response_data["identifiers"][0]["identifier"] == "identifier test"
    assert response_data["identifiers"][0]["type"] == "ARK"

    assert (
        response_data["related_identifier"][0]["identifier"] == "editor test identifier"
    )
    assert (
        response_data["related_identifier"][0]["relation_type"] == "test relation type"
    )
    assert response_data["related_identifier"][0]["resource_type"] == "test"

    assert admin_response_data["contributors"][0]["first_name"] == "Given Name here"
    assert admin_response_data["contributors"][0]["last_name"] == "Family Name here"
    assert admin_response_data["contributors"][0]["name_type"] == "Personal"
    assert admin_response_data["contributors"][0]["contributor_type"] == "Con Type"
    assert admin_response_data["dates"][0]["date"] == "01-01-1970"
    assert admin_response_data["dates"][0]["type"] == "Type"
    assert admin_response_data["creators"][0]["first_name"] == "Given Name here"
    assert admin_response_data["creators"][0]["last_name"] == "Family Name here"
    assert admin_response_data["creators"][0]["name_type"] == "Personal"
    assert admin_response_data["funders"][0]["name"] == "Name"
    assert admin_response_data["funders"][0]["identifier"] == "Identifier"
    assert admin_response_data["rights"][0]["identifier"] == "Identifier"
    assert admin_response_data["rights"][0]["rights"] == "Rights"
    assert admin_response_data["subjects"][0]["subject"] == "Subject"
    assert admin_response_data["about"]["language"] == "English"

    assert admin_response_data["about"]["resource_type"] == "Resource Type"
    assert admin_response_data["about"]["size"] == ["Size"]
    assert admin_response_data["access"]["type"] == "editor type"
    assert admin_response_data["access"]["description"] == "editor description"
    assert admin_response_data["consent"]["noncommercial"] is True
    assert admin_response_data["consent"]["geog_restrict"] is True
    assert admin_response_data["consent"]["research_type"] is True
    assert admin_response_data["de_identification"]["direct"] is True
    assert admin_response_data["de_identification"]["type"] == "Level"
    assert (
        admin_response_data["managing_organization"]["name"]
        == "editor Managing Organization Name"
    )
    assert admin_response_data["managing_organization"]["identifier"] == "identifier"

    assert admin_response_data["identifiers"][0]["identifier"] == "identifier test"
    assert admin_response_data["identifiers"][0]["type"] == "ARK"

    assert (
        admin_response_data["related_identifier"][0]["identifier"]
        == "editor test identifier"
    )
    assert (
        admin_response_data["related_identifier"][0]["relation_type"]
        == "test relation type"
    )
    assert admin_response_data["related_identifier"][0]["resource_type"] == "test"

    assert editor_response_data["contributors"][0]["first_name"] == "Given Name here"
    assert editor_response_data["contributors"][0]["last_name"] == "Family Name here"
    assert editor_response_data["contributors"][0]["name_type"] == "Personal"
    assert editor_response_data["contributors"][0]["contributor_type"] == "Con Type"
    assert editor_response_data["dates"][0]["date"] == "01-01-1970"
    assert editor_response_data["dates"][0]["type"] == "Type"
    assert editor_response_data["creators"][0]["first_name"] == "Given Name here"
    assert editor_response_data["creators"][0]["last_name"] == "Family Name here"
    assert editor_response_data["creators"][0]["name_type"] == "Personal"
    assert editor_response_data["funders"][0]["name"] == "Name"
    assert editor_response_data["funders"][0]["identifier"] == "Identifier"
    assert editor_response_data["rights"][0]["identifier"] == "Identifier"
    assert editor_response_data["rights"][0]["rights"] == "Rights"
    assert editor_response_data["subjects"][0]["subject"] == "Subject"
    assert editor_response_data["about"]["language"] == "English"

    assert editor_response_data["about"]["resource_type"] == "Resource Type"
    assert editor_response_data["about"]["size"] == ["Size"]
    assert editor_response_data["access"]["type"] == "editor type"
    assert editor_response_data["access"]["description"] == "editor description"
    assert editor_response_data["consent"]["noncommercial"] is True
    assert editor_response_data["consent"]["geog_restrict"] is True
    assert editor_response_data["consent"]["research_type"] is True
    assert editor_response_data["de_identification"]["direct"] is True
    assert editor_response_data["de_identification"]["type"] == "Level"
    assert (
        editor_response_data["managing_organization"]["name"]
        == "editor Managing Organization Name"
    )
    assert editor_response_data["managing_organization"]["identifier"] == "identifier"

    assert editor_response_data["identifiers"][0]["identifier"] == "identifier test"
    assert editor_response_data["identifiers"][0]["type"] == "ARK"

    assert (
        editor_response_data["related_identifier"][0]["identifier"]
        == "editor test identifier"
    )
    assert (
        editor_response_data["related_identifier"][0]["relation_type"]
        == "test relation type"
    )
    assert editor_response_data["related_identifier"][0]["resource_type"] == "test"


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
    study_id = pytest.global_study_id["id"]  # type: ignore
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
