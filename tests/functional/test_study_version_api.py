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
    _logged_in_client.put(
        f"/study/{study_id}/metadata/description",
        json={
            "brief_summary": "brief_summary",
            "detailed_description": "detailed_description",
        },
    )
    _logged_in_client.put(
        f"/study/{study_id}/metadata/eligibility",
        json={
            "gender": "All",
            "gender_based": "Yes",
            "gender_description": "none",
            "minimum_age_value": 18,
            "maximum_age_value": 61,
            "minimum_age_unit": "1",
            "maximum_age_unit": "2",
            "healthy_volunteers": "Yes",
            "inclusion_criteria": ["tests"],
            "exclusion_criteria": ["Probability Sample"],
            "study_population": "study_population",
            "sampling_method": "Probability Sample",
        },
    )
    _logged_in_client.put(
        f"/study/{study_id}/metadata/ipdsharing",
        json={
            "ipd_sharing": "Yes",
            "ipd_sharing_description": "yes",
            "ipd_sharing_info_type_list": ["Study Protocol", "Analytical Code"],
            "ipd_sharing_time_frame": "uh",
            "ipd_sharing_access_criteria": "Study Protocol",
            "ipd_sharing_url": "1",
        },
    )
    _logged_in_client.put(
        f"/study/{study_id}/metadata/sponsors",
        json={
            "responsible_party_type": "Sponsor",
            "responsible_party_investigator_name": "party name",
            "responsible_party_investigator_title": "party title",
            "responsible_party_investigator_affiliation": "party affiliation",
            "lead_sponsor_name": "sponsor name",
        },
    )
    _logged_in_client.put(
        f"/study/{study_id}/metadata/collaborators",
        json=[
            "collaborator1123",
        ],
    )

    _logged_in_client.put(
        f"/study/{study_id}/metadata/status",
        json={
            "overall_status": "Withdrawn",
            "why_stopped": "test",
            "start_date": "2023-11-15 00:00:00",
            "start_date_type": "Actual",
            "completion_date": "2023-11-16 00:00:00",

            "completion_date_type": "Actual",
        },
    )
    _logged_in_client.put(
        f"/study/{study_id}/metadata/conditions",
        json=["c"],
    )
    _logged_in_client.put(
        f"/study/{study_id}/metadata/design",
        json={
            "design_allocation": "dfasdfasd",
            "study_type": "Interventional",
            "design_intervention_model": "Treatment",
            "design_intervention_model_description": "dfadf",
            "design_primary_purpose": "Parallel Assignment",
            "design_masking": "Double",
            "design_masking_description": "tewsfdasf",
            "design_who_masked_list": ["Participant", "Care Provider"],
            "phase_list": ["N/A"],
            "enrollment_count": 3,
            "enrollment_type": "Actual",
            "number_arms": 2,
            "design_observational_model_list": ["Cohort", "Case-Control"],
            "design_time_perspective_list": ["Other"],
            "bio_spec_retention": "None Retained",
            "bio_spec_description": "dfasdf",
            "target_duration": "rewrwe",
            "number_groups_cohorts": 1,
        },
    )
    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/version/{version_id}/study-metadata"
    )
    response_data = json.loads(response.data)
    # print(response_data)
    assert response.status_code == 200
    assert response_data["ipd_sharing"]["ipd_sharing_info_type_list"] ==  ["Study Protocol", "Analytical Code"]
    assert response_data["ipd_sharing"]["ipd_sharing"] == "Yes"
    assert response_data["available_ipd"][0]["identifier"] == "identifier1"
    assert response_data["available_ipd"][0]["url"] == "google.com"
    assert response_data["arms"][0]["label"] == "Label1"

    assert response_data["contacts"][0]["name"] == "central-contact"
    assert response_data["contacts"][0]["affiliation"] == "affiliation"
    assert response_data["description"]["brief_summary"] == "brief_summary"

    assert response_data["design"]["design_allocation"] == "dfasdfasd"
    assert response_data["design"]["study_type"] == "Interventional"
    assert response_data["design"]["design_intervention_model"] == "Treatment"
    assert response_data["design"]["design_primary_purpose"] == "Parallel Assignment"
    assert response_data["design"]["design_masking"] == "Double"
    assert response_data["design"]["design_who_masked_list"] == ["Participant", "Care Provider"]
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
    assert response_data["design"]["bio_spec_description"] == "dfasdf"
    assert response_data["design"]["target_duration"] == "rewrwe"
    assert response_data["design"]["number_groups_cohorts"] == 1


    assert response_data["eligibility"]["gender"] == "All"
    assert response_data["eligibility"]["minimum_age_value"] == 18
    assert response_data["primary_identifier"]["identifier"] == "test"
    assert response_data["primary_identifier"]["identifier_type"] == "test"
    assert response_data["secondary_identifiers"][0]["identifier"] == "test"
    assert response_data["secondary_identifiers"][0]["identifier_type"] == "test"
    assert response_data["interventions"][0]["type"] == "Device"
    assert response_data["interventions"][0]["name"] == "name test"
    assert response_data["links"][0]["title"] == "google link"
    assert response_data["links"][0]["url"] == "google.com"
    assert response_data["locations"][0]["country"] == "yes"
    assert response_data["locations"][0]["facility"] == "test"
    assert response_data["overall_officials"][0]["name"] == "test"
    assert response_data["overall_officials"][0]["affiliation"] == "aff"
    assert response_data["references"][0]["identifier"] == "reference identifier"
    assert response_data["references"][0]["citation"] == "reference citation"
    assert response_data["sponsors"]["responsible_party_type"] == "Sponsor"
    assert response_data["sponsors"]["responsible_party_investigator_name"] == "party name"
    assert response_data["collaborators"] == ["collaborator1123"]
    assert response_data["status"]["overall_status"] == "Withdrawn"
    assert response_data["status"]["start_date"] == "2023-11-15 00:00:00"
    assert response_data["oversight"] is True
    assert response_data["conditions"] == ["c"]


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
    response_data = json.loads(response.data)
    print(response_data)
    assert response.status_code == 200

    assert response_data["links"][0]["url"] == "google.com"
    assert response_data["locations"][0]["country"] == "yes"
    assert response_data["locations"][0]["facility"] == "test"
    assert response_data["overall_officials"][0]["name"] == "test"
    assert response_data["overall_officials"][0]["affiliation"] == "aff"
    assert response_data["references"][0]["identifier"] == "reference identifier"
    assert response_data["references"][0]["citation"] == "reference citation"


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
