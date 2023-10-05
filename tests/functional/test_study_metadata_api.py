"""Tests for the Study Metadata API endpoints"""
import json

import pytest


# ------------------- ARM METADATA ------------------- #
def test_post_arm_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/arm' endpoint is requested (POST)
    THEN check that the response is vaild and create a new arm
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.post(
        f"/study/{study_id}/metadata/arm",
        json=[
            {
                "label": "Label1",
                "type": "Arm Type",
                "description": "Arm Description",
                "intervention_list": ["intervention1", "intervention2"],
            }
        ],
    )

    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["arms"][0]["type"] == "Arm Type"
    assert response_data["arms"][0]["description"] == "Arm Description"
    assert response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]
    pytest.global_arm_id = response_data["arms"][0]["id"]


def test_get_arm_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/arm/metadata' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the arm metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/arm")
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["arms"][0]["type"] == "Arm Type"
    assert response_data["arms"][0]["description"] == "Arm Description"
    assert response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]


def test_delete_arm_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID and arm ID
    WHEN the '/study/{study_id}/arm/metadata' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the arm metadata
    """
    study_id = pytest.global_study_id["id"]
    arm_id = pytest.global_arm_id
    response = _test_client.delete(f"/study/{study_id}/metadata/arm/{arm_id}")
    assert response.status_code == 200


# ------------------- IPD METADATA ------------------- #
def test_post_available_ipd_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/available-id' endpoint is requested (POST)
    THEN check that the response is vaild and new IPD was created
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.post(
        f"/study/{study_id}/metadata/available-ipd",
        json=[
            {
                "identifier": "identifier1",
                "type": "type1",
                "url": "google.com",
                "comment": "comment1",
            }
        ],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_available_ipd_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "identifier1"
    assert response_data[0]["type"] == "type1"
    assert response_data[0]["url"] == "google.com"
    assert response_data[0]["comment"] == "comment1"


def test_get_available_ipd_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/available-id' endpoint is requested (GET)
    THEN check that the response is vaild and retrieves the available IPD(s)
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/available-ipd")
    assert response.status_code == 200


def test_delete_available_ipd_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and available IPD ID
    WHEN the '/study/{study_id}/metadata/available-id' endpoint is requested (DELETE)
    THEN check that the response is vaild and deletes the available IPD
    """
    study_id = pytest.global_study_id["id"]
    available_ipd_id = pytest.global_available_ipd_id
    response = _test_client.delete(
        f"/study/{study_id}/metadata/available-ipd/{available_ipd_id}"
    )
    assert response.status_code == 204


# ------------------- CENTRAL CONTACT METADATA ------------------- #
def test_post_cc_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/central-contact' endpoint is requested (POST)
    THEN check that the response is valid and creates the central contact metadata
    """
    # BUG: IF CENTRAL_CONTACT IS SET TO FALSE THE ENDPOINT STILL RETURNS AS TRUE
    # BUG: ROLE IS RETURNED AS NONE
    study_id = pytest.global_study_id["id"]
    response = _test_client.post(
        f"/study/{study_id}/metadata/central-contact",
        json=[
            {
                "name": "central-contact",
                "affiliation": "affiliation",
                "role": "role",
                "phone": "phone",
                "phone_ext": "phone_ext",
                "email_address": "email_address",
                "central_contact": True,
            }
        ],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_cc_id = response_data[0]["id"]

    assert response_data[0]["name"] == "central-contact"
    assert response_data[0]["affiliation"] == "affiliation"
    assert response_data[0]["role"] == "role"
    assert response_data[0]["phone"] == "phone"
    assert response_data[0]["phone_ext"] == "phone_ext"
    assert response_data[0]["email_address"] == "email_address"
    assert response_data[0]["central_contact"] == True


def test_get_cc_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/central-contact' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the central contact metadata
    """
    # BUG: ROLE IS RETURNED AS NONE
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/central-contact")
    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data[0]["name"] == "central-contact"
    assert response_data[0]["affiliation"] == "affiliation"
    assert response_data[0]["role"] == "role"
    assert response_data[0]["phone"] == "phone"
    assert response_data[0]["phone_ext"] == "phone_ext"
    assert response_data[0]["email_address"] == "email_address"
    assert response_data[0]["central_contact"] == True


