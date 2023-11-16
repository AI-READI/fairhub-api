# pylint: disable=too-many-lines
"""Tests for the Study Metadata API endpoints"""
import json

import pytest


# ------------------- ARM METADATA ------------------- #
def test_post_arm_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/arm' endpoint is requested (POST)
    THEN check that the response is vaild and create a new arm
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_arm_id = response_data["arms"][0]["id"]

    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["arms"][0]["type"] == "Experimental"
    assert response_data["arms"][0]["description"] == "Arm Description"
    assert response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/arm",
        json=[
            {
                "label": "Admin Label",
                "type": "Experimental",
                "description": "Arm Description",
                "intervention_list": ["intervention1", "intervention2"],
            }
        ],
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    pytest.global_admin_arm_id_admin = admin_response_data["arms"][1]["id"]

    assert admin_response_data["arms"][1]["label"] == "Admin Label"

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/arm",
        json=[
            {
                "label": "Editor Label",
                "type": "Experimental",
                "description": "Arm Description",
                "intervention_list": ["intervention1", "intervention2"],
            }
        ],
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    pytest.global_editor_arm_id_editor = editor_response_data["arms"][2]["id"]

    assert editor_response_data["arms"][2]["label"] == "Editor Label"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/metadata/arm",
        json=[
            {
                "label": "Viewer Label",
                "type": "Experimental",
                "description": "Arm Description",
                "intervention_list": ["intervention1", "intervention2"],
            }
        ],
    )

    assert viewer_response.status_code == 403


def test_get_arm_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/arm/metadata' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the arm metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/arm")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/arm")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/arm")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/arm")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["arms"][0]["type"] == "Experimental"
    assert response_data["arms"][0]["description"] == "Arm Description"
    assert response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]


def test_delete_arm_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID and arm ID
    WHEN the '/study/{study_id}/arm/metadata' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the arm metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    arm_id = pytest.global_arm_id
    admin_arm_id = pytest.global_admin_arm_id_admin
    editor_arm_id = pytest.global_editor_arm_id_editor
    
    # Verify viewer cannot delete arm
    viewer_response = _viewer_client.delete(f"/study/{study_id}/metadata/arm/{arm_id}")
    response = _logged_in_client.delete(f"/study/{study_id}/metadata/arm/{arm_id}")
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/arm/{admin_arm_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/arm/{editor_arm_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200


# ------------------- IPD METADATA ------------------- #
def test_post_available_ipd_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/available-id' endpoint is requested (POST)
    THEN check that the response is vaild and new IPD was created
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_available_ipd_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "identifier1"
    assert response_data[0]["type"] == "Clinical Study Report"
    assert response_data[0]["url"] == "google.com"
    assert response_data[0]["comment"] == "comment1"

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/available-ipd",
        json=[
            {
                "identifier": "identifier2",
                "type": "Clinical Study Report",
                "url": "google.com",
                "comment": "comment2",
            }
        ],
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    pytest.global_admin_available_ipd_id_admin = admin_response_data[1]["id"]

    assert admin_response_data[1]["identifier"] == "identifier2"
    assert admin_response_data[1]["type"] == "Clinical Study Report"
    assert admin_response_data[1]["url"] == "google.com"
    assert admin_response_data[1]["comment"] == "comment2"

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/available-ipd",
        json=[
            {
                "identifier": "identifier3",
                "type": "Clinical Study Report",
                "url": "google.com",
                "comment": "comment3",
            }
        ],
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    pytest.global_editor_available_ipd_id_editor = editor_response_data[2]["id"]

    assert editor_response_data[2]["identifier"] == "identifier3"
    assert editor_response_data[2]["type"] == "Clinical Study Report"
    assert editor_response_data[2]["url"] == "google.com"
    assert editor_response_data[2]["comment"] == "comment3"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/metadata/available-ipd",
        json=[
            {
                "identifier": "identifier4",
                "type": "Clinical Study Report",
                "url": "google.com",
                "comment": "comment4",
            }
        ],
    )

    assert viewer_response.status_code == 403


def test_get_available_ipd_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/available-id' endpoint is requested (GET)
    THEN check that the response is vaild and retrieves the available IPD(s)
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/available-ipd")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/available-ipd")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/available-ipd")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/available-ipd")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


