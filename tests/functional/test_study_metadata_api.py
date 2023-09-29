"""Tests for the Study Metadata API endpoints"""
import json
import pytest

# ------------------- ARM METADATA ------------------- #
def test_post_arm_metadata(test_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/arm' endpoint is requested (POST)
    THEN check that the response is vaild and create a new arm
    """
    study_id = pytest.global_study_id["id"]
    response = test_client.post(f"/study/{study_id}/metadata/arm", json={
        "label": "Label1",
        "type": "Arm Type",
        "description": "Arm Description",
        "intervention_list": ["intervention1", "intervention2"]
    })

    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["arms"][0]["type"] == "Arm Type" 
    assert response_data["arms"][0]["description"] == "Arm Description"
    assert response_data["arms"][0]["intervention_list"] == ["intervention1", "intervention2"]
    pytest.global_arm_id = response_data["arms"][0]["id"]

def test_get_arm_metadata(test_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/arm/metadata' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the arm metadata
    """
    study_id = pytest.global_study_id["id"]
    response = test_client.get(f"/study/{study_id}/metadata/arm")
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["arms"][0]["type"] == "Arm Type" 
    assert response_data["arms"][0]["description"] == "Arm Description"
    assert response_data["arms"][0]["intervention_list"] == ["intervention1", "intervention2"]

def test_delete_arm_metadata(test_client):
    """
    GIVEN a Flask application configured for testing and a study ID and arm ID
    WHEN the '/study/{study_id}/arm/metadata' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the arm metadata
    """
    study_id = pytest.global_study_id["id"]
    arm_id = pytest.global_arm_id
    response = test_client.delete(f"/study/{study_id}/metadata/arm/{arm_id}")
    assert response.status_code == 204


# ------------------- IPD METADATA ------------------- #
def test_post_available_ipd_metadata(test_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/available_id' endpoint is requested (POST)
    THEN check that the response is vaild and new IPD was created
    """
    # Endpoint currently not working
    # study_id = pytest.global_study_id["id"]
    # response = test_client(f"/study/{study_id}/metadata/available_ipd", json={
    #     "identifier": "identifier1",
    #     "type": "type1",
    #     "url": "google.com",
    #     "comment": "comment1"
    # })


def test_get_available_ipd_metadata(test_client):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/available_id' endpoint is requested (GET)
    THEN check that the response is vaild and retrieves the available IPD(s)
    """
    study_id = pytest.global_study_id["id"]
    response = test_client.get(f"/study/{study_id}/metadata/available_ipd")
    assert response.status_code == 200

# ------------------- CENTRAL CONTACT METADATA ------------------- #
def test_get_cc_metadata(test_client):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/central-contact' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the central contact metadata
    """
    study_id = pytest.global_study_id["id"]
    response = test_client.get(f"/study/{study_id}/metadata/central-contact")
    assert response.status_code == 200