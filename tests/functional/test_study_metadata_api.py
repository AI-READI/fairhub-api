# pylint: disable=too-many-lines
"""Tests for the Study Metadata API endpoints"""
import json

import pytest


# ------------------- ARM METADATA ------------------- #
def test_post_arm_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/arm' endpoint is requested (POST)
    THEN check that the response is vaild and create a new arm
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_arm_id = response_data["arms"][0]["id"]

    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["arms"][0]["type"] == "Experimental"
    assert response_data["arms"][0]["description"] == "Arm Description"
    assert response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]


def test_get_arm_metadata(_logged_in_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/arm/metadata' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the arm metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/arm")

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["arms"][0]["type"] == "Experimental"
    assert response_data["arms"][0]["description"] == "Arm Description"
    assert response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]


def test_delete_arm_metadata(_logged_in_client):
    """
    GIVEN a Flask application configured for testing and a study ID and arm ID
    WHEN the '/study/{study_id}/arm/metadata' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the arm metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    arm_id = pytest.global_arm_id

    response = _logged_in_client.delete(f"/study/{study_id}/metadata/arm/{arm_id}")

    assert response.status_code == 204


# ------------------- IPD METADATA ------------------- #
def test_post_available_ipd_metadata(_logged_in_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/available-id' endpoint is requested (POST)
    THEN check that the response is vaild and new IPD was created
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_available_ipd_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "identifier1"
    assert response_data[0]["type"] == "Clinical Study Report"
    assert response_data[0]["url"] == "google.com"
    assert response_data[0]["comment"] == "comment1"


def test_get_available_ipd_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/available-id' endpoint is requested (GET)
    THEN check that the response is vaild and retrieves the available IPD(s)
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/available-ipd")

    assert response.status_code == 200


def test_delete_available_ipd_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID and available IPD ID
    WHEN the '/study/{study_id}/metadata/available-id' endpoint is requested (DELETE)
    THEN check that the response is vaild and deletes the available IPD
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    available_ipd_id = pytest.global_available_ipd_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/available-ipd/{available_ipd_id}"
    )

    assert response.status_code == 204


# ------------------- CENTRAL CONTACT METADATA ------------------- #
def test_post_cc_metadata(_logged_in_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/central-contact' endpoint is requested (POST)
    THEN check that the response is valid and creates the central contact metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_cc_id = response_data[0]["id"]

    assert response_data[0]["name"] == "central-contact"
    assert response_data[0]["affiliation"] == "affiliation"
    assert response_data[0]["role"] is None
    assert response_data[0]["phone"] == "808"
    assert response_data[0]["phone_ext"] == "909"
    assert response_data[0]["email_address"] == "sample@gmail.com"
    assert response_data[0]["central_contact"] is True


def test_get_cc_metadata(_logged_in_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/central-contact' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the central contact metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/central-contact")

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data[0]["name"] == "central-contact"
    assert response_data[0]["affiliation"] == "affiliation"
    assert response_data[0]["role"] is None
    assert response_data[0]["phone"] == "808"
    assert response_data[0]["phone_ext"] == "909"
    assert response_data[0]["email_address"] == "sample@gmail.com"
    assert response_data[0]["central_contact"] is True


def test_delete_cc_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
        and central contact ID
    WHEN the '/study/{study_id}/metadata/central-contact/{central_contact_id}'
        endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the central contact metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    central_contact_id = pytest.global_cc_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/central-contact/{central_contact_id}"
    )

    assert response.status_code == 204


#  ------------------- COLLABORATORS METADATA ------------------- #
def test_get_collaborators_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/collaborators' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the collaborators metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/collaborators")

    assert response.status_code == 200


def test_put_collaborators_metadata(_logged_in_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/collaborators'
        endpoint is requested (POST)
    THEN check that the response is valid and creates the collaborators metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/collaborators",
        json=[
            "collaborator1123",
        ],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data[0] == "collaborator1123"


# ------------------- CONDITIONS METADATA ------------------- #
def test_get_conditions_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/conditions' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the conditions metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/conditions")

    assert response.status_code == 200


def test_put_conditions_metadata(_logged_in_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/conditions' endpoint is requested (POST)
    THEN check that the response is valid and creates the conditions metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/conditions",
        json=[
            "true",
            "conditions string",
            "keywords string",
            "size string",
        ],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data[0] == "true"
    assert response_data[1] == "conditions string"
    assert response_data[2] == "keywords string"
    assert response_data[3] == "size string"


# ------------------- DESCRIPTION METADATA ------------------- #
def test_get_description_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/description' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the description metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/description")

    assert response.status_code == 200


def test_put_description_metadata(_logged_in_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/description' endpoint is requested (POST)
    THEN check that the response is valid and creates the description metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/description",
        json={
            "brief_summary": "brief_summary",
            "detailed_description": "detailed_description",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["brief_summary"] == "brief_summary"
    assert response_data["detailed_description"] == "detailed_description"


# ------------------- DESIGN METADATA ------------------- #
def test_get_design_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/design' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/design")

    assert response.status_code == 200


def test_put_design_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/design' endpoint is requested (PUT)
    THEN check that the response is valid and creates the design metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
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

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["design_allocation"] == "dfasdfasd"
    assert response_data["study_type"] == "Interventional"
    assert response_data["design_intervention_model"] == "Treatment"
    assert response_data["design_intervention_model_description"] == "dfadf"
    assert response_data["design_primary_purpose"] == "Parallel Assignment"
    assert response_data["design_masking"] == "Double"
    assert response_data["design_masking_description"] == "tewsfdasf"
    assert response_data["design_who_masked_list"] == ["Participant", "Care Provider"]
    assert response_data["phase_list"] == ["N/A"]
    assert response_data["enrollment_count"] == 3
    assert response_data["enrollment_type"] == "Actual"
    assert response_data["number_arms"] == 2
    assert response_data["design_observational_model_list"] == [
        "Cohort",
        "Case-Control",
    ]
    assert response_data["design_time_perspective_list"] == ["Other"]
    assert response_data["bio_spec_retention"] == "None Retained"
    assert response_data["bio_spec_description"] == "dfasdf"
    assert response_data["target_duration"] == "rewrwe"
    assert response_data["number_groups_cohorts"] == 1


# ------------------- ELIGIBILITY METADATA ------------------- #
def test_get_eligibility_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/eligibility' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the eligibility metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/eligibility")

    assert response.status_code == 200


def test_put_eligibility_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/eligibility' endpoint is requested (PUT)
    THEN check that the response is valid and updates the eligibility metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
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

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["gender"] == "All"
    assert response_data["gender_based"] == "Yes"
    assert response_data["gender_description"] == "none"
    assert response_data["minimum_age_value"] == 18
    assert response_data["maximum_age_value"] == 61
    assert response_data["minimum_age_unit"] == "1"
    assert response_data["maximum_age_unit"] == "2"
    assert response_data["healthy_volunteers"] == "Yes"
    assert response_data["inclusion_criteria"] == ["tests"]
    assert response_data["exclusion_criteria"] == ["Probability Sample"]
    assert response_data["study_population"] == "study_population"
    assert response_data["sampling_method"] == "Probability Sample"


# ------------------- IDENTIFICATION METADATA ------------------- #
def test_get_identification_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/identification' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the identification metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/identification")

    assert response.status_code == 200


def test_post_identification_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/identification' endpoint is requested (POST)
    THEN check that the response is valid and creates the identification metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
        f"/study/{study_id}/metadata/identification",
        json={
            "primary": {
                "identifier": "first",
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_identification_id = response_data["secondary"][0]["id"]

    assert response_data["primary"]["identifier"] == "first"
    assert response_data["primary"]["identifier_type"] == "test"
    assert response_data["primary"]["identifier_domain"] == "domain"
    assert response_data["primary"]["identifier_link"] == "link"
    assert response_data["secondary"][0]["identifier"] == "test"
    assert response_data["secondary"][0]["identifier_type"] == "test"
    assert response_data["secondary"][0]["identifier_domain"] == "dodfasdfmain"
    assert response_data["secondary"][0]["identifier_link"] == "link"


def test_delete_identification_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/identification' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the identification metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    identification_id = pytest.global_identification_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/identification/{identification_id}"
    )

    assert response.status_code == 204


# ------------------- INTERVENTION METADATA ------------------- #
def test_get_intervention_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/intervention' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the intervention metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/intervention")

    assert response.status_code == 200


def test_post_intervention_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/intervention' endpoint is requested (POST)
    THEN check that the response is valid and creates the intervention metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_intervention_id = response_data[0]["id"]

    assert response_data[0]["type"] == "Device"
    assert response_data[0]["name"] == "name test"
    assert response_data[0]["description"] == "desc"
    assert response_data[0]["arm_group_label_list"] == ["test", "one"]
    assert response_data[0]["other_name_list"] == ["uhh", "yes"]


# ------------------- IPD SHARING METADATA ------------------- #
def test_get_ipdsharing_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/ipdsharing' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the ipdsharing metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/ipdsharing")

    assert response.status_code == 200


def test_put_ipdsharing_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/ipdsharing' endpoint is requested (PUT)
    THEN check that the response is valid and updates the ipdsharing metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
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

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["ipd_sharing"] == "Yes"
    assert response_data["ipd_sharing_description"] == "yes"
    assert response_data["ipd_sharing_info_type_list"] == [
        "Study Protocol",
        "Analytical Code",
    ]
    assert response_data["ipd_sharing_time_frame"] == "uh"
    assert response_data["ipd_sharing_access_criteria"] == "Study Protocol"
    assert response_data["ipd_sharing_url"] == "1"


# ------------------- LINK METADATA ------------------- #
def test_get_link_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/link' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the link metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/link")

    assert response.status_code == 200


def test_post_link_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/link' endpoint is requested (POST)
    THEN check that the response is valid and creates the link metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
        f"/study/{study_id}/metadata/link",
        json=[{"url": "google.com", "title": "google link"}],
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_link_id = response_data[0]["id"]

    assert response_data[0]["url"] == "google.com"
    assert response_data[0]["title"] == "google link"


def test_delete_link_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID and link ID
    WHEN the '/study/{study_id}/metadata/link/{link_id}' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the link metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    link_id = pytest.global_link_id

    response = _logged_in_client.delete(f"/study/{study_id}/metadata/link/{link_id}")

    assert response.status_code == 204


# ------------------- LOCATION METADATA ------------------- #
def test_get_location_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/location' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the location metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/location")

    assert response.status_code == 200


def test_post_location_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/location' endpoint is requested (POST)
    THEN check that the response is valid and creates the location metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_location_id = response_data[0]["id"]

    assert response_data[0]["facility"] == "test"
    assert response_data[0]["status"] == "Withdrawn"
    assert response_data[0]["city"] == "city"
    assert response_data[0]["state"] == "ca"
    assert response_data[0]["zip"] == "test"
    assert response_data[0]["country"] == "yes"


def test_delete_location_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID and location ID
    WHEN the '/study/{study_id}/metadata/location/{location_id}'
        endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the location metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    location_id = pytest.global_location_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/location/{location_id}"
    )

    assert response.status_code == 204


# ------------------- OTHER METADATA ------------------- #
def test_get_other_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/other' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the other metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/other")

    assert response.status_code == 200


def test_put_other_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/other' endpoint is requested (PUT)
    THEN check that the response is valid and updates the other metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/other",
        json={
            "oversight_has_dmc": False,
            "conditions": ["true", "conditions", "keywords", "1"],
            "keywords": ["true", "u"],
            "size": 103,
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["oversight_has_dmc"] is False
    assert response_data["conditions"] == ["true", "conditions", "keywords", "1"]
    assert response_data["keywords"] == ["true", "u"]
    assert response_data["size"] == 103


# ------------------- OVERALL-OFFICIAL METADATA ------------------- #
def test_get_overall_official_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/overall-official' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the overall-official metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/overall-official")

    assert response.status_code == 200


def test_post_overall_official_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/overall-official' endpoint is requested (POST)
    THEN check that the response is valid and creates the overall-official metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
        f"/study/{study_id}/metadata/overall-official",
        json=[{"name": "test", "affiliation": "aff", "role": "Study Chair"}],
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_overall_official_id = response_data[0]["id"]

    assert response_data[0]["name"] == "test"
    assert response_data[0]["affiliation"] == "aff"
    assert response_data[0]["role"] == "Study Chair"


def test_delete_overall_official_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a
        study ID and overall official ID
    WHEN the '/study/{study_id}/metadata/overall-official/{overall_official_id}'
        endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the overall-official metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    overall_official_id = pytest.global_overall_official_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/overall-official/{overall_official_id}"
    )

    assert response.status_code == 204


# ------------------- OVERSIGHT METADATA ------------------- #
def test_get_oversight_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/oversight' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the oversight metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/oversight")

    assert response.status_code == 200


def test_put_oversight_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/oversight' endpoint is requested (PUT)
    THEN check that the response is valid and updates the oversight metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/oversight", json={"oversight_has_dmc": True}
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data is True


# ------------------- REFERENCE METADATA ------------------- #
def test_get_reference_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/reference' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the reference metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/reference")

    assert response.status_code == 200


def test_post_reference_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/reference' endpoint is requested (POST)
    THEN check that the response is valid and creates the reference metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
        f"/study/{study_id}/metadata/reference",
        json=[
            {
                "identifier": "reference identifier",
                "type": "Yes",
                "citation": "reference citation",
            }
        ],
    )

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_reference_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "reference identifier"
    assert response_data[0]["type"] == "Yes"
    assert response_data[0]["citation"] == "reference citation"


def test_delete_reference_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and
        a study ID and reference ID
    WHEN the '/study/{study_id}/metadata/reference/{reference_id}'
        endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the reference metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore
    reference_id = pytest.global_reference_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/reference/{reference_id}"
    )

    assert response.status_code == 204


# ------------------- SPONSORS METADATA ------------------- #
def test_get_sponsors_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/sponsors' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the sponsors metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/sponsors")

    assert response.status_code == 200


def test_put_sponsors_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/sponsors' endpoint is requested (PUT)
    THEN check that the response is valid and updates the sponsors metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/sponsors",
        json={
            "responsible_party_type": "Sponsor",
            "responsible_party_investigator_name": "party name",
            "responsible_party_investigator_title": "party title",
            "responsible_party_investigator_affiliation": "party affiliation",
            "lead_sponsor_name": "sponsor name",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["responsible_party_type"] == "Sponsor"
    assert response_data["responsible_party_investigator_name"] == "party name"
    assert response_data["responsible_party_investigator_title"] == "party title"
    assert (
        response_data["responsible_party_investigator_affiliation"]
        == "party affiliation"  # noqa: W503
    )
    assert response_data["lead_sponsor_name"] == "sponsor name"


# ------------------- STATUS METADATA ------------------- #
def test_get_status_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/status' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the status metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/status")

    assert response.status_code == 200


def test_put_status_metadata(_logged_in_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/status' endpoint is requested (PUT)
    THEN check that the response is valid and updates the status metadata
    """
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
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

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["overall_status"] == "Withdrawn"
    assert response_data["why_stopped"] == "test"
    assert response_data["start_date"] == "2023-11-15 00:00:00"
    assert response_data["start_date_type"] == "Actual"
    assert response_data["completion_date"] == "2023-11-16 00:00:00"
    assert response_data["completion_date_type"] == "Actual"