def test_delete_cc_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and central contact ID
    WHEN the '/study/{study_id}/metadata/central-contact/{central_contact_id}' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the central contact metadata
    """
    study_id = pytest.global_study_id["id"]
    central_contact_id = pytest.global_cc_id
    response = _test_client.delete(
        f"/study/{study_id}/metadata/central-contact/{central_contact_id}"
    )
    assert response.status_code == 200


#  ------------------- COLLABORATORS METADATA ------------------- #
def test_get_collaborators_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/collaborators' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the collaborators metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/collaborators")
    assert response.status_code == 200


def test_put_collaborators_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/collaborators' endpoint is requested (POST)
    THEN check that the response is valid and creates the collaborators metadata
    """
    # BUG: ENDPOINT STORES KEY RATHER THAN VALUE
    study_id = pytest.global_study_id["id"]
    response = _test_client.put(
        f"/study/{study_id}/metadata/collaborators",
        json={
            "collaborator_name": "collaborator",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data[0] == "collaborator"


# ------------------- CONDITIONS METADATA ------------------- #
def test_get_conditions_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/conditions' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the conditions metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/conditions")
    assert response.status_code == 200


def test_put_conditions_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/conditions' endpoint is requested (POST)
    THEN check that the response is valid and creates the conditions metadata
    """
    # BUG: ENDPOINT STORES KEY RATHER THAN VALUE
    study_id = pytest.global_study_id["id"]
    response = _test_client.put(
        f"/study/{study_id}/metadata/conditions",
        json={
            "oversight_has_dmc": True,
            "conditions": "conditions",
            "keywords": "keywords",
            "size": "size",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data[0] == True
    assert response_data[1] == "conditions"
    assert response_data[2] == "keywords"
    assert response_data[3] == "size"


# ------------------- DESCRIPTION METADATA ------------------- #
def test_get_description_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/description' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the description metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/description")
    assert response.status_code == 200


def test_put_description_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/description' endpoint is requested (POST)
    THEN check that the response is valid and creates the description metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.put(
        f"/study/{study_id}/metadata/description",
        json={
            "brief_summary": "brief_summary",
            "detailed_description": "detailed_description",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_description_id = response_data["id"]

    assert response_data["brief_summary"] == "brief_summary"
    assert response_data["detailed_description"] == "detailed_description"


# ------------------- DESIGN METADATA ------------------- #
def test_get_design_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/design' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/design")
    assert response.status_code == 200


def test_put_design_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/design' endpoint is requested (PUT)
    THEN check that the response is valid and creates the design metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.put(
        f"/study/{study_id}/metadata/design",
        json={
            "design_allocation": "dfasdfasd",
            "study_type": "dffad",
            "design_intervention_model": "eredf",
            "design_intervention_model_description": "dfadf",
            "design_primary_purpose": "dfasder",
            "design_masking": "dfdasdf",
            "design_masking_description": "tewsfdasf",
            "design_who_masked_list": ["one", "two"],
            "phase_list": ["three", "four"],
            "enrollment_count": 3,
            "enrollment_type": "dfasdf",
            "number_arms": 2,
            "design_observational_model_list": ["yes", "dfasd"],
            "design_time_perspective_list": ["uhh"],
            "bio_spec_retention": "dfasdf",
            "bio_spec_description": "dfasdf",
            "target_duration": "rewrwe",
            "number_groups_cohorts": 1,
        },
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["design_allocation"] == "dfasdfasd"
    assert response_data["study_type"] == "dffad"
    assert response_data["design_intervention_model"] == "eredf"
    assert response_data["design_intervention_model_description"] == "dfadf"
    assert response_data["design_primary_purpose"] == "dfasder"
    assert response_data["design_masking"] == "dfdasdf"
    assert response_data["design_masking_description"] == "tewsfdasf"
    assert response_data["design_who_masked_list"] == ["one", "two"]
    assert response_data["phase_list"] == ["three", "four"]
    assert response_data["enrollment_count"] == 3
    assert response_data["enrollment_type"] == "dfasdf"
    assert response_data["number_arms"] == 2
    assert response_data["design_observational_model_list"] == ["yes", "dfasd"]
    assert response_data["design_time_perspective_list"] == ["uhh"]
    assert response_data["bio_spec_retention"] == "dfasdf"
    assert response_data["bio_spec_description"] == "dfasdf"
    assert response_data["target_duration"] == "rewrwe"
    assert response_data["number_groups_cohorts"] == 1


# ------------------- ELIGIBILITY METADATA ------------------- #
def test_get_eligibility_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/eligibility' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the eligibility metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/eligibility")
    assert response.status_code == 200


def test_put_eligibility_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/eligibility' endpoint is requested (PUT)
    THEN check that the response is valid and updates the eligibility metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.put(
        f"/study/{study_id}/metadata/eligibility",
        json={
            "gender": "nb",
            "gender_based": "no",
            "gender_description": "none",
            "minimum_age_value": 18,
            "maximum_age_value": 61,
            "minimum_age_unit": "1",
            "maximum_age_unit": "2",
            "healthy_volunteers": "3",
            "inclusion_criteria": ["test"],
            "exclusion_criteria": ["test", "ttest"],
            "study_population": "study_population",
            "sampling_method": "test",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["gender"] == "nb"
    assert response_data["gender_based"] == "no"
    assert response_data["gender_description"] == "none"
    assert response_data["minimum_age_value"] == 18
    assert response_data["maximum_age_value"] == 61
    assert response_data["minimum_age_unit"] == "1"
    assert response_data["maximum_age_unit"] == "2"
    assert response_data["healthy_volunteers"] == "3"
    assert response_data["inclusion_criteria"] == ["test"]
    assert response_data["exclusion_criteria"] == ["test", "ttest"]
    assert response_data["study_population"] == "study_population"
    assert response_data["sampling_method"] == "test"


# ------------------- IDENTIFICATION METADATA ------------------- #
def test_get_identification_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/identification' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the identification metadata
    """
    # BUG: ENDPOINT NOT WORKING
    # study_id = pytest.global_study_id["id"]
    # response = _test_client.get(f"/study/{study_id}/metadata/identification")
    # assert response.status_code == 200


def test_post_identification_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/identification' endpoint is requested (POST)
    THEN check that the response is valid and creates the identification metadata
    """
    # BUG: ENDPOINT NOT WORKING
    # study_id = pytest.global_study_id["id"]
    # response = _test_client.post(
    #     f"/study/{study_id}/metadata/identification",
    #     json={
    #         "identifier": "identifier",
    #         "identifier_type": "identifier type",
    #         "identifier_value": "identifier value",
    #         "identifier_link": "identifier link",
    #         "secondary": "secondary"
    #     },
    # )
    # assert response.status_code == 200
    # response_data = json.loads(response.data)
    # pytest.global_identification_id = response_data["id"]


def test_delete_identification_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/identification' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the identification metadata
    """
    # BUG: ENDPOINT NOT WORKING
    # study_id = pytest.global_study_id["id"]
    # idenficiation_id = pytest.global_identification_id
    # response = _test_client.delete(f"/study/{study_id}/metadata/identification/{identification_id}")
    # assert response.status_code == 200


# ------------------- INTERVENTION METADATA ------------------- #
def test_get_intervention_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/intervention' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the intervention metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/intervention")
    assert response.status_code == 200


def test_post_internvertion_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/intervention' endpoint is requested (POST)
    THEN check that the response is valid and creates the intervention metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.post(
        f"/study/{study_id}/metadata/intervention",
        json=[
            {
                "type": "intervention type",
                "name": "intervention name",
                "description": "intervention description",
                "arm_group_list": ["arm group 1", "arm group 2"],
                "other_name_list": ["other name 1", "other name 2"],
            }
        ],
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_intervention_id = response_data[0]["id"]

    assert response_data[0]["type"] == "intervention type"
    assert response_data[0]["name"] == "intervention name"
    assert response_data[0]["description"] == "intervention description"
    assert response_data[0]["arm_group_list"] == ["arm group 1", "arm group 2"]
    assert response_data[0]["other_name_list"] == ["other name 1", "other name 2"]


# ------------------- IPD SHARING METADATA ------------------- #
def test_get_ipdsharing_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/ipdsharing' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the ipdsharing metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/ipdsharing")
    assert response.status_code == 200


def test_put_ipdsharing_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/ipdsharing' endpoint is requested (PUT)
    THEN check that the response is valid and updates the ipdsharing metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.put(
        f"/study/{study_id}/metadata/ipdsharing",
        json={
            "ipd_sharing": "ipd sharing",
            "ipd_sharing_description": "sharing description",
            "ipd_sharing_info_type_list": ["type1", "type2"],
            "ipd_sharing_time_frame": "time frame",
            "ipd_sharing_access_criteria": "access criteria",
            "ipd_sharing_url": "sharing url",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["ipd_sharing"] == "ipd sharing"
    assert response_data["ipd_sharing_description"] == "sharing description"
    assert response_data["ipd_sharing_info_type_list"] == ["type1", "type2"]
    assert response_data["ipd_sharing_time_frame"] == "time frame"
    assert response_data["ipd_sharing_access_criteria"] == "access criteria"
    assert response_data["ipd_sharing_url"] == "sharing url"


# ------------------- LINK METADATA ------------------- #
def test_get_link_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/link' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the link metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/link")
    assert response.status_code == 200


def test_post_link_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/link' endpoint is requested (POST)
    THEN check that the response is valid and creates the link metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.post(
        f"/study/{study_id}/metadata/link", json=[{"url": "url link", "title": "link"}]
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_link_id = response_data[0]["id"]

    assert response_data[0]["url"] == "url"
    assert response_data[0]["description"] == "description"
    assert response_data[0]["link_type"] == "link type"
    assert response_data[0]["label"] == "label"


def test_delete_link_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and link ID
    WHEN the '/study/{study_id}/metadata/link/{link_id}' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the link metadata
    """
    study_id = pytest.global_study_id["id"]
    link_id = pytest.global_link_id
    response = _test_client.delete(f"/study/{study_id}/metadata/link/{link_id}")
    assert response.status_code == 204


# ------------------- LOCATION METADATA ------------------- #
def test_get_location_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/location' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the location metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/location")
    assert response.status_code == 200


def test_post_location_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/location' endpoint is requested (POST)
    THEN check that the response is valid and creates the location metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.post(
        f"/study/{study_id}/metadata/location",
        json=[
            {
                "facility": "facility location",
                "status": "status location",
                "city": "city location",
                "state": "California",
                "zip": "zip location",
                "country": "country location",
            }
        ],
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_location_id = response_data[0]["id"]

    assert response_data[0]["facility"] == "facility location"
    assert response_data[0]["status"] == "status location"
    assert response_data[0]["city"] == "city location"
    assert response_data[0]["state"] == "California"
    assert response_data[0]["zip"] == "zip location"
    assert response_data[0]["country"] == "country location"


def test_delete_location_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and location ID
    WHEN the '/study/{study_id}/metadata/location/{location_id}' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the location metadata
    """
    study_id = pytest.global_study_id["id"]
    location_id = pytest.global_location_id
    response = _test_client.delete(f"/study/{study_id}/metadata/location/{location_id}")
    assert response.status_code == 204


# ------------------- OTHER METADATA ------------------- #
def test_get_other_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/other' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the other metadata
    """
    # BUG: KEYWORDS RETURNS A STRING '[]' INSTEAD OF A LIST
    # BUG: CONDITIONS RETURNS A STRING '[]' INSTEAD OF A LIST (CONDITIONS ENDPOINT IS CAUSING WRONG RESPONSE HERE)
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/other")
    assert response.status_code == 200


def test_put_other_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/other' endpoint is requested (PUT)
    THEN check that the response is valid and updates the other metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.put(
        f"/study/{study_id}/metadata/other",
        json={
            "oversight_has_dmc": False,
            "conditions": ["TESTCONDITION"],
            "keywords": ["TEST"],
            "size": "0",
        },
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["oversight_has_dmc"] is False
    assert response_data["conditions"] == ["TESTCONDITION"]
    assert response_data["keywords"] == ["TEST"]
    assert response_data["size"] == "0"


# ------------------- OVERALL-OFFICIAL METADATA ------------------- #
def test_get_overall_official_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/overall-official' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the overall-official metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/overall-official")
    assert response.status_code == 200


def test_post_overall_official_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/overall-official' endpoint is requested (POST)
    THEN check that the response is valid and creates the overall-official metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.post(
        f"/study/{study_id}/metadata/overall-official",
        json=[
            {
                "name": "official name",
                "affiliation": "official affiliation",
                "role": "official role",
            }
        ],
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_overall_official_id = response_data[0]["id"]

    assert response_data[0]["name"] == "official name"
    assert response_data[0]["affiliation"] == "official affiliation"
    assert response_data[0]["role"] == "official role"


def test_delete_overall_official_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID and overall official ID
    WHEN the '/study/{study_id}/metadata/overall-official/{overall_official_id}' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the overall-official metadata
    """
    study_id = pytest.global_study_id["id"]
    overall_official_id = pytest.global_overall_official_id
    response = _test_client.delete(
        f"/study/{study_id}/metadata/overall-official/{overall_official_id}"
    )
    assert response.status_code == 204


# ------------------- OVERSIGHT METADATA ------------------- #
def test_get_oversight_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/oversight' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the oversight metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/oversight")
    assert response.status_code == 200


def test_put_oversight_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/oversight' endpoint is requested (PUT)
    THEN check that the response is valid and updates the oversight metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.put(
        f"/study/{study_id}/metadata/oversight", json={"oversight_has_dmc": True}
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    print(response)

    assert response_data is True


# ------------------- REFERENCE METADATA ------------------- #
def test_get_reference_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/reference' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the reference metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/reference")
    assert response.status_code == 200


# ------------------- SPONSORS METADATA ------------------- #
def test_get_sponsors_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/sponsors' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the sponsors metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/sponsors")
    assert response.status_code == 200


# ------------------- STATUS METADATA ------------------- #
def test_get_status_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/status' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the status metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/status")
    assert response.status_code == 200
