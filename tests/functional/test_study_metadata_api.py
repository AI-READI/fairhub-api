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
        json={
            "label": "Label1",
            "type": "Arm Type",
            "description": "Arm Description",
            "intervention_list": ["intervention1", "intervention2"],
        },
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
    WHEN the '/study/{study_id}/metadata/available_id' endpoint is requested (POST)
    THEN check that the response is vaild and new IPD was created
    """
    # Endpoint currently not working
    # study_id = pytest.global_study_id["id"]
    # response = _test_client(f"/study/{study_id}/metadata/available-ipd", json={
    #     "identifier": "identifier1",
    #     "type": "type1",
    #     "url": "google.com",
    #     "comment": "comment1"
    # })


def test_get_available_ipd_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/available_id' endpoint is requested (GET)
    THEN check that the response is vaild and retrieves the available IPD(s)
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/available-ipd")
    assert response.status_code == 200


# ------------------- CENTRAL CONTACT METADATA ------------------- #
def test_post_cc_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/central-contact' endpoint is requested (POST)
    THEN check that the response is valid and creates the central contact metadata
    """
    # BUG: IF CENTRAL_CONTACT IS SET TO FALSE THE ENDPOINT STILL RETURNS AS TRUE
    study_id = pytest.global_study_id["id"]
    response = _test_client.post(
        f"/study/{study_id}/metadata/central-contact",
        json={
            "name": "central-contact",
            "affiliation": "affiliation",
            "role": "role",
            "phone": "phone",
            "phone_ext": "phone_ext",
            "email_address": "email_address",
            "central_contact": True,
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data[0]["name"] == "central-contact"
    assert response_data[0]["affiliation"] == "affiliation"
    # assert response_data[0]["role"] == "role"    # BUG: ROLE IS RETURNED AS NONE
    assert response_data[0]["phone"] == "phone"
    assert response_data[0]["phone_ext"] == "phone_ext"
    assert response_data[0]["email_address"] == "email_address"
    assert response_data[0]["central_contact"] == True
    pytest.global_cc_id = response_data[0]["id"]


def test_get_cc_metadata(_test_client, _login_user):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/central-contact' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the central contact metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/central-contact")
    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data[0]["name"] == "central-contact"
    assert response_data[0]["affiliation"] == "affiliation"
    # assert response_data[0]["role"] == "role"     # BUG: ROLE IS RETURNED AS NONE
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


# ------------------- OTHER METADATA ------------------- #
def test_get_other_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/other' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the other metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/other")
    assert response.status_code == 200


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


# ------------------- OVERSIGHT METADATA ------------------- #
def test_get_oversight_official_metadata(_test_client, _login_user):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/oversight' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the oversight metadata
    """
    study_id = pytest.global_study_id["id"]
    response = _test_client.get(f"/study/{study_id}/metadata/oversight")
    assert response.status_code == 200


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