def test_delete_available_ipd_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and available IPD ID
    WHEN the '/study/{study_id}/metadata/available-id' endpoint is requested (DELETE)
    THEN check that the response is vaild and deletes the available IPD
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    available_ipd_id = pytest.global_available_ipd_id
    admin_avail_ipd = pytest.global_admin_available_ipd_id_admin
    editor_avail_ipd = pytest.global_editor_available_ipd_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/metadata/available-ipd/{available_ipd_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/available-ipd/{available_ipd_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/available-ipd/{admin_avail_ipd}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/available-ipd/{editor_avail_ipd}"
    )

    assert viewer_response == 403
    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200


# ------------------- CENTRAL CONTACT METADATA ------------------- #
def test_post_cc_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/central-contact' endpoint is requested (POST)
    THEN check that the response is valid and creates the central contact metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_cc_id = response_data[0]["id"]

    assert response_data[0]["name"] == "central-contact"
    assert response_data[0]["affiliation"] == "affiliation"
    assert response_data[0]["role"] is None
    assert response_data[0]["phone"] == "808"
    assert response_data[0]["phone_ext"] == "909"
    assert response_data[0]["email_address"] == "sample@gmail.com"
    assert response_data[0]["central_contact"] is True

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/central-contact",
        json=[
            {
                "name": "admin-central-contact",
                "affiliation": "affiliation",
                "role": "role",
                "phone": "808",
                "phone_ext": "909",
                "email_address": "sample1@gmail.com",
            }
        ],
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    pytest.global_admin_cc_id_admin = admin_response_data[1]["id"]

    assert admin_response_data[1]["name"] == "admin-central-contact"
    assert admin_response_data[1]["affiliation"] == "affiliation"
    assert admin_response_data[1]["role"] is None
    assert admin_response_data[1]["phone"] == "808"
    assert admin_response_data[1]["phone_ext"] == "909"
    assert admin_response_data[1]["email_address"] == "sample1@gmail.com"
    assert admin_response_data[1]["central_contact"] is True

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/central-contact",
        json=[
            {
                "name": "editor-central-contact",
                "affiliation": "affiliation",
                "role": "role",
                "phone": "808",
                "phone_ext": "909",
                "email_address": "sample2@gmail.com",
            }
        ],
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    pytest.global_editor_cc_id_editor = editor_response_data[2]["id"]

    assert editor_response_data[2]["name"] == "editor-central-contact"
    assert editor_response_data[2]["affiliation"] == "affiliation"
    assert editor_response_data[2]["role"] is None
    assert editor_response_data[2]["phone"] == "808"
    assert editor_response_data[2]["phone_ext"] == "909"
    assert editor_response_data[2]["email_address"] == "sample2@gmail.com"
    assert editor_response_data[2]["central_contact"] is True


def test_get_cc_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/central-contact' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the central contact metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/central-contact")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/central-contact")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/central-contact")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/central-contact")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data[0]["name"] == "central-contact"
    assert response_data[0]["affiliation"] == "affiliation"
    assert response_data[0]["role"] is None
    assert response_data[0]["phone"] == "808"
    assert response_data[0]["phone_ext"] == "909"
    assert response_data[0]["email_address"] == "sample@gmail.com"
    assert response_data[0]["central_contact"] is True


def test_delete_cc_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
        and central contact ID
    WHEN the '/study/{study_id}/metadata/central-contact/{central_contact_id}'
        endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the central contact metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    central_contact_id = pytest.global_cc_id
    admin_cc_id = pytest.global_admin_cc_id_admin
    editor_cc_id = pytest.global_editor_cc_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/metadata/central-contact/{central_contact_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/central-contact/{central_contact_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/central-contact/{admin_cc_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/central-contact/{editor_cc_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200


#  ------------------- COLLABORATORS METADATA ------------------- #
def test_get_collaborators_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/collaborators' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the collaborators metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/collaborators")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/collaborators")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/collaborators")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/collaborators")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


def test_put_collaborators_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/collaborators'
        endpoint is requested (POST)
    THEN check that the response is valid and creates the collaborators metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    admin_response = _admin_client.put(
        f"/study/{study_id}/metadata/collaborators",
        json=[
            "admin-collaborator1123",
        ],
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data[0] == "admin-collaborator1123"

    editor_response = _editor_client.put(
        f"/study/{study_id}/metadata/collaborators",
        json=[
            "editor-collaborator1123",
        ],
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data[0] == "editor-collaborator1123"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/metadata/collaborators",
        json=[
            "viewer-collaborator1123",
        ],
    )

    assert viewer_response.status_code == 403


# ------------------- CONDITIONS METADATA ------------------- #
def test_get_conditions_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/conditions' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the conditions metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/conditions")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/conditions")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/conditions")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/conditions")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


def test_put_conditions_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/conditions' endpoint is requested (POST)
    THEN check that the response is valid and creates the conditions metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    admin_response = _admin_client.put(
        f"/study/{study_id}/metadata/conditions",
        json=[
            "true",
            "admin-conditions string",
            "admin-keywords string",
            "admin-size string",
        ],
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data[0] == "true"
    assert admin_response_data[1] == "admin-conditions string"
    assert admin_response_data[2] == "admin-keywords string"
    assert admin_response_data[3] == "admin-size string"

    editor_response = _editor_client.put(
        f"/study/{study_id}/metadata/conditions",
        json=[
            "true",
            "editor-conditions string",
            "editor-keywords string",
            "editor-size string",
        ],
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data[0] == "true"
    assert editor_response_data[1] == "editor-conditions string"
    assert editor_response_data[2] == "editor-keywords string"
    assert editor_response_data[3] == "editor-size string"


# ------------------- DESCRIPTION METADATA ------------------- #
def test_get_description_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/description' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the description metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/description")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/description")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/description")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/description")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


def test_put_description_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/description' endpoint is requested (POST)
    THEN check that the response is valid and creates the description metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    admin_response = _admin_client.put(
        f"/study/{study_id}/metadata/description",
        json={
            "brief_summary": "admin-brief_summary",
            "detailed_description": "admin-detailed_description",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["brief_summary"] == "admin-brief_summary"
    assert admin_response_data["detailed_description"] == "admin-detailed_description"

    editor_response = _editor_client.put(
        f"/study/{study_id}/metadata/description",
        json={
            "brief_summary": "editor-brief_summary",
            "detailed_description": "editor-detailed_description",
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["brief_summary"] == "editor-brief_summary"
    assert editor_response_data["detailed_description"] == "editor-detailed_description"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/metadata/description",
        json={
            "brief_summary": "viewer-brief_summary",
            "detailed_description": "viewer-detailed_description",
        },
    )

    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)

    assert viewer_response_data["brief_summary"] == "viewer-brief_summary"
    assert viewer_response_data["detailed_description"] == "viewer-detailed_description"


# ------------------- DESIGN METADATA ------------------- #
def test_get_design_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/design' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the design metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/design")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/design")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/design")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/design")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


def test_put_design_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/design' endpoint is requested (PUT)
    THEN check that the response is valid and creates the design metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    admin_response = _admin_client.put(
        f"/study/{study_id}/metadata/design",
        json={
            "design_allocation": "admin-dfasdfasd",
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

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["design_allocation"] == "admin-dfasdfasd"
    assert admin_response_data["study_type"] == "Interventional"
    assert admin_response_data["design_intervention_model"] == "Treatment"
    assert admin_response_data["design_intervention_model_description"] == "dfadf"
    assert admin_response_data["design_primary_purpose"] == "Parallel Assignment"
    assert admin_response_data["design_masking"] == "Double"
    assert admin_response_data["design_masking_description"] == "tewsfdasf"
    assert admin_response_data["design_who_masked_list"] == ["Participant", "Care Provider"]
    assert admin_response_data["phase_list"] == ["N/A"]
    assert admin_response_data["enrollment_count"] == 3
    assert admin_response_data["enrollment_type"] == "Actual"
    assert admin_response_data["number_arms"] == 2
    assert admin_response_data["design_observational_model_list"] == [
        "Cohort",
        "Case-Control",
    ]
    assert admin_response_data["design_time_perspective_list"] == ["Other"]
    assert admin_response_data["bio_spec_retention"] == "None Retained"
    assert admin_response_data["bio_spec_description"] == "dfasdf"
    assert admin_response_data["target_duration"] == "rewrwe"
    assert admin_response_data["number_groups_cohorts"] == 1

    editor_response = _editor_client.put(
        f"/study/{study_id}/metadata/design",
        json={
            "design_allocation": "editor-dfasdfasd",
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

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["design_allocation"] == "editor-dfasdfasd"
    assert editor_response_data["study_type"] == "Interventional"
    assert editor_response_data["design_intervention_model"] == "Treatment"
    assert editor_response_data["design_intervention_model_description"] == "dfadf"
    assert editor_response_data["design_primary_purpose"] == "Parallel Assignment"
    assert editor_response_data["design_masking"] == "Double"
    assert editor_response_data["design_masking_description"] == "tewsfdasf"
    assert editor_response_data["design_who_masked_list"] == ["Participant", "Care Provider"]
    assert editor_response_data["phase_list"] == ["N/A"]
    assert editor_response_data["enrollment_count"] == 3
    assert editor_response_data["enrollment_type"] == "Actual"
    assert editor_response_data["number_arms"] == 2
    assert editor_response_data["design_observational_model_list"] == [
        "Cohort",
        "Case-Control",
    ]
    assert editor_response_data["design_time_perspective_list"] == ["Other"]
    assert editor_response_data["bio_spec_retention"] == "None Retained"
    assert editor_response_data["bio_spec_description"] == "dfasdf"
    assert editor_response_data["target_duration"] == "rewrwe"
    assert editor_response_data["number_groups_cohorts"] == 1

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/metadata/design",
        json={
            "design_allocation": "viewer-dfasdfasd",
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
        }
    )

    assert viewer_response.status_code == 403


# ------------------- ELIGIBILITY METADATA ------------------- #
def test_get_eligibility_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/eligibility' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the eligibility metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/eligibility")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/eligibility")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/eligibility")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/eligibility")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 403


def test_put_eligibility_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/eligibility' endpoint is requested (PUT)
    THEN check that the response is valid and updates the eligibility metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    admin_response = _admin_client.put(
        f"/study/{study_id}/metadata/eligibility",
        json={
            "gender": "All",
            "gender_based": "Yes",
            "gender_description": "admin-none",
            "minimum_age_value": 18,
            "maximum_age_value": 61,
            "minimum_age_unit": "1",
            "maximum_age_unit": "2",
            "healthy_volunteers": "Yes",
            "inclusion_criteria": ["tests"],
            "exclusion_criteria": ["Probability Sample"],
            "study_population": "study_population",
            "sampling_method": "Probability Sample",
        }
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["gender"] == "All"
    assert admin_response_data["gender_based"] == "Yes"
    assert admin_response_data["gender_description"] == "admin-none"
    assert admin_response_data["minimum_age_value"] == 18
    assert admin_response_data["maximum_age_value"] == 61
    assert admin_response_data["minimum_age_unit"] == "1"
    assert admin_response_data["maximum_age_unit"] == "2"
    assert admin_response_data["healthy_volunteers"] == "Yes"
    assert admin_response_data["inclusion_criteria"] == ["tests"]
    assert admin_response_data["exclusion_criteria"] == ["Probability Sample"]
    assert admin_response_data["study_population"] == "study_population"
    assert admin_response_data["sampling_method"] == "Probability Sample"

    editor_response = _editor_client.put(
        f"/study/{study_id}/metadata/eligibility",
        json={
            "gender": "All",
            "gender_based": "Yes",
            "gender_description": "editor-none",
            "minimum_age_value": 18,
            "maximum_age_value": 61,
            "minimum_age_unit": "1",
            "maximum_age_unit": "2",
            "healthy_volunteers": "Yes",
            "inclusion_criteria": ["tests"],
            "exclusion_criteria": ["Probability Sample"],
            "study_population": "study_population",
            "sampling_method": "Probability Sample",
        }
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["gender"] == "All"
    assert editor_response_data["gender_based"] == "Yes"
    assert editor_response_data["gender_description"] == "editor-none"
    assert editor_response_data["minimum_age_value"] == 18
    assert editor_response_data["maximum_age_value"] == 61
    assert editor_response_data["minimum_age_unit"] == "1"
    assert editor_response_data["maximum_age_unit"] == "2"
    assert editor_response_data["healthy_volunteers"] == "Yes"
    assert editor_response_data["inclusion_criteria"] == ["tests"]
    assert editor_response_data["exclusion_criteria"] == ["Probability Sample"]
    assert editor_response_data["study_population"] == "study_population"
    assert editor_response_data["sampling_method"] == "Probability Sample"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/metadata/eligibility",
        json={
            "gender": "All",
            "gender_based": "Yes",
            "gender_description": "viewer-none",
            "minimum_age_value": 18,
            "maximum_age_value": 61,
            "minimum_age_unit": "1",
            "maximum_age_unit": "2",
            "healthy_volunteers": "Yes",
            "inclusion_criteria": ["tests"],
            "exclusion_criteria": ["Probability Sample"],
            "study_population": "study_population",
            "sampling_method": "Probability Sample",
        }
    )

    assert viewer_response.status_code == 403


# ------------------- IDENTIFICATION METADATA ------------------- #
def test_get_identification_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/identification' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the identification metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/identification")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/identification")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/identification")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/identification")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


def test_post_identification_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/identification' endpoint is requested (POST)
    THEN check that the response is valid and creates the identification metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    assert response.status_code == 200
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

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/identification",
        json={
            "primary": {
                "identifier": "admin-first",
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

    assert admin_response.status_code == 200
    admin_response_data = json.loads(response.data)
    pytest.global_identification_id_admin = response_data["secondary"][1]["id"]

    assert admin_response_data["primary"]["identifier"] == "admin-first"
    assert admin_response_data["primary"]["identifier_type"] == "test"
    assert admin_response_data["primary"]["identifier_domain"] == "domain"
    assert admin_response_data["primary"]["identifier_link"] == "link"
    assert admin_response_data["secondary"][1]["identifier"] == "test"
    assert admin_response_data["secondary"][1]["identifier_type"] == "test"
    assert admin_response_data["secondary"][1]["identifier_domain"] == "dodfasdfmain"
    assert admin_response_data["secondary"][1]["identifier_link"] == "link"

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/identification",
        json={
            "primary": {
                "identifier": "editor-first",
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

    assert editor_response.status_code == 200
    editor_response_data = json.loads(response.data)
    pytest.global_identification_id_editor = response_data["secondary"][2]["id"]

    assert editor_response_data["primary"]["identifier"] == "first"
    assert editor_response_data["primary"]["identifier_type"] == "test"
    assert editor_response_data["primary"]["identifier_domain"] == "domain"
    assert editor_response_data["primary"]["identifier_link"] == "link"
    assert editor_response_data["secondary"][0]["identifier"] == "test"
    assert editor_response_data["secondary"][0]["identifier_type"] == "test"
    assert editor_response_data["secondary"][0]["identifier_domain"] == "dodfasdfmain"
    assert editor_response_data["secondary"][0]["identifier_link"] == "link"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/metadata/identification",
        json={
            "primary": {
                "identifier": "viewer-first",
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

    assert viewer_response.status_code == 403


def test_delete_identification_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/identification' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the identification metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    identification_id = pytest.global_identification_id
    admin_identification_id = pytest.global_identification_id_admin
    editor_identification_id = pytest.global_identification_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/metadata/identification/{identification_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/identification/{identification_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/identification/{admin_identification_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/identification/{editor_identification_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200


# ------------------- INTERVENTION METADATA ------------------- #
def test_get_intervention_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/intervention' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the intervention metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/intervention")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/intervention")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/intervention")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/intervention")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200


def test_post_intervention_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/intervention' endpoint is requested (POST)
    THEN check that the response is valid and creates the intervention metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_intervention_id = response_data[0]["id"]

    assert response_data[0]["type"] == "Device"
    assert response_data[0]["name"] == "name test"
    assert response_data[0]["description"] == "desc"
    assert response_data[0]["arm_group_label_list"] == ["test", "one"]
    assert response_data[0]["other_name_list"] == ["uhh", "yes"]

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/intervention",
        json=[
            {
                "type": "Device",
                "name": "admin-name test",
                "description": "desc",
                "arm_group_label_list": ["test", "one"],
                "other_name_list": ["uhh", "yes"],
            }
        ],
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(response.data)
    pytest.global_intervention_id = response_data[0]["id"]

    assert admin_response_data[0]["type"] == "Device"
    assert admin_response_data[0]["name"] == "admin-name test"
    assert admin_response_data[0]["description"] == "desc"
    assert admin_response_data[0]["arm_group_label_list"] == ["test", "one"]
    assert admin_response_data[0]["other_name_list"] == ["uhh", "yes"]

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/intervention",
        json=[
            {
                "type": "Device",
                "name": "editor-name test",
                "description": "desc",
                "arm_group_label_list": ["test", "one"],
                "other_name_list": ["uhh", "yes"],
            }
        ],
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(response.data)
    pytest.global_intervention_id_editor = response_data[2]["id"]

    assert editor_response_data[2]["type"] == "Device"
    assert editor_response_data[2]["name"] == "editor-name test"
    assert editor_response_data[2]["description"] == "desc"
    assert editor_response_data[2]["arm_group_label_list"] == ["test", "one"]
    assert editor_response_data[2]["other_name_list"] == ["uhh", "yes"]

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/metadata/intervention",
        json=[
            {
                "type": "Device",
                "name": "viewer-name test",
                "description": "desc",
                "arm_group_label_list": ["test", "one"],
                "other_name_list": ["uhh", "yes"],
            }
        ],
    )

    assert viewer_response.status_code == 403


# ------------------- IPD SHARING METADATA ------------------- #
def test_get_ipdsharing_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/ipdsharing' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the ipdsharing metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/ipdsharing")

    assert response.status_code == 200


def test_put_ipdsharing_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/ipdsharing' endpoint is requested (PUT)
    THEN check that the response is valid and updates the ipdsharing metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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
def test_get_link_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/link' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the link metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/link")

    assert response.status_code == 200


def test_post_link_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/link' endpoint is requested (POST)
    THEN check that the response is valid and creates the link metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
        f"/study/{study_id}/metadata/link",
        json=[{"url": "google.com", "title": "google link"}],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_link_id = response_data[0]["id"]

    assert response_data[0]["url"] == "google.com"
    assert response_data[0]["title"] == "google link"


def test_delete_link_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and link ID
    WHEN the '/study/{study_id}/metadata/link/{link_id}' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the link metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    link_id = pytest.global_link_id

    response = _logged_in_client.delete(f"/study/{study_id}/metadata/link/{link_id}")

    assert response.status_code == 200


# ------------------- LOCATION METADATA ------------------- #
def test_get_location_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/location' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the location metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/location")

    assert response.status_code == 200


def test_post_location_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/location' endpoint is requested (POST)
    THEN check that the response is valid and creates the location metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_location_id = response_data[0]["id"]

    assert response_data[0]["facility"] == "test"
    assert response_data[0]["status"] == "Withdrawn"
    assert response_data[0]["city"] == "city"
    assert response_data[0]["state"] == "ca"
    assert response_data[0]["zip"] == "test"
    assert response_data[0]["country"] == "yes"


def test_delete_location_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and location ID
    WHEN the '/study/{study_id}/metadata/location/{location_id}'
        endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the location metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    location_id = pytest.global_location_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/location/{location_id}"
    )

    assert response.status_code == 200


# ------------------- OTHER METADATA ------------------- #
def test_get_other_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/other' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the other metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/other")

    assert response.status_code == 200


def test_put_other_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/other' endpoint is requested (PUT)
    THEN check that the response is valid and updates the other metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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
def test_get_overall_official_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/overall-official' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the overall-official metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/overall-official")

    assert response.status_code == 200


def test_post_overall_official_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/overall-official' endpoint is requested (POST)
    THEN check that the response is valid and creates the overall-official metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
        f"/study/{study_id}/metadata/overall-official",
        json=[{"name": "test", "affiliation": "aff", "role": "Study Chair"}],
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_overall_official_id = response_data[0]["id"]

    assert response_data[0]["name"] == "test"
    assert response_data[0]["affiliation"] == "aff"
    assert response_data[0]["role"] == "Study Chair"


def test_delete_overall_official_metadata(clients):
    """
    Given a Flask application configured for testing and a
        study ID and overall official ID
    WHEN the '/study/{study_id}/metadata/overall-official/{overall_official_id}'
        endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the overall-official metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    overall_official_id = pytest.global_overall_official_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/overall-official/{overall_official_id}"
    )

    assert response.status_code == 200


# ------------------- OVERSIGHT METADATA ------------------- #
def test_get_oversight_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/oversight' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the oversight metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/oversight")

    assert response.status_code == 200


def test_put_oversight_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/oversight' endpoint is requested (PUT)
    THEN check that the response is valid and updates the oversight metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/oversight", json={"oversight_has_dmc": True}
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data is True


# ------------------- REFERENCE METADATA ------------------- #
def test_get_reference_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/reference' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the reference metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/reference")

    assert response.status_code == 200


def test_post_reference_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/reference' endpoint is requested (POST)
    THEN check that the response is valid and creates the reference metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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

    assert response.status_code == 200
    response_data = json.loads(response.data)
    pytest.global_reference_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "reference identifier"
    assert response_data[0]["type"] == "Yes"
    assert response_data[0]["citation"] == "reference citation"


def test_delete_reference_metadata(clients):
    """
    Given a Flask application configured for testing and
        a study ID and reference ID
    WHEN the '/study/{study_id}/metadata/reference/{reference_id}'
        endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the reference metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    reference_id = pytest.global_reference_id

    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/reference/{reference_id}"
    )

    assert response.status_code == 200


# ------------------- SPONSORS METADATA ------------------- #
def test_get_sponsors_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/sponsors' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the sponsors metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/sponsors")

    assert response.status_code == 200


def test_put_sponsors_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/sponsors' endpoint is requested (PUT)
    THEN check that the response is valid and updates the sponsors metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
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
def test_get_status_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/status' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the status metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/status")

    assert response.status_code == 200


def test_put_status_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/status' endpoint is requested (PUT)
    THEN check that the response is valid and updates the status metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/status",
        json={
            "overall_status": "Withdrawn",
            "why_stopped": "test",
            "start_date": "fff",
            "start_date_type": "Actual",
            "completion_date": "nuzzzll",
            "completion_date_type": "Actual",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["overall_status"] == "Withdrawn"
    assert response_data["why_stopped"] == "test"
    assert response_data["start_date"] == "fff"
    assert response_data["start_date_type"] == "Actual"
    assert response_data["completion_date"] == "nuzzzll"
    assert response_data["completion_date_type"] == "Actual"
