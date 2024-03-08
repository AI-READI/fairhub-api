# pylint: disable=too-many-lines
"""Tests for the Study Metadata API endpoints"""
import json
from time import sleep

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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
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

    assert editor_response.status_code == 201
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
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["arms"][0]["id"] == pytest.global_arm_id
    assert response_data["arms"][0]["label"] == "Label1"
    assert response_data["arms"][0]["type"] == "Experimental"
    assert response_data["arms"][0]["description"] == "Arm Description"
    assert response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]
    assert response_data["arms"][1]["id"] == pytest.global_admin_arm_id_admin
    assert response_data["arms"][1]["label"] == "Admin Label"
    assert response_data["arms"][1]["type"] == "Experimental"
    assert response_data["arms"][1]["description"] == "Arm Description"
    assert response_data["arms"][1]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]
    assert response_data["arms"][2]["id"] == pytest.global_editor_arm_id_editor
    assert response_data["arms"][2]["label"] == "Editor Label"
    assert response_data["arms"][2]["type"] == "Experimental"
    assert response_data["arms"][2]["description"] == "Arm Description"
    assert response_data["arms"][2]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]

    assert admin_response_data["arms"][0]["id"] == pytest.global_arm_id
    assert admin_response_data["arms"][0]["label"] == "Label1"
    assert admin_response_data["arms"][0]["type"] == "Experimental"
    assert admin_response_data["arms"][0]["description"] == "Arm Description"
    assert admin_response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]
    assert admin_response_data["arms"][1]["id"] == pytest.global_admin_arm_id_admin
    assert admin_response_data["arms"][1]["label"] == "Admin Label"
    assert admin_response_data["arms"][1]["type"] == "Experimental"
    assert admin_response_data["arms"][1]["description"] == "Arm Description"
    assert admin_response_data["arms"][1]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]
    assert admin_response_data["arms"][2]["id"] == pytest.global_editor_arm_id_editor
    assert admin_response_data["arms"][2]["label"] == "Editor Label"
    assert admin_response_data["arms"][2]["type"] == "Experimental"
    assert admin_response_data["arms"][2]["description"] == "Arm Description"
    assert admin_response_data["arms"][2]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]

    assert editor_response_data["arms"][0]["id"] == pytest.global_arm_id
    assert editor_response_data["arms"][0]["label"] == "Label1"
    assert editor_response_data["arms"][0]["type"] == "Experimental"
    assert editor_response_data["arms"][0]["description"] == "Arm Description"
    assert editor_response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]
    assert editor_response_data["arms"][1]["id"] == pytest.global_admin_arm_id_admin
    assert editor_response_data["arms"][1]["label"] == "Admin Label"
    assert editor_response_data["arms"][1]["type"] == "Experimental"
    assert editor_response_data["arms"][1]["description"] == "Arm Description"
    assert editor_response_data["arms"][1]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]
    assert editor_response_data["arms"][2]["id"] == pytest.global_editor_arm_id_editor
    assert editor_response_data["arms"][2]["label"] == "Editor Label"
    assert editor_response_data["arms"][2]["type"] == "Experimental"
    assert editor_response_data["arms"][2]["description"] == "Arm Description"
    assert editor_response_data["arms"][2]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]

    assert viewer_response_data["arms"][0]["id"] == pytest.global_arm_id
    assert viewer_response_data["arms"][0]["label"] == "Label1"
    assert viewer_response_data["arms"][0]["type"] == "Experimental"
    assert viewer_response_data["arms"][0]["description"] == "Arm Description"
    assert viewer_response_data["arms"][0]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]
    assert viewer_response_data["arms"][1]["id"] == pytest.global_admin_arm_id_admin
    assert viewer_response_data["arms"][1]["label"] == "Admin Label"
    assert viewer_response_data["arms"][1]["type"] == "Experimental"
    assert viewer_response_data["arms"][1]["description"] == "Arm Description"
    assert viewer_response_data["arms"][1]["intervention_list"] == [
        "intervention1",
        "intervention2",
    ]
    assert viewer_response_data["arms"][2]["id"] == pytest.global_editor_arm_id_editor
    assert viewer_response_data["arms"][2]["label"] == "Editor Label"
    assert viewer_response_data["arms"][2]["type"] == "Experimental"
    assert viewer_response_data["arms"][2]["description"] == "Arm Description"
    assert viewer_response_data["arms"][2]["intervention_list"] == [
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
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_cc_id = response_data[0]["id"]

    assert response_data[0]["affiliation"] == "affiliation"
    assert response_data[0]["phone"] == "808"
    assert response_data[0]["phone_ext"] == "909"
    assert response_data[0]["email_address"] == "sample@gmail.com"
    assert response_data[0]["first_name"] == "central-contact"
    assert response_data[0]["last_name"] == "central-contact"
    assert response_data[0]["degree"] == "degree"
    assert response_data[0]["identifier"] == "central-contact"
    assert response_data[0]["identifier_scheme"] == "id"
    assert response_data[0]["identifier_scheme_uri"] == "uri"
    assert response_data[0]["affiliation_identifier"] == "affiliation identifier"
    assert (
        response_data[0]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        response_data[0]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/central-contact",
        json=[
            {
                "affiliation": "affiliation",
                "phone": "808",
                "phone_ext": "909",
                "email_address": "sample@gmail.com",
                "first_name": "admin-central-contact",
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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_admin_cc_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["affiliation"] == "affiliation"
    assert admin_response_data[0]["phone"] == "808"
    assert admin_response_data[0]["phone_ext"] == "909"
    assert admin_response_data[0]["email_address"] == "sample@gmail.com"
    assert admin_response_data[0]["first_name"] == "admin-central-contact"
    assert admin_response_data[0]["last_name"] == "central-contact"
    assert admin_response_data[0]["degree"] == "degree"
    assert admin_response_data[0]["identifier"] == "central-contact"
    assert admin_response_data[0]["identifier_scheme"] == "id"
    assert admin_response_data[0]["identifier_scheme_uri"] == "uri"
    assert admin_response_data[0]["affiliation_identifier"] == "affiliation identifier"
    assert (
        admin_response_data[0]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        admin_response_data[0]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/central-contact",
        json=[
            {
                "affiliation": "affiliation",
                "phone": "808",
                "phone_ext": "909",
                "email_address": "sample@gmail.com",
                "first_name": "editor-central-contact",
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

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_editor_cc_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["affiliation"] == "affiliation"
    assert editor_response_data[0]["phone"] == "808"
    assert editor_response_data[0]["phone_ext"] == "909"
    assert editor_response_data[0]["email_address"] == "sample@gmail.com"
    assert editor_response_data[0]["first_name"] == "editor-central-contact"
    assert editor_response_data[0]["last_name"] == "central-contact"
    assert editor_response_data[0]["degree"] == "degree"
    assert editor_response_data[0]["identifier"] == "central-contact"
    assert editor_response_data[0]["identifier_scheme"] == "id"
    assert editor_response_data[0]["identifier_scheme_uri"] == "uri"
    assert editor_response_data[0]["affiliation_identifier"] == "affiliation identifier"
    assert (
        editor_response_data[0]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        editor_response_data[0]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )


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
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["affiliation"] == "affiliation"
    assert response_data[0]["phone"] == "808"
    assert response_data[0]["phone_ext"] == "909"
    assert response_data[0]["email_address"] == "sample@gmail.com"
    assert response_data[0]["first_name"] == "central-contact"
    assert response_data[0]["last_name"] == "central-contact"
    assert response_data[0]["degree"] == "degree"
    assert response_data[0]["identifier"] == "central-contact"
    assert response_data[0]["identifier_scheme"] == "id"
    assert response_data[0]["identifier_scheme_uri"] == "uri"
    assert response_data[0]["affiliation_identifier"] == "affiliation identifier"
    assert (
        response_data[0]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        response_data[0]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert admin_response_data[0]["affiliation"] == "affiliation"
    assert admin_response_data[0]["phone"] == "808"
    assert admin_response_data[0]["phone_ext"] == "909"
    assert admin_response_data[0]["email_address"] == "sample@gmail.com"
    assert admin_response_data[0]["first_name"] == "central-contact"
    assert admin_response_data[0]["last_name"] == "central-contact"
    assert admin_response_data[0]["degree"] == "degree"
    assert admin_response_data[0]["identifier"] == "central-contact"
    assert admin_response_data[0]["identifier_scheme"] == "id"
    assert admin_response_data[0]["identifier_scheme_uri"] == "uri"
    assert admin_response_data[0]["affiliation_identifier"] == "affiliation identifier"
    assert (
        admin_response_data[0]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        admin_response_data[0]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert editor_response_data[0]["affiliation"] == "affiliation"
    assert editor_response_data[0]["phone"] == "808"
    assert editor_response_data[0]["phone_ext"] == "909"
    assert editor_response_data[0]["email_address"] == "sample@gmail.com"
    assert editor_response_data[0]["first_name"] == "central-contact"
    assert editor_response_data[0]["last_name"] == "central-contact"
    assert editor_response_data[0]["degree"] == "degree"
    assert editor_response_data[0]["identifier"] == "central-contact"
    assert editor_response_data[0]["identifier_scheme"] == "id"
    assert editor_response_data[0]["identifier_scheme_uri"] == "uri"
    assert editor_response_data[0]["affiliation_identifier"] == "affiliation identifier"
    assert (
        editor_response_data[0]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        editor_response_data[0]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert viewer_response_data[0]["affiliation"] == "affiliation"
    assert viewer_response_data[0]["phone"] == "808"
    assert viewer_response_data[0]["phone_ext"] == "909"
    assert viewer_response_data[0]["email_address"] == "sample@gmail.com"
    assert viewer_response_data[0]["first_name"] == "central-contact"
    assert viewer_response_data[0]["last_name"] == "central-contact"
    assert viewer_response_data[0]["degree"] == "degree"
    assert viewer_response_data[0]["identifier"] == "central-contact"
    assert viewer_response_data[0]["identifier_scheme"] == "id"
    assert viewer_response_data[0]["identifier_scheme_uri"] == "uri"
    assert viewer_response_data[0]["affiliation_identifier"] == "affiliation identifier"
    assert (
        viewer_response_data[0]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        viewer_response_data[0]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert response_data[1]["affiliation"] == "affiliation"
    assert response_data[1]["phone"] == "808"
    assert response_data[1]["phone_ext"] == "909"
    assert response_data[1]["email_address"] == "sample@gmail.com"
    assert response_data[1]["first_name"] == "admin-central-contact"
    assert response_data[1]["last_name"] == "central-contact"
    assert response_data[1]["degree"] == "degree"
    assert response_data[1]["identifier"] == "central-contact"
    assert response_data[1]["identifier_scheme"] == "id"
    assert response_data[1]["identifier_scheme_uri"] == "uri"
    assert response_data[1]["affiliation_identifier"] == "affiliation identifier"
    assert (
        response_data[1]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        response_data[1]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert admin_response_data[1]["affiliation"] == "affiliation"
    assert admin_response_data[1]["phone"] == "808"
    assert admin_response_data[1]["phone_ext"] == "909"
    assert admin_response_data[1]["email_address"] == "sample@gmail.com"
    assert admin_response_data[1]["first_name"] == "admin-central-contact"
    assert admin_response_data[1]["last_name"] == "central-contact"
    assert admin_response_data[1]["degree"] == "degree"
    assert admin_response_data[1]["identifier"] == "central-contact"
    assert admin_response_data[1]["identifier_scheme"] == "id"
    assert admin_response_data[1]["identifier_scheme_uri"] == "uri"
    assert admin_response_data[1]["affiliation_identifier"] == "affiliation identifier"
    assert (
        admin_response_data[1]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        admin_response_data[1]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert editor_response_data[1]["affiliation"] == "affiliation"
    assert editor_response_data[1]["phone"] == "808"
    assert editor_response_data[1]["phone_ext"] == "909"
    assert editor_response_data[1]["email_address"] == "sample@gmail.com"
    assert editor_response_data[1]["first_name"] == "admin-central-contact"
    assert editor_response_data[1]["last_name"] == "central-contact"
    assert editor_response_data[1]["degree"] == "degree"
    assert editor_response_data[1]["identifier"] == "central-contact"
    assert editor_response_data[1]["identifier_scheme"] == "id"
    assert editor_response_data[1]["identifier_scheme_uri"] == "uri"
    assert editor_response_data[1]["affiliation_identifier"] == "affiliation identifier"
    assert (
        editor_response_data[1]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        editor_response_data[1]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert viewer_response_data[1]["affiliation"] == "affiliation"
    assert viewer_response_data[1]["phone"] == "808"
    assert viewer_response_data[1]["phone_ext"] == "909"
    assert viewer_response_data[1]["email_address"] == "sample@gmail.com"
    assert viewer_response_data[1]["first_name"] == "admin-central-contact"
    assert viewer_response_data[1]["last_name"] == "central-contact"
    assert viewer_response_data[1]["degree"] == "degree"
    assert viewer_response_data[1]["identifier"] == "central-contact"
    assert viewer_response_data[1]["identifier_scheme"] == "id"
    assert viewer_response_data[1]["identifier_scheme_uri"] == "uri"
    assert viewer_response_data[1]["affiliation_identifier"] == "affiliation identifier"
    assert (
        viewer_response_data[1]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        viewer_response_data[1]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert response_data[2]["affiliation"] == "affiliation"
    assert response_data[2]["phone"] == "808"
    assert response_data[2]["phone_ext"] == "909"
    assert response_data[2]["email_address"] == "sample@gmail.com"
    assert response_data[2]["first_name"] == "editor-central-contact"
    assert response_data[2]["last_name"] == "central-contact"
    assert response_data[2]["degree"] == "degree"
    assert response_data[2]["identifier"] == "central-contact"
    assert response_data[2]["identifier_scheme"] == "id"
    assert response_data[2]["identifier_scheme_uri"] == "uri"
    assert response_data[2]["affiliation_identifier"] == "affiliation identifier"
    assert (
        response_data[2]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        response_data[2]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert admin_response_data[2]["affiliation"] == "affiliation"
    assert admin_response_data[2]["phone"] == "808"
    assert admin_response_data[2]["phone_ext"] == "909"
    assert admin_response_data[2]["email_address"] == "sample@gmail.com"
    assert admin_response_data[2]["first_name"] == "editor-central-contact"
    assert admin_response_data[2]["last_name"] == "central-contact"
    assert admin_response_data[2]["degree"] == "degree"
    assert admin_response_data[2]["identifier"] == "central-contact"
    assert admin_response_data[2]["identifier_scheme"] == "id"
    assert admin_response_data[2]["identifier_scheme_uri"] == "uri"
    assert admin_response_data[2]["affiliation_identifier"] == "affiliation identifier"
    assert (
        admin_response_data[2]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        admin_response_data[2]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert editor_response_data[2]["affiliation"] == "affiliation"
    assert editor_response_data[2]["phone"] == "808"
    assert editor_response_data[2]["phone_ext"] == "909"
    assert editor_response_data[2]["email_address"] == "sample@gmail.com"
    assert editor_response_data[2]["first_name"] == "editor-central-contact"
    assert editor_response_data[2]["last_name"] == "central-contact"
    assert editor_response_data[2]["degree"] == "degree"
    assert editor_response_data[2]["identifier"] == "central-contact"
    assert editor_response_data[2]["identifier_scheme"] == "id"
    assert editor_response_data[2]["identifier_scheme_uri"] == "uri"
    assert editor_response_data[2]["affiliation_identifier"] == "affiliation identifier"
    assert (
        editor_response_data[2]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        editor_response_data[2]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )

    assert viewer_response_data[2]["affiliation"] == "affiliation"
    assert viewer_response_data[2]["phone"] == "808"
    assert viewer_response_data[2]["phone_ext"] == "909"
    assert viewer_response_data[2]["email_address"] == "sample@gmail.com"
    assert viewer_response_data[2]["first_name"] == "editor-central-contact"
    assert viewer_response_data[2]["last_name"] == "central-contact"
    assert viewer_response_data[2]["degree"] == "degree"
    assert viewer_response_data[2]["identifier"] == "central-contact"
    assert viewer_response_data[2]["identifier_scheme"] == "id"
    assert viewer_response_data[2]["identifier_scheme_uri"] == "uri"
    assert viewer_response_data[2]["affiliation_identifier"] == "affiliation identifier"
    assert (
        viewer_response_data[2]["affiliation_identifier_scheme"]
        == "affiliation identifier scheme"
    )
    assert (
        viewer_response_data[2]["affiliation_identifier_scheme_uri"]
        == "affiliation identifier scheme uri"
    )


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
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


#  ------------------- COLLABORATORS METADATA ------------------- #
def test_post_collaborators_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/collaborators'
        endpoint is requested (POST)
    THEN check that the response is valid and creates the collaborators metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_collaborators_id = response_data[0]["id"]

    assert response_data[0]["name"] == "collaborator1123"
    assert response_data[0]["identifier"] == "collaborator1123"
    assert response_data[0]["scheme"] == "collaborator1123"
    assert response_data[0]["scheme_uri"] == "collaborator1123"

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/collaborators",
        json=[
            {
                "name": "admin collaborator1123",
                "identifier": "collaborator1123",
                "identifier_scheme": "collaborator1123",
                "identifier_scheme_uri": "collaborator1123",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_admin_collaborators_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["name"] == "admin collaborator1123"
    assert admin_response_data[0]["identifier"] == "collaborator1123"
    assert admin_response_data[0]["scheme"] == "collaborator1123"
    assert admin_response_data[0]["scheme_uri"] == "collaborator1123"

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/collaborators",
        json=[
            {
                "name": "editor collaborator1123",
                "identifier": "collaborator1123",
                "identifier_scheme": "collaborator1123",
                "identifier_scheme_uri": "collaborator1123",
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_editor_collaborators_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["name"] == "editor collaborator1123"
    assert editor_response_data[0]["identifier"] == "collaborator1123"
    assert editor_response_data[0]["scheme"] == "collaborator1123"
    assert editor_response_data[0]["scheme_uri"] == "collaborator1123"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/metadata/collaborators",
        json=[
            {
                "name": "editor collaborator1123",
                "identifier": "collaborator1123",
                "identifier_scheme": "collaborator1123",
                "identifier_scheme_uri": "collaborator1123",
            }
        ],
    )

    assert viewer_response.status_code == 403


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

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["name"] == "collaborator1123"
    assert response_data[0]["identifier"] == "collaborator1123"
    assert response_data[0]["scheme"] == "collaborator1123"
    assert response_data[0]["scheme_uri"] == "collaborator1123"

    assert admin_response_data[0]["name"] == "collaborator1123"
    assert admin_response_data[0]["identifier"] == "collaborator1123"
    assert admin_response_data[0]["scheme"] == "collaborator1123"
    assert admin_response_data[0]["scheme_uri"] == "collaborator1123"

    assert editor_response_data[0]["name"] == "collaborator1123"
    assert editor_response_data[0]["identifier"] == "collaborator1123"
    assert editor_response_data[0]["scheme"] == "collaborator1123"
    assert editor_response_data[0]["scheme_uri"] == "collaborator1123"

    assert viewer_response_data[0]["name"] == "collaborator1123"
    assert viewer_response_data[0]["identifier"] == "collaborator1123"
    assert viewer_response_data[0]["scheme"] == "collaborator1123"
    assert viewer_response_data[0]["scheme_uri"] == "collaborator1123"

    assert response_data[1]["name"] == "admin collaborator1123"
    assert response_data[1]["identifier"] == "collaborator1123"
    assert response_data[1]["scheme"] == "collaborator1123"
    assert response_data[1]["scheme_uri"] == "collaborator1123"

    assert admin_response_data[1]["name"] == "admin collaborator1123"
    assert admin_response_data[1]["identifier"] == "collaborator1123"
    assert admin_response_data[1]["scheme"] == "collaborator1123"
    assert admin_response_data[1]["scheme_uri"] == "collaborator1123"

    assert editor_response_data[1]["name"] == "admin collaborator1123"
    assert editor_response_data[1]["identifier"] == "collaborator1123"
    assert editor_response_data[1]["scheme"] == "collaborator1123"
    assert editor_response_data[1]["scheme_uri"] == "collaborator1123"

    assert viewer_response_data[1]["name"] == "admin collaborator1123"
    assert viewer_response_data[1]["identifier"] == "collaborator1123"
    assert viewer_response_data[1]["scheme"] == "collaborator1123"
    assert viewer_response_data[1]["scheme_uri"] == "collaborator1123"

    assert response_data[2]["name"] == "editor collaborator1123"
    assert response_data[2]["identifier"] == "collaborator1123"
    assert response_data[2]["scheme"] == "collaborator1123"
    assert response_data[2]["scheme_uri"] == "collaborator1123"

    assert admin_response_data[2]["name"] == "editor collaborator1123"
    assert admin_response_data[2]["identifier"] == "collaborator1123"
    assert admin_response_data[2]["scheme"] == "collaborator1123"
    assert admin_response_data[2]["scheme_uri"] == "collaborator1123"

    assert editor_response_data[2]["name"] == "editor collaborator1123"
    assert editor_response_data[2]["identifier"] == "collaborator1123"
    assert editor_response_data[2]["scheme"] == "collaborator1123"
    assert editor_response_data[2]["scheme_uri"] == "collaborator1123"

    assert viewer_response_data[2]["name"] == "editor collaborator1123"
    assert viewer_response_data[2]["identifier"] == "collaborator1123"
    assert viewer_response_data[2]["scheme"] == "collaborator1123"
    assert viewer_response_data[2]["scheme_uri"] == "collaborator1123"


def test_delete_collaborators_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/collaborators' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the identification metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    collaborators_id = pytest.global_collaborators_id
    admin_collaborators_id = pytest.global_admin_collaborators_id_admin
    editor_collaborators_id = pytest.global_editor_collaborators_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/metadata/collaborators/{collaborators_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/collaborators/{collaborators_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/collaborators/{admin_collaborators_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/collaborators/{editor_collaborators_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# # ------------------- CONDITIONS METADATA ------------------- #
def test_post_conditions_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/conditions' endpoint is requested (POST)
    THEN check that the response is valid and creates the conditions metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
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

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_conditions_id = response_data[0]["id"]

    assert response_data[0]["name"] == "condition"
    assert response_data[0]["classification_code"] == "classification code"
    assert response_data[0]["scheme"] == "scheme"
    assert response_data[0]["scheme_uri"] == "scheme uri"
    assert response_data[0]["condition_uri"] == "condition"

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/conditions",
        json=[
            {
                "name": "admin condition",
                "classification_code": "classification code",
                "scheme": "scheme",
                "scheme_uri": "scheme uri",
                "condition_uri": "condition",
            }
        ],
    )

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_admin_conditions_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["name"] == "admin condition"
    assert admin_response_data[0]["classification_code"] == "classification code"
    assert admin_response_data[0]["scheme"] == "scheme"
    assert admin_response_data[0]["scheme_uri"] == "scheme uri"
    assert admin_response_data[0]["condition_uri"] == "condition"

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/conditions",
        json=[
            {
                "name": "editor condition",
                "classification_code": "classification code",
                "scheme": "scheme",
                "scheme_uri": "scheme uri",
                "condition_uri": "condition",
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_editor_conditions_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["name"] == "editor condition"
    assert editor_response_data[0]["classification_code"] == "classification code"
    assert editor_response_data[0]["scheme"] == "scheme"
    assert editor_response_data[0]["scheme_uri"] == "scheme uri"
    assert editor_response_data[0]["condition_uri"] == "condition"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/metadata/conditions",
        json=[
            {
                "name": "editor condition",
                "classification_code": "classification code",
                "scheme": "scheme",
                "scheme_uri": "scheme uri",
                "condition_uri": "condition",
            }
        ],
    )

    assert viewer_response.status_code == 403


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

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["name"] == "condition"
    assert response_data[0]["classification_code"] == "classification code"
    assert response_data[0]["scheme"] == "scheme"
    assert response_data[0]["scheme_uri"] == "scheme uri"
    assert response_data[0]["condition_uri"] == "condition"

    assert admin_response_data[0]["name"] == "condition"
    assert admin_response_data[0]["classification_code"] == "classification code"
    assert admin_response_data[0]["scheme"] == "scheme"
    assert admin_response_data[0]["scheme_uri"] == "scheme uri"
    assert admin_response_data[0]["condition_uri"] == "condition"

    assert editor_response_data[0]["name"] == "condition"
    assert editor_response_data[0]["classification_code"] == "classification code"
    assert editor_response_data[0]["scheme"] == "scheme"
    assert editor_response_data[0]["scheme_uri"] == "scheme uri"
    assert editor_response_data[0]["condition_uri"] == "condition"

    assert viewer_response_data[0]["name"] == "condition"
    assert viewer_response_data[0]["classification_code"] == "classification code"
    assert viewer_response_data[0]["scheme"] == "scheme"
    assert viewer_response_data[0]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[0]["condition_uri"] == "condition"

    assert response_data[1]["name"] == "admin condition"
    assert response_data[1]["classification_code"] == "classification code"
    assert response_data[1]["scheme"] == "scheme"
    assert response_data[1]["scheme_uri"] == "scheme uri"
    assert response_data[1]["condition_uri"] == "condition"

    assert admin_response_data[1]["name"] == "admin condition"
    assert admin_response_data[1]["classification_code"] == "classification code"
    assert admin_response_data[1]["scheme"] == "scheme"
    assert admin_response_data[1]["scheme_uri"] == "scheme uri"
    assert admin_response_data[1]["condition_uri"] == "condition"

    assert editor_response_data[1]["name"] == "admin condition"
    assert editor_response_data[1]["classification_code"] == "classification code"
    assert editor_response_data[1]["scheme"] == "scheme"
    assert editor_response_data[1]["scheme_uri"] == "scheme uri"
    assert editor_response_data[1]["condition_uri"] == "condition"

    assert viewer_response_data[1]["name"] == "admin condition"
    assert viewer_response_data[1]["classification_code"] == "classification code"
    assert viewer_response_data[1]["scheme"] == "scheme"
    assert viewer_response_data[1]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[1]["condition_uri"] == "condition"

    assert response_data[2]["name"] == "editor condition"
    assert response_data[2]["classification_code"] == "classification code"
    assert response_data[2]["scheme"] == "scheme"
    assert response_data[2]["scheme_uri"] == "scheme uri"
    assert response_data[2]["condition_uri"] == "condition"

    assert admin_response_data[2]["name"] == "editor condition"
    assert admin_response_data[2]["classification_code"] == "classification code"
    assert admin_response_data[2]["scheme"] == "scheme"
    assert admin_response_data[2]["scheme_uri"] == "scheme uri"
    assert admin_response_data[2]["condition_uri"] == "condition"

    assert editor_response_data[2]["name"] == "editor condition"
    assert editor_response_data[2]["classification_code"] == "classification code"
    assert editor_response_data[2]["scheme"] == "scheme"
    assert editor_response_data[2]["scheme_uri"] == "scheme uri"
    assert editor_response_data[2]["condition_uri"] == "condition"

    assert viewer_response_data[2]["name"] == "editor condition"
    assert viewer_response_data[2]["classification_code"] == "classification code"
    assert viewer_response_data[2]["scheme"] == "scheme"
    assert viewer_response_data[2]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[2]["condition_uri"] == "condition"


def test_delete_conditions_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/conditions' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the identification metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    conditions_id = pytest.global_conditions_id
    admin_conditions_id = pytest.global_admin_conditions_id_admin
    editor_conditions_id = pytest.global_editor_conditions_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/metadata/conditions/{conditions_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/conditions/{conditions_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/conditions/{admin_conditions_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/conditions/{editor_conditions_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- KEYWORDS METADATA ------------------- #
def test_post_keywords_metadata(clients):
    """
    GIVEN a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/keywords' endpoint is requested (POST)
    THEN check that the response is valid and creates the keywords metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.post(
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
    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_keywords_id = response_data[0]["id"]

    assert response_data[0]["name"] == "keywords"
    assert response_data[0]["classification_code"] == "classification code"
    assert response_data[0]["scheme"] == "scheme"
    assert response_data[0]["scheme_uri"] == "scheme uri"
    assert response_data[0]["keyword_uri"] == "keywords"

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/keywords",
        json=[
            {
                "name": "admin keywords",
                "classification_code": "classification code",
                "scheme": "scheme",
                "scheme_uri": "scheme uri",
                "keyword_uri": "keywords",
            }
        ],
    )

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_admin_keywords_id_admin = admin_response_data[0]["id"]
    assert admin_response_data[0]["name"] == "admin keywords"
    assert admin_response_data[0]["classification_code"] == "classification code"
    assert admin_response_data[0]["scheme"] == "scheme"
    assert admin_response_data[0]["scheme_uri"] == "scheme uri"
    assert admin_response_data[0]["keyword_uri"] == "keywords"

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/keywords",
        json=[
            {
                "name": "editor keywords",
                "classification_code": "classification code",
                "scheme": "scheme",
                "scheme_uri": "scheme uri",
                "keyword_uri": "keywords",
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_editor_keywords_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["name"] == "editor keywords"
    assert editor_response_data[0]["classification_code"] == "classification code"
    assert editor_response_data[0]["scheme"] == "scheme"
    assert editor_response_data[0]["scheme_uri"] == "scheme uri"
    assert editor_response_data[0]["keyword_uri"] == "keywords"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/metadata/keywords",
        json=[
            {
                "name": "editor keywords",
                "classification_code": "classification code",
                "scheme": "scheme",
                "scheme_uri": "scheme uri",
                "keyword_uri": "keywords",
            }
        ],
    )

    assert viewer_response.status_code == 403


def test_get_keywords_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/keywords' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the keywords metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/keywords")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/keywords")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/keywords")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/keywords")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["name"] == "keywords"
    assert response_data[0]["classification_code"] == "classification code"
    assert response_data[0]["scheme"] == "scheme"
    assert response_data[0]["scheme_uri"] == "scheme uri"
    assert response_data[0]["keyword_uri"] == "keywords"

    assert admin_response_data[0]["name"] == "keywords"
    assert admin_response_data[0]["classification_code"] == "classification code"
    assert admin_response_data[0]["scheme"] == "scheme"
    assert admin_response_data[0]["scheme_uri"] == "scheme uri"
    assert admin_response_data[0]["keyword_uri"] == "keywords"

    assert editor_response_data[0]["name"] == "keywords"
    assert editor_response_data[0]["classification_code"] == "classification code"
    assert editor_response_data[0]["scheme"] == "scheme"
    assert editor_response_data[0]["scheme_uri"] == "scheme uri"
    assert editor_response_data[0]["keyword_uri"] == "keywords"

    assert viewer_response_data[0]["name"] == "keywords"
    assert viewer_response_data[0]["classification_code"] == "classification code"
    assert viewer_response_data[0]["scheme"] == "scheme"
    assert viewer_response_data[0]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[0]["keyword_uri"] == "keywords"

    assert response_data[1]["name"] == "admin keywords"
    assert response_data[1]["classification_code"] == "classification code"
    assert response_data[1]["scheme"] == "scheme"
    assert response_data[1]["scheme_uri"] == "scheme uri"
    assert response_data[1]["keyword_uri"] == "keywords"

    assert admin_response_data[1]["name"] == "admin keywords"
    assert admin_response_data[1]["classification_code"] == "classification code"
    assert admin_response_data[1]["scheme"] == "scheme"
    assert admin_response_data[1]["scheme_uri"] == "scheme uri"
    assert admin_response_data[1]["keyword_uri"] == "keywords"

    assert editor_response_data[1]["name"] == "admin keywords"
    assert editor_response_data[1]["classification_code"] == "classification code"
    assert editor_response_data[1]["scheme"] == "scheme"
    assert editor_response_data[1]["scheme_uri"] == "scheme uri"
    assert editor_response_data[1]["keyword_uri"] == "keywords"

    assert viewer_response_data[1]["name"] == "admin keywords"
    assert viewer_response_data[1]["classification_code"] == "classification code"
    assert viewer_response_data[1]["scheme"] == "scheme"
    assert viewer_response_data[1]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[1]["keyword_uri"] == "keywords"

    assert response_data[2]["name"] == "editor keywords"
    assert response_data[2]["classification_code"] == "classification code"
    assert response_data[2]["scheme"] == "scheme"
    assert response_data[2]["scheme_uri"] == "scheme uri"
    assert response_data[2]["keyword_uri"] == "keywords"

    assert admin_response_data[2]["name"] == "editor keywords"
    assert admin_response_data[2]["classification_code"] == "classification code"
    assert admin_response_data[2]["scheme"] == "scheme"
    assert admin_response_data[2]["scheme_uri"] == "scheme uri"
    assert admin_response_data[2]["keyword_uri"] == "keywords"

    assert editor_response_data[2]["name"] == "editor keywords"
    assert editor_response_data[2]["classification_code"] == "classification code"
    assert editor_response_data[2]["scheme"] == "scheme"
    assert editor_response_data[2]["scheme_uri"] == "scheme uri"
    assert editor_response_data[2]["keyword_uri"] == "keywords"

    assert viewer_response_data[2]["name"] == "editor keywords"
    assert viewer_response_data[2]["classification_code"] == "classification code"
    assert viewer_response_data[2]["scheme"] == "scheme"
    assert viewer_response_data[2]["scheme_uri"] == "scheme uri"
    assert viewer_response_data[2]["keyword_uri"] == "keywords"


def test_delete_keywords_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/keywords' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the identification metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    keywords_id = pytest.global_keywords_id
    admin_keywords_id = pytest.global_admin_keywords_id_admin
    editor_keywords_id = pytest.global_editor_keywords_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/metadata/keywords/{keywords_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/keywords/{keywords_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/keywords/{admin_keywords_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/keywords/{editor_keywords_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DESCRIPTION METADATA ------------------- #
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

    assert viewer_response.status_code == 403


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

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["brief_summary"] == "editor-brief_summary"
    assert response_data["detailed_description"] == "editor-detailed_description"

    assert admin_response_data["brief_summary"] == "editor-brief_summary"
    assert admin_response_data["detailed_description"] == "editor-detailed_description"

    assert editor_response_data["brief_summary"] == "editor-brief_summary"
    assert editor_response_data["detailed_description"] == "editor-detailed_description"

    assert viewer_response_data["brief_summary"] == "editor-brief_summary"
    assert viewer_response_data["detailed_description"] == "editor-detailed_description"


# ------------------- DESIGN METADATA ------------------- #
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
            "is_patient_registry": "yes",
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
    assert response_data["is_patient_registry"] == "yes"

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
            "is_patient_registry": "yes",
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
    assert admin_response_data["design_who_masked_list"] == [
        "Participant",
        "Care Provider",
    ]
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
    assert admin_response_data["is_patient_registry"] == "yes"

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
            "is_patient_registry": "yes",
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
    assert editor_response_data["design_who_masked_list"] == [
        "Participant",
        "Care Provider",
    ]
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
    assert editor_response_data["is_patient_registry"] == "yes"

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
            "is_patient_registry": "yes",
        },
    )

    assert viewer_response.status_code == 403


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

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["design_allocation"] == "editor-dfasdfasd"
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
    assert response_data["is_patient_registry"] == "yes"

    assert admin_response_data["design_allocation"] == "editor-dfasdfasd"
    assert admin_response_data["study_type"] == "Interventional"
    assert admin_response_data["design_intervention_model"] == "Treatment"
    assert admin_response_data["design_intervention_model_description"] == "dfadf"
    assert admin_response_data["design_primary_purpose"] == "Parallel Assignment"
    assert admin_response_data["design_masking"] == "Double"
    assert admin_response_data["design_masking_description"] == "tewsfdasf"
    assert admin_response_data["design_who_masked_list"] == [
        "Participant",
        "Care Provider",
    ]
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
    assert admin_response_data["is_patient_registry"] == "yes"

    assert editor_response_data["design_allocation"] == "editor-dfasdfasd"
    assert editor_response_data["study_type"] == "Interventional"
    assert editor_response_data["design_intervention_model"] == "Treatment"
    assert editor_response_data["design_intervention_model_description"] == "dfadf"
    assert editor_response_data["design_primary_purpose"] == "Parallel Assignment"
    assert editor_response_data["design_masking"] == "Double"
    assert editor_response_data["design_masking_description"] == "tewsfdasf"
    assert editor_response_data["design_who_masked_list"] == [
        "Participant",
        "Care Provider",
    ]
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
    assert editor_response_data["is_patient_registry"] == "yes"

    assert viewer_response_data["design_allocation"] == "editor-dfasdfasd"
    assert viewer_response_data["study_type"] == "Interventional"
    assert viewer_response_data["design_intervention_model"] == "Treatment"
    assert viewer_response_data["design_intervention_model_description"] == "dfadf"
    assert viewer_response_data["design_primary_purpose"] == "Parallel Assignment"
    assert viewer_response_data["design_masking"] == "Double"
    assert viewer_response_data["design_masking_description"] == "tewsfdasf"
    assert viewer_response_data["design_who_masked_list"] == [
        "Participant",
        "Care Provider",
    ]
    assert viewer_response_data["phase_list"] == ["N/A"]
    assert viewer_response_data["enrollment_count"] == 3
    assert viewer_response_data["enrollment_type"] == "Actual"
    assert viewer_response_data["number_arms"] == 2
    assert viewer_response_data["design_observational_model_list"] == [
        "Cohort",
        "Case-Control",
    ]
    assert viewer_response_data["design_time_perspective_list"] == ["Other"]
    assert viewer_response_data["bio_spec_retention"] == "None Retained"
    assert viewer_response_data["bio_spec_description"] == "dfasdf"
    assert viewer_response_data["target_duration"] == "rewrwe"
    assert viewer_response_data["is_patient_registry"] == "yes"


# ------------------- ELIGIBILITY METADATA ------------------- #
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
            "sex": "All",
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

    assert response_data["sex"] == "All"
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
            "sex": "All",
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
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["sex"] == "All"
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
            "sex": "All",
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
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["sex"] == "All"
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
            "sex": "All",
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
        },
    )

    assert viewer_response.status_code == 403


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
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["sex"] == "All"
    assert response_data["gender_based"] == "Yes"
    assert response_data["gender_description"] == "editor-none"
    assert response_data["minimum_age_value"] == 18
    assert response_data["maximum_age_value"] == 61
    assert response_data["minimum_age_unit"] == "1"
    assert response_data["maximum_age_unit"] == "2"
    assert response_data["healthy_volunteers"] == "Yes"
    assert response_data["inclusion_criteria"] == ["tests"]
    assert response_data["exclusion_criteria"] == ["Probability Sample"]
    assert response_data["study_population"] == "study_population"
    assert response_data["sampling_method"] == "Probability Sample"

    assert admin_response_data["sex"] == "All"
    assert admin_response_data["gender_based"] == "Yes"
    assert admin_response_data["gender_description"] == "editor-none"
    assert admin_response_data["minimum_age_value"] == 18
    assert admin_response_data["maximum_age_value"] == 61
    assert admin_response_data["minimum_age_unit"] == "1"
    assert admin_response_data["maximum_age_unit"] == "2"
    assert admin_response_data["healthy_volunteers"] == "Yes"
    assert admin_response_data["inclusion_criteria"] == ["tests"]
    assert admin_response_data["exclusion_criteria"] == ["Probability Sample"]
    assert admin_response_data["study_population"] == "study_population"
    assert admin_response_data["sampling_method"] == "Probability Sample"

    assert editor_response_data["sex"] == "All"
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

    assert viewer_response_data["sex"] == "All"
    assert viewer_response_data["gender_based"] == "Yes"
    assert viewer_response_data["gender_description"] == "editor-none"
    assert viewer_response_data["minimum_age_value"] == 18
    assert viewer_response_data["maximum_age_value"] == 61
    assert viewer_response_data["minimum_age_unit"] == "1"
    assert viewer_response_data["maximum_age_unit"] == "2"
    assert viewer_response_data["healthy_volunteers"] == "Yes"
    assert viewer_response_data["inclusion_criteria"] == ["tests"]
    assert viewer_response_data["exclusion_criteria"] == ["Probability Sample"]
    assert viewer_response_data["study_population"] == "study_population"
    assert viewer_response_data["sampling_method"] == "Probability Sample"


# ------------------- IDENTIFICATION METADATA ------------------- #
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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_identification_id_admin = admin_response_data["secondary"][1]["id"]

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

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_identification_id_editor = editor_response_data["secondary"][2]["id"]

    assert editor_response_data["primary"]["identifier"] == "editor-first"
    assert editor_response_data["primary"]["identifier_type"] == "test"
    assert editor_response_data["primary"]["identifier_domain"] == "domain"
    assert editor_response_data["primary"]["identifier_link"] == "link"
    assert editor_response_data["secondary"][2]["identifier"] == "test"
    assert editor_response_data["secondary"][2]["identifier_type"] == "test"
    assert editor_response_data["secondary"][2]["identifier_domain"] == "dodfasdfmain"
    assert editor_response_data["secondary"][2]["identifier_link"] == "link"

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

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["primary"]["identifier"] == "editor-first"
    assert response_data["primary"]["identifier_type"] == "test"
    assert response_data["primary"]["identifier_domain"] == "domain"
    assert response_data["primary"]["identifier_link"] == "link"
    assert response_data["secondary"][0]["identifier"] == "test"
    assert response_data["secondary"][0]["identifier_type"] == "test"
    assert response_data["secondary"][0]["identifier_domain"] == "dodfasdfmain"
    assert response_data["secondary"][0]["identifier_link"] == "link"
    assert response_data["secondary"][1]["identifier"] == "test"
    assert response_data["secondary"][1]["identifier_type"] == "test"
    assert response_data["secondary"][1]["identifier_domain"] == "dodfasdfmain"
    assert response_data["secondary"][1]["identifier_link"] == "link"
    assert response_data["secondary"][2]["identifier"] == "test"
    assert response_data["secondary"][2]["identifier_type"] == "test"
    assert response_data["secondary"][2]["identifier_domain"] == "dodfasdfmain"
    assert response_data["secondary"][2]["identifier_link"] == "link"

    assert admin_response_data["primary"]["identifier"] == "editor-first"
    assert admin_response_data["primary"]["identifier_type"] == "test"
    assert admin_response_data["primary"]["identifier_domain"] == "domain"
    assert admin_response_data["primary"]["identifier_link"] == "link"
    assert admin_response_data["secondary"][0]["identifier"] == "test"
    assert admin_response_data["secondary"][0]["identifier_type"] == "test"
    assert admin_response_data["secondary"][0]["identifier_domain"] == "dodfasdfmain"
    assert admin_response_data["secondary"][0]["identifier_link"] == "link"
    assert admin_response_data["secondary"][1]["identifier"] == "test"
    assert admin_response_data["secondary"][1]["identifier_type"] == "test"
    assert admin_response_data["secondary"][1]["identifier_domain"] == "dodfasdfmain"
    assert admin_response_data["secondary"][1]["identifier_link"] == "link"
    assert admin_response_data["secondary"][2]["identifier"] == "test"
    assert admin_response_data["secondary"][2]["identifier_type"] == "test"
    assert admin_response_data["secondary"][2]["identifier_domain"] == "dodfasdfmain"
    assert admin_response_data["secondary"][2]["identifier_link"] == "link"

    assert editor_response_data["primary"]["identifier"] == "editor-first"
    assert editor_response_data["primary"]["identifier_type"] == "test"
    assert editor_response_data["primary"]["identifier_domain"] == "domain"
    assert editor_response_data["primary"]["identifier_link"] == "link"
    assert editor_response_data["secondary"][0]["identifier"] == "test"
    assert editor_response_data["secondary"][0]["identifier_type"] == "test"
    assert editor_response_data["secondary"][0]["identifier_domain"] == "dodfasdfmain"
    assert editor_response_data["secondary"][0]["identifier_link"] == "link"
    assert editor_response_data["secondary"][1]["identifier"] == "test"
    assert editor_response_data["secondary"][1]["identifier_type"] == "test"
    assert editor_response_data["secondary"][1]["identifier_domain"] == "dodfasdfmain"
    assert editor_response_data["secondary"][1]["identifier_link"] == "link"
    assert editor_response_data["secondary"][2]["identifier"] == "test"
    assert editor_response_data["secondary"][2]["identifier_type"] == "test"
    assert editor_response_data["secondary"][2]["identifier_domain"] == "dodfasdfmain"
    assert editor_response_data["secondary"][2]["identifier_link"] == "link"

    assert viewer_response_data["primary"]["identifier"] == "editor-first"
    assert viewer_response_data["primary"]["identifier_type"] == "test"
    assert viewer_response_data["primary"]["identifier_domain"] == "domain"
    assert viewer_response_data["primary"]["identifier_link"] == "link"
    assert viewer_response_data["secondary"][0]["identifier"] == "test"
    assert viewer_response_data["secondary"][0]["identifier_type"] == "test"
    assert viewer_response_data["secondary"][0]["identifier_domain"] == "dodfasdfmain"
    assert viewer_response_data["secondary"][0]["identifier_link"] == "link"
    assert viewer_response_data["secondary"][1]["identifier"] == "test"
    assert viewer_response_data["secondary"][1]["identifier_type"] == "test"
    assert viewer_response_data["secondary"][1]["identifier_domain"] == "dodfasdfmain"
    assert viewer_response_data["secondary"][1]["identifier_link"] == "link"
    assert viewer_response_data["secondary"][2]["identifier"] == "test"
    assert viewer_response_data["secondary"][2]["identifier_type"] == "test"
    assert viewer_response_data["secondary"][2]["identifier_domain"] == "dodfasdfmain"
    assert viewer_response_data["secondary"][2]["identifier_link"] == "link"


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
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- INTERVENTION METADATA ------------------- #
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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_intervention_id_admin = admin_response_data[0]["id"]

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

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_intervention_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["type"] == "Device"
    assert editor_response_data[0]["name"] == "editor-name test"
    assert editor_response_data[0]["description"] == "desc"
    assert editor_response_data[0]["arm_group_label_list"] == ["test", "one"]
    assert editor_response_data[0]["other_name_list"] == ["uhh", "yes"]

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

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["type"] == "Device"
    assert response_data[0]["name"] == "name test"
    assert response_data[0]["description"] == "desc"
    assert response_data[0]["arm_group_label_list"] == ["test", "one"]
    assert response_data[0]["other_name_list"] == ["uhh", "yes"]
    assert response_data[1]["type"] == "Device"
    assert response_data[1]["name"] == "admin-name test"
    assert response_data[1]["description"] == "desc"
    assert response_data[1]["arm_group_label_list"] == ["test", "one"]
    assert response_data[1]["other_name_list"] == ["uhh", "yes"]
    assert response_data[2]["type"] == "Device"
    assert response_data[2]["name"] == "editor-name test"
    assert response_data[2]["description"] == "desc"
    assert response_data[2]["arm_group_label_list"] == ["test", "one"]
    assert response_data[2]["other_name_list"] == ["uhh", "yes"]

    assert admin_response_data[0]["type"] == "Device"
    assert admin_response_data[0]["name"] == "name test"
    assert admin_response_data[0]["description"] == "desc"
    assert admin_response_data[0]["arm_group_label_list"] == ["test", "one"]
    assert admin_response_data[0]["other_name_list"] == ["uhh", "yes"]
    assert admin_response_data[1]["type"] == "Device"
    assert admin_response_data[1]["name"] == "admin-name test"
    assert admin_response_data[1]["description"] == "desc"
    assert admin_response_data[1]["arm_group_label_list"] == ["test", "one"]
    assert admin_response_data[1]["other_name_list"] == ["uhh", "yes"]
    assert admin_response_data[2]["type"] == "Device"
    assert admin_response_data[2]["name"] == "editor-name test"
    assert admin_response_data[2]["description"] == "desc"
    assert admin_response_data[2]["arm_group_label_list"] == ["test", "one"]
    assert admin_response_data[2]["other_name_list"] == ["uhh", "yes"]

    assert editor_response_data[0]["type"] == "Device"
    assert editor_response_data[0]["name"] == "name test"
    assert editor_response_data[0]["description"] == "desc"
    assert editor_response_data[0]["arm_group_label_list"] == ["test", "one"]
    assert editor_response_data[0]["other_name_list"] == ["uhh", "yes"]
    assert editor_response_data[1]["type"] == "Device"
    assert editor_response_data[1]["name"] == "admin-name test"
    assert editor_response_data[1]["description"] == "desc"
    assert editor_response_data[1]["arm_group_label_list"] == ["test", "one"]
    assert editor_response_data[1]["other_name_list"] == ["uhh", "yes"]
    assert editor_response_data[2]["type"] == "Device"
    assert editor_response_data[2]["name"] == "editor-name test"
    assert editor_response_data[2]["description"] == "desc"
    assert editor_response_data[2]["arm_group_label_list"] == ["test", "one"]
    assert editor_response_data[2]["other_name_list"] == ["uhh", "yes"]

    assert viewer_response_data[0]["type"] == "Device"
    assert viewer_response_data[0]["name"] == "name test"
    assert viewer_response_data[0]["description"] == "desc"
    assert viewer_response_data[0]["arm_group_label_list"] == ["test", "one"]
    assert viewer_response_data[0]["other_name_list"] == ["uhh", "yes"]
    assert viewer_response_data[1]["type"] == "Device"
    assert viewer_response_data[1]["name"] == "admin-name test"
    assert viewer_response_data[1]["description"] == "desc"
    assert viewer_response_data[1]["arm_group_label_list"] == ["test", "one"]
    assert viewer_response_data[1]["other_name_list"] == ["uhh", "yes"]
    assert viewer_response_data[2]["type"] == "Device"
    assert viewer_response_data[2]["name"] == "editor-name test"
    assert viewer_response_data[2]["description"] == "desc"
    assert viewer_response_data[2]["arm_group_label_list"] == ["test", "one"]
    assert viewer_response_data[2]["other_name_list"] == ["uhh", "yes"]


def test_delete_intervention_metadata(clients):
    """
    Given a Flask application configured for testing, study ID, dataset ID and intervention ID
    WHEN the '/study/{study_id}/metadata/intervention' endpoint is requested (DELETE)
    THEN check that the response is valid and deletes the intervention metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    intervention_id = pytest.global_intervention_id
    a_intervention_id = pytest.global_intervention_id_admin
    e_intervention_id = pytest.global_intervention_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/metadata/intervention/{intervention_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/intervention/{intervention_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/intervention/{a_intervention_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/intervention/{e_intervention_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- LOCATION METADATA ------------------- #
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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_location_id = response_data[0]["id"]

    assert response_data[0]["facility"] == "test"
    assert response_data[0]["status"] == "Withdrawn"
    assert response_data[0]["city"] == "city"
    assert response_data[0]["state"] == "ca"
    assert response_data[0]["zip"] == "test"
    assert response_data[0]["country"] == "yes"

    admin_response = _admin_client.post(
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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_location_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["facility"] == "test"
    assert admin_response_data[0]["status"] == "Withdrawn"
    assert admin_response_data[0]["city"] == "city"
    assert admin_response_data[0]["state"] == "ca"
    assert admin_response_data[0]["zip"] == "test"
    assert admin_response_data[0]["country"] == "yes"

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/location",
        json=[
            {
                "facility": "editor test",
                "status": "Withdrawn",
                "city": "city",
                "state": "ca",
                "zip": "test",
                "country": "yes",
            }
        ],
    )

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_location_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["facility"] == "editor test"
    assert editor_response_data[0]["status"] == "Withdrawn"
    assert editor_response_data[0]["city"] == "city"
    assert editor_response_data[0]["state"] == "ca"
    assert editor_response_data[0]["zip"] == "test"
    assert editor_response_data[0]["country"] == "yes"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/metadata/location",
        json=[
            {
                "facility": "viewer test",
                "status": "Withdrawn",
                "city": "city",
                "state": "ca",
                "zip": "test",
                "country": "yes",
            }
        ],
    )

    assert viewer_response.status_code == 403


def test_get_location_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/location' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the location metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/location")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/location")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/location")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/location")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["facility"] == "test"
    assert response_data[0]["status"] == "Withdrawn"
    assert response_data[0]["city"] == "city"
    assert response_data[0]["state"] == "ca"
    assert response_data[0]["zip"] == "test"
    assert response_data[0]["country"] == "yes"
    assert response_data[1]["facility"] == "test"
    assert response_data[1]["status"] == "Withdrawn"
    assert response_data[1]["city"] == "city"
    assert response_data[1]["state"] == "ca"
    assert response_data[1]["zip"] == "test"
    assert response_data[1]["country"] == "yes"
    assert response_data[2]["facility"] == "editor test"
    assert response_data[2]["status"] == "Withdrawn"
    assert response_data[2]["city"] == "city"
    assert response_data[2]["state"] == "ca"
    assert response_data[2]["zip"] == "test"
    assert response_data[2]["country"] == "yes"

    assert admin_response_data[0]["facility"] == "test"
    assert admin_response_data[0]["status"] == "Withdrawn"
    assert admin_response_data[0]["city"] == "city"
    assert admin_response_data[0]["state"] == "ca"
    assert admin_response_data[0]["zip"] == "test"
    assert admin_response_data[0]["country"] == "yes"
    assert admin_response_data[1]["facility"] == "test"
    assert admin_response_data[1]["status"] == "Withdrawn"
    assert admin_response_data[1]["city"] == "city"
    assert admin_response_data[1]["state"] == "ca"
    assert admin_response_data[1]["zip"] == "test"
    assert admin_response_data[1]["country"] == "yes"
    assert admin_response_data[2]["facility"] == "editor test"
    assert admin_response_data[2]["status"] == "Withdrawn"
    assert admin_response_data[2]["city"] == "city"
    assert admin_response_data[2]["state"] == "ca"
    assert admin_response_data[2]["zip"] == "test"
    assert admin_response_data[2]["country"] == "yes"

    assert editor_response_data[0]["facility"] == "test"
    assert editor_response_data[0]["status"] == "Withdrawn"
    assert editor_response_data[0]["city"] == "city"
    assert editor_response_data[0]["state"] == "ca"
    assert editor_response_data[0]["zip"] == "test"
    assert editor_response_data[0]["country"] == "yes"
    assert editor_response_data[1]["facility"] == "test"
    assert editor_response_data[1]["status"] == "Withdrawn"
    assert editor_response_data[1]["city"] == "city"
    assert editor_response_data[1]["state"] == "ca"
    assert editor_response_data[1]["zip"] == "test"
    assert editor_response_data[1]["country"] == "yes"
    assert editor_response_data[2]["facility"] == "editor test"
    assert editor_response_data[2]["status"] == "Withdrawn"
    assert editor_response_data[2]["city"] == "city"
    assert editor_response_data[2]["state"] == "ca"
    assert editor_response_data[2]["zip"] == "test"
    assert editor_response_data[2]["country"] == "yes"

    assert viewer_response_data[0]["facility"] == "test"
    assert viewer_response_data[0]["status"] == "Withdrawn"
    assert viewer_response_data[0]["city"] == "city"
    assert viewer_response_data[0]["state"] == "ca"
    assert viewer_response_data[0]["zip"] == "test"
    assert viewer_response_data[0]["country"] == "yes"
    assert viewer_response_data[1]["facility"] == "test"
    assert viewer_response_data[1]["status"] == "Withdrawn"
    assert viewer_response_data[1]["city"] == "city"
    assert viewer_response_data[1]["state"] == "ca"
    assert viewer_response_data[1]["zip"] == "test"
    assert viewer_response_data[1]["country"] == "yes"
    assert viewer_response_data[2]["facility"] == "editor test"
    assert viewer_response_data[2]["status"] == "Withdrawn"
    assert viewer_response_data[2]["city"] == "city"
    assert viewer_response_data[2]["state"] == "ca"
    assert viewer_response_data[2]["zip"] == "test"
    assert viewer_response_data[2]["country"] == "yes"


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
    admin_location_id = pytest.global_location_id_admin
    editor_location_id = pytest.global_location_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/metadata/location/{location_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/location/{location_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/location/{admin_location_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/location/{editor_location_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- OVERALL-OFFICIAL METADATA ------------------- #
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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_overall_official_id = response_data[0]["id"]

    assert response_data[0]["first_name"] == "test"
    assert response_data[0]["last_name"] == "test"
    assert response_data[0]["affiliation"] == "aff"
    assert response_data[0]["degree"] == "aff"
    assert response_data[0]["identifier"] == "identifier"
    assert response_data[0]["identifier_scheme"] == "scheme"
    assert response_data[0]["identifier_scheme_uri"] == "uri"
    assert response_data[0]["affiliation_identifier"] == "identifier"
    assert response_data[0]["affiliation_identifier_scheme"] == "scheme"
    assert response_data[0]["affiliation_identifier_scheme_uri"] == "uri"
    assert response_data[0]["role"] == "chair"

    admin_response = _admin_client.post(
        f"/study/{study_id}/metadata/overall-official",
        json=[
            {
                "first_name": "admin test",
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
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_overall_official_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["first_name"] == "admin test"
    assert admin_response_data[0]["last_name"] == "test"
    assert admin_response_data[0]["affiliation"] == "aff"
    assert admin_response_data[0]["degree"] == "aff"
    assert admin_response_data[0]["identifier"] == "identifier"
    assert admin_response_data[0]["identifier_scheme"] == "scheme"
    assert admin_response_data[0]["identifier_scheme_uri"] == "uri"
    assert admin_response_data[0]["affiliation"] == "aff"
    assert admin_response_data[0]["affiliation_identifier"] == "identifier"
    assert admin_response_data[0]["affiliation_identifier_scheme"] == "scheme"
    assert admin_response_data[0]["affiliation_identifier_scheme_uri"] == "uri"
    assert admin_response_data[0]["role"] == "chair"

    editor_response = _editor_client.post(
        f"/study/{study_id}/metadata/overall-official",
        json=[
            {
                "first_name": "editor test",
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

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_overall_official_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["first_name"] == "editor test"
    assert editor_response_data[0]["last_name"] == "test"
    assert editor_response_data[0]["affiliation"] == "aff"
    assert editor_response_data[0]["degree"] == "aff"
    assert editor_response_data[0]["identifier"] == "identifier"
    assert editor_response_data[0]["identifier_scheme"] == "scheme"
    assert editor_response_data[0]["identifier_scheme_uri"] == "uri"
    assert editor_response_data[0]["affiliation"] == "aff"
    assert editor_response_data[0]["affiliation_identifier"] == "identifier"
    assert editor_response_data[0]["affiliation_identifier_scheme"] == "scheme"
    assert editor_response_data[0]["affiliation_identifier_scheme_uri"] == "uri"
    assert editor_response_data[0]["role"] == "chair"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/metadata/overall-official",
        json=[
            {
                "first_name": "editor test",
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

    assert viewer_response.status_code == 403


def test_get_overall_official_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/overall-official' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the overall-official metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/overall-official")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/overall-official")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/overall-official")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/overall-official")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["first_name"] == "test"
    assert response_data[0]["last_name"] == "test"
    assert response_data[0]["affiliation"] == "aff"
    assert response_data[0]["degree"] == "aff"
    assert response_data[0]["identifier"] == "identifier"
    assert response_data[0]["identifier_scheme"] == "scheme"
    assert response_data[0]["identifier_scheme_uri"] == "uri"
    assert response_data[0]["affiliation"] == "aff"
    assert response_data[0]["affiliation_identifier"] == "identifier"
    assert response_data[0]["affiliation_identifier_scheme"] == "scheme"
    assert response_data[0]["affiliation_identifier_scheme_uri"] == "uri"
    assert response_data[0]["role"] == "chair"

    assert admin_response_data[0]["first_name"] == "test"
    assert admin_response_data[0]["last_name"] == "test"
    assert admin_response_data[0]["affiliation"] == "aff"
    assert admin_response_data[0]["degree"] == "aff"
    assert admin_response_data[0]["identifier"] == "identifier"
    assert admin_response_data[0]["identifier_scheme"] == "scheme"
    assert admin_response_data[0]["identifier_scheme_uri"] == "uri"
    assert admin_response_data[0]["affiliation"] == "aff"
    assert admin_response_data[0]["affiliation_identifier"] == "identifier"
    assert admin_response_data[0]["affiliation_identifier_scheme"] == "scheme"
    assert admin_response_data[0]["affiliation_identifier_scheme_uri"] == "uri"
    assert admin_response_data[0]["role"] == "chair"

    assert editor_response_data[0]["first_name"] == "test"
    assert editor_response_data[0]["last_name"] == "test"
    assert editor_response_data[0]["affiliation"] == "aff"
    assert editor_response_data[0]["degree"] == "aff"
    assert editor_response_data[0]["identifier"] == "identifier"
    assert editor_response_data[0]["identifier_scheme"] == "scheme"
    assert editor_response_data[0]["identifier_scheme_uri"] == "uri"
    assert editor_response_data[0]["affiliation"] == "aff"
    assert editor_response_data[0]["affiliation_identifier"] == "identifier"
    assert editor_response_data[0]["affiliation_identifier_scheme"] == "scheme"
    assert editor_response_data[0]["affiliation_identifier_scheme_uri"] == "uri"
    assert editor_response_data[0]["role"] == "chair"

    assert viewer_response_data[0]["first_name"] == "test"
    assert viewer_response_data[0]["last_name"] == "test"
    assert viewer_response_data[0]["affiliation"] == "aff"
    assert viewer_response_data[0]["degree"] == "aff"
    assert viewer_response_data[0]["identifier"] == "identifier"
    assert viewer_response_data[0]["identifier_scheme"] == "scheme"
    assert viewer_response_data[0]["identifier_scheme_uri"] == "uri"
    assert viewer_response_data[0]["affiliation"] == "aff"
    assert viewer_response_data[0]["affiliation_identifier"] == "identifier"
    assert viewer_response_data[0]["affiliation_identifier_scheme"] == "scheme"
    assert viewer_response_data[0]["affiliation_identifier_scheme_uri"] == "uri"
    assert viewer_response_data[0]["role"] == "chair"

    assert response_data[1]["first_name"] == "admin test"
    assert response_data[1]["last_name"] == "test"
    assert response_data[1]["affiliation"] == "aff"
    assert response_data[1]["degree"] == "aff"
    assert response_data[1]["identifier"] == "identifier"
    assert response_data[1]["identifier_scheme"] == "scheme"
    assert response_data[1]["identifier_scheme_uri"] == "uri"
    assert response_data[1]["affiliation"] == "aff"
    assert response_data[1]["affiliation_identifier"] == "identifier"
    assert response_data[1]["affiliation_identifier_scheme"] == "scheme"
    assert response_data[1]["affiliation_identifier_scheme_uri"] == "uri"
    assert response_data[1]["role"] == "chair"

    assert admin_response_data[1]["first_name"] == "admin test"
    assert admin_response_data[1]["last_name"] == "test"
    assert admin_response_data[1]["affiliation"] == "aff"
    assert admin_response_data[1]["degree"] == "aff"
    assert admin_response_data[1]["identifier"] == "identifier"
    assert admin_response_data[1]["identifier_scheme"] == "scheme"
    assert admin_response_data[1]["identifier_scheme_uri"] == "uri"
    assert admin_response_data[1]["affiliation"] == "aff"
    assert admin_response_data[1]["affiliation_identifier"] == "identifier"
    assert admin_response_data[1]["affiliation_identifier_scheme"] == "scheme"
    assert admin_response_data[1]["affiliation_identifier_scheme_uri"] == "uri"
    assert admin_response_data[1]["role"] == "chair"

    assert editor_response_data[1]["first_name"] == "admin test"
    assert editor_response_data[1]["last_name"] == "test"
    assert editor_response_data[1]["affiliation"] == "aff"
    assert editor_response_data[1]["degree"] == "aff"
    assert editor_response_data[1]["identifier"] == "identifier"
    assert editor_response_data[1]["identifier_scheme"] == "scheme"
    assert editor_response_data[1]["identifier_scheme_uri"] == "uri"
    assert editor_response_data[1]["affiliation"] == "aff"
    assert editor_response_data[1]["affiliation_identifier"] == "identifier"
    assert editor_response_data[1]["affiliation_identifier_scheme"] == "scheme"
    assert editor_response_data[1]["affiliation_identifier_scheme_uri"] == "uri"
    assert editor_response_data[1]["role"] == "chair"

    assert viewer_response_data[1]["first_name"] == "test"
    assert viewer_response_data[1]["last_name"] == "test"
    assert viewer_response_data[1]["affiliation"] == "aff"
    assert viewer_response_data[1]["degree"] == "aff"
    assert viewer_response_data[1]["identifier"] == "identifier"
    assert viewer_response_data[1]["identifier_scheme"] == "scheme"
    assert viewer_response_data[1]["identifier_scheme_uri"] == "uri"
    assert viewer_response_data[1]["affiliation"] == "aff"
    assert viewer_response_data[1]["affiliation_identifier"] == "identifier"
    assert viewer_response_data[1]["affiliation_identifier_scheme"] == "scheme"
    assert viewer_response_data[1]["affiliation_identifier_scheme_uri"] == "uri"
    assert viewer_response_data[1]["role"] == "chair"

    assert response_data[2]["first_name"] == "editor test"
    assert response_data[2]["last_name"] == "test"
    assert response_data[2]["affiliation"] == "aff"
    assert response_data[2]["degree"] == "aff"
    assert response_data[2]["identifier"] == "identifier"
    assert response_data[2]["identifier_scheme"] == "scheme"
    assert response_data[2]["identifier_scheme_uri"] == "uri"
    assert response_data[2]["affiliation"] == "aff"
    assert response_data[2]["affiliation_identifier"] == "identifier"
    assert response_data[2]["affiliation_identifier_scheme"] == "scheme"
    assert response_data[2]["affiliation_identifier_scheme_uri"] == "uri"
    assert response_data[2]["role"] == "chair"

    assert admin_response_data[2]["first_name"] == "editor test"
    assert admin_response_data[2]["last_name"] == "test"
    assert admin_response_data[2]["affiliation"] == "aff"
    assert admin_response_data[2]["degree"] == "aff"
    assert admin_response_data[2]["identifier"] == "identifier"
    assert admin_response_data[2]["identifier_scheme"] == "scheme"
    assert admin_response_data[2]["identifier_scheme_uri"] == "uri"
    assert admin_response_data[2]["affiliation"] == "aff"
    assert admin_response_data[2]["affiliation_identifier"] == "identifier"
    assert admin_response_data[2]["affiliation_identifier_scheme"] == "scheme"
    assert admin_response_data[2]["affiliation_identifier_scheme_uri"] == "uri"
    assert admin_response_data[2]["role"] == "chair"

    assert editor_response_data[2]["first_name"] == "editor test"
    assert editor_response_data[2]["last_name"] == "test"
    assert editor_response_data[2]["affiliation"] == "aff"
    assert editor_response_data[2]["degree"] == "aff"
    assert editor_response_data[2]["identifier"] == "identifier"
    assert editor_response_data[2]["identifier_scheme"] == "scheme"
    assert editor_response_data[2]["identifier_scheme_uri"] == "uri"
    assert editor_response_data[2]["affiliation"] == "aff"
    assert editor_response_data[2]["affiliation_identifier"] == "identifier"
    assert editor_response_data[2]["affiliation_identifier_scheme"] == "scheme"
    assert editor_response_data[2]["affiliation_identifier_scheme_uri"] == "uri"
    assert editor_response_data[2]["role"] == "chair"

    assert viewer_response_data[2]["first_name"] == "test"
    assert viewer_response_data[2]["last_name"] == "test"
    assert viewer_response_data[2]["affiliation"] == "aff"
    assert viewer_response_data[2]["degree"] == "aff"
    assert viewer_response_data[2]["identifier"] == "identifier"
    assert viewer_response_data[2]["identifier_scheme"] == "scheme"
    assert viewer_response_data[2]["identifier_scheme_uri"] == "uri"
    assert viewer_response_data[2]["affiliation"] == "aff"
    assert viewer_response_data[2]["affiliation_identifier"] == "identifier"
    assert viewer_response_data[2]["affiliation_identifier_scheme"] == "scheme"
    assert viewer_response_data[2]["affiliation_identifier_scheme_uri"] == "uri"
    assert viewer_response_data[2]["role"] == "chair"


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
    oo_admin_id = pytest.global_overall_official_id_admin
    oo_editor_id = pytest.global_overall_official_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/metadata/overall-official/{overall_official_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/metadata/overall-official/{overall_official_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/metadata/overall-official/{oo_admin_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/metadata/overall-official/{oo_editor_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- OVERSIGHT METADATA ------------------- #
def test_put_oversight_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/oversight' endpoint is requested (PUT)
    THEN check that the response is valid and updates the oversight metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/oversight",
        json={
            "fda_regulated_drug": "drug",
            "fda_regulated_device": "device",
            "has_dmc": "yes",
            "human_subject_review_status": "yes",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["fda_regulated_drug"] == "drug"
    assert response_data["fda_regulated_device"] == "device"
    assert response_data["has_dmc"] == "yes"
    assert response_data["human_subject_review_status"] == "yes"

    admin_response = _admin_client.put(
        f"/study/{study_id}/metadata/oversight",
        json={
            "fda_regulated_drug": "drug",
            "fda_regulated_device": "device",
            "has_dmc": "yes",
            "human_subject_review_status": "yes",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["fda_regulated_drug"] == "drug"
    assert admin_response_data["fda_regulated_device"] == "device"
    assert admin_response_data["has_dmc"] == "yes"
    assert admin_response_data["human_subject_review_status"] == "yes"

    editor_response = _editor_client.put(
        f"/study/{study_id}/metadata/oversight",
        json={
            "fda_regulated_drug": "drug",
            "fda_regulated_device": "device",
            "has_dmc": "yes",
            "human_subject_review_status": "yes",
        },
    )

    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["fda_regulated_drug"] == "drug"
    assert editor_response_data["fda_regulated_device"] == "device"
    assert editor_response_data["has_dmc"] == "yes"
    assert editor_response_data["human_subject_review_status"] == "yes"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/metadata/oversight",
        json={
            "fda_regulated_drug": "drug",
            "fda_regulated_device": "device",
            "has_dmc": "yes",
            "human_subject_review_status": "yes",
        },
    )

    assert viewer_response.status_code == 403


def test_get_oversight_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/oversight' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the oversight metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/oversight")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/oversight")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/oversight")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/oversight")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["fda_regulated_drug"] == "drug"
    assert response_data["fda_regulated_device"] == "device"
    assert response_data["has_dmc"] == "yes"
    assert response_data["human_subject_review_status"] == "yes"

    assert admin_response_data["fda_regulated_drug"] == "drug"
    assert admin_response_data["fda_regulated_device"] == "device"
    assert admin_response_data["has_dmc"] == "yes"
    assert admin_response_data["human_subject_review_status"] == "yes"

    assert editor_response_data["fda_regulated_drug"] == "drug"
    assert editor_response_data["fda_regulated_device"] == "device"
    assert editor_response_data["has_dmc"] == "yes"
    assert editor_response_data["human_subject_review_status"] == "yes"

    assert viewer_response_data["fda_regulated_drug"] == "drug"
    assert viewer_response_data["fda_regulated_device"] == "device"
    assert viewer_response_data["has_dmc"] == "yes"
    assert viewer_response_data["human_subject_review_status"] == "yes"


# ------------------- SPONSORS METADATA ------------------- #
def test_put_sponsors_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/sponsors' endpoint is requested (PUT)
    THEN check that the response is valid and updates the sponsors metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.put(
        f"/study/{study_id}/metadata/sponsor",
        json={
            "lead_sponsor_identifier_scheme": "scheme",
            "lead_sponsor_identifier_scheme_uri": "uri",
            "responsible_party_type": "Sponsor",
            "responsible_party_investigator_first_name": "name",
            "responsible_party_investigator_last_name": "surname",
            "responsible_party_investigator_title": "title",
            "responsible_party_investigator_identifier_value": "identifier",
            "responsible_party_investigator_identifier_scheme": "scheme",
            "responsible_party_investigator_identifier_scheme_uri": "uri",
            "responsible_party_investigator_affiliation_name": "affiliation",
            "responsible_party_investigator_affiliation_identifier_value": "identifier",
            "responsible_party_investigator_affiliation_identifier_scheme": "scheme",
            "responsible_party_investigator_affiliation_identifier_scheme_uri": "uri",
            "lead_sponsor_name": "name",
            "lead_sponsor_identifier": "identifier",
        },
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["responsible_party_type"] == "Sponsor"
    assert response_data["responsible_party_investigator_first_name"] == "name"
    assert response_data["responsible_party_investigator_last_name"] == "surname"
    assert (
        response_data["responsible_party_investigator_title"] == "title"
    )  # noqa: E501
    assert (
        response_data["responsible_party_investigator_identifier_value"] == "identifier"
    )
    assert response_data["responsible_party_investigator_identifier_scheme"] == "scheme"
    assert (
        response_data["responsible_party_investigator_identifier_scheme_uri"] == "uri"
    )
    assert (
        response_data["responsible_party_investigator_affiliation_name"]
        == "affiliation"
    )
    assert (
        response_data["responsible_party_investigator_affiliation_identifier_value"]
        == "identifier"
    )
    assert (
        response_data["responsible_party_investigator_affiliation_identifier_scheme"]
        == "scheme"
    )
    assert (
        response_data[
            "responsible_party_investigator_affiliation_identifier_scheme_uri"
        ]
        == "uri"
    )
    assert response_data["lead_sponsor_name"] == "name"
    assert response_data["lead_sponsor_identifier"] == "identifier"
    assert response_data["lead_sponsor_identifier_scheme"] == "scheme"
    assert response_data["lead_sponsor_identifier_scheme_uri"] == "uri"

    admin_response = _admin_client.put(
        f"/study/{study_id}/metadata/sponsor",
        json={
            "lead_sponsor_identifier_scheme": "scheme",
            "lead_sponsor_identifier_scheme_uri": "uri",
            "responsible_party_type": "Sponsor",
            "responsible_party_investigator_first_name": "name",
            "responsible_party_investigator_last_name": "surname",
            "responsible_party_investigator_title": "title",
            "responsible_party_investigator_identifier_value": "identifier",
            "responsible_party_investigator_identifier_scheme": "scheme",
            "responsible_party_investigator_identifier_scheme_uri": "uri",
            "responsible_party_investigator_affiliation_name": "affiliation",
            "responsible_party_investigator_affiliation_identifier_value": "identifier",
            "responsible_party_investigator_affiliation_identifier_scheme": "scheme",
            "responsible_party_investigator_affiliation_identifier_scheme_uri": "uri",
            "lead_sponsor_name": "name",
            "lead_sponsor_identifier": "identifier",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["responsible_party_type"] == "Sponsor"
    assert admin_response_data["responsible_party_investigator_first_name"] == "name"
    assert admin_response_data["responsible_party_investigator_last_name"] == "surname"
    assert (
        admin_response_data["responsible_party_investigator_title"] == "title"
    )  # noqa: E501
    assert (
        admin_response_data["responsible_party_investigator_identifier_value"]
        == "identifier"
    )
    assert (
        admin_response_data["responsible_party_investigator_identifier_scheme"]
        == "scheme"
    )
    assert (
        admin_response_data["responsible_party_investigator_identifier_scheme_uri"]
        == "uri"
    )
    assert (
        admin_response_data["responsible_party_investigator_affiliation_name"]
        == "affiliation"
    )
    assert (
        admin_response_data[
            "responsible_party_investigator_affiliation_identifier_value"
        ]
        == "identifier"
    )
    assert (
        admin_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme"
        ]
        == "scheme"
    )
    assert (
        admin_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme_uri"
        ]
        == "uri"
    )
    assert admin_response_data["lead_sponsor_name"] == "name"
    assert admin_response_data["lead_sponsor_identifier"] == "identifier"
    assert admin_response_data["lead_sponsor_identifier_scheme"] == "scheme"
    assert admin_response_data["lead_sponsor_identifier_scheme_uri"] == "uri"

    editor_response = _editor_client.put(
        f"/study/{study_id}/metadata/sponsor",
        json={
            "lead_sponsor_identifier_scheme": "scheme",
            "lead_sponsor_identifier_scheme_uri": "uri",
            "responsible_party_type": "Sponsor",
            "responsible_party_investigator_first_name": "name",
            "responsible_party_investigator_last_name": "surname",
            "responsible_party_investigator_title": "title",
            "responsible_party_investigator_identifier_value": "identifier",
            "responsible_party_investigator_identifier_scheme": "scheme",
            "responsible_party_investigator_identifier_scheme_uri": "uri",
            "responsible_party_investigator_affiliation_name": "affiliation",
            "responsible_party_investigator_affiliation_identifier_value": "identifier",
            "responsible_party_investigator_affiliation_identifier_scheme": "scheme",
            "responsible_party_investigator_affiliation_identifier_scheme_uri": "uri",
            "lead_sponsor_name": "name",
            "lead_sponsor_identifier": "identifier",
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["responsible_party_type"] == "Sponsor"
    assert editor_response_data["responsible_party_investigator_first_name"] == "name"
    assert editor_response_data["responsible_party_investigator_last_name"] == "surname"
    assert (
        editor_response_data["responsible_party_investigator_title"] == "title"
    )  # noqa: E501
    assert (
        editor_response_data["responsible_party_investigator_identifier_value"]
        == "identifier"
    )
    assert (
        editor_response_data["responsible_party_investigator_identifier_scheme"]
        == "scheme"
    )
    assert (
        editor_response_data["responsible_party_investigator_identifier_scheme_uri"]
        == "uri"
    )
    assert (
        editor_response_data["responsible_party_investigator_affiliation_name"]
        == "affiliation"
    )
    assert (
        editor_response_data[
            "responsible_party_investigator_affiliation_identifier_value"
        ]
        == "identifier"
    )
    assert (
        editor_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme"
        ]
        == "scheme"
    )
    assert (
        editor_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme_uri"
        ]
        == "uri"
    )
    assert editor_response_data["lead_sponsor_name"] == "name"
    assert editor_response_data["lead_sponsor_identifier"] == "identifier"
    assert editor_response_data["lead_sponsor_identifier_scheme"] == "scheme"
    assert editor_response_data["lead_sponsor_identifier_scheme_uri"] == "uri"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/metadata/sponsor",
        json={
            "responsible_party_type": "Sponsor",
            "responsible_party_investigator_first_name": "name",
            "responsible_party_investigator_last_name": "surname",
            "responsible_party_investigator_title": "title",
            "responsible_party_investigator_identifier_value": "identifier",
            "responsible_party_investigator_identifier_scheme": "scheme",
            "responsible_party_investigator_identifier_scheme_uri": "uri",
            "responsible_party_investigator_affiliation_name": "affiliation",
            "responsible_party_investigator_affiliation_identifier_value": "identifier",
            "responsible_party_investigator_affiliation_identifier_scheme": "scheme",
            "responsible_party_investigator_affiliation_identifier_scheme_uri": "uri",
            "lead_sponsor_name": "name",
            "lead_sponsor_identifier": "identifier",
            "lead_sponsor_identifier_scheme": "scheme",
            "lead_sponsor_identifier_scheme_uri": "uri",
        },
    )

    assert viewer_response.status_code == 403


def test_get_sponsors_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/sponsors' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the sponsors metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/sponsor")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/sponsor")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/sponsor")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/sponsor")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["responsible_party_type"] == "Sponsor"
    assert response_data["responsible_party_investigator_first_name"] == "name"
    assert response_data["responsible_party_investigator_last_name"] == "surname"
    assert (
        response_data["responsible_party_investigator_title"] == "title"
    )  # noqa: E501

    assert (
        response_data["responsible_party_investigator_identifier_value"] == "identifier"
    )
    assert response_data["responsible_party_investigator_identifier_scheme"] == "scheme"
    assert (
        response_data["responsible_party_investigator_identifier_scheme_uri"] == "uri"
    )
    assert (
        response_data["responsible_party_investigator_affiliation_name"]
        == "affiliation"
    )
    assert (
        response_data["responsible_party_investigator_affiliation_identifier_value"]
        == "identifier"
    )
    assert (
        response_data["responsible_party_investigator_affiliation_identifier_scheme"]
        == "scheme"
    )
    assert (
        response_data[
            "responsible_party_investigator_affiliation_identifier_scheme_uri"
        ]
        == "uri"
    )
    assert response_data["lead_sponsor_name"] == "name"
    assert response_data["lead_sponsor_identifier"] == "identifier"
    assert response_data["lead_sponsor_identifier_scheme"] == "scheme"
    assert response_data["lead_sponsor_identifier_scheme_uri"] == "uri"

    assert admin_response_data["responsible_party_type"] == "Sponsor"
    assert admin_response_data["responsible_party_investigator_first_name"] == "name"
    assert admin_response_data["responsible_party_investigator_last_name"] == "surname"
    assert (
        admin_response_data["responsible_party_investigator_title"] == "title"
    )  # noqa: E501
    assert (
        admin_response_data["responsible_party_investigator_identifier_value"]
        == "identifier"
    )
    assert (
        admin_response_data["responsible_party_investigator_identifier_scheme"]
        == "scheme"
    )
    assert (
        admin_response_data["responsible_party_investigator_identifier_scheme_uri"]
        == "uri"
    )
    assert (
        admin_response_data["responsible_party_investigator_affiliation_name"]
        == "affiliation"
    )
    assert (
        admin_response_data[
            "responsible_party_investigator_affiliation_identifier_value"
        ]
        == "identifier"
    )
    assert (
        admin_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme"
        ]
        == "scheme"
    )
    assert (
        admin_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme_uri"
        ]
        == "uri"
    )
    assert admin_response_data["lead_sponsor_name"] == "name"
    assert admin_response_data["lead_sponsor_identifier"] == "identifier"
    assert admin_response_data["lead_sponsor_identifier_scheme"] == "scheme"
    assert admin_response_data["lead_sponsor_identifier_scheme_uri"] == "uri"

    assert editor_response_data["responsible_party_type"] == "Sponsor"
    assert editor_response_data["responsible_party_investigator_first_name"] == "name"
    assert editor_response_data["responsible_party_investigator_last_name"] == "surname"
    assert (
        editor_response_data["responsible_party_investigator_title"] == "title"
    )  # noqa: E501
    assert (
        editor_response_data["responsible_party_investigator_identifier_value"]
        == "identifier"
    )
    assert (
        editor_response_data["responsible_party_investigator_identifier_scheme"]
        == "scheme"
    )
    assert (
        editor_response_data["responsible_party_investigator_identifier_scheme_uri"]
        == "uri"
    )
    assert (
        editor_response_data["responsible_party_investigator_affiliation_name"]
        == "affiliation"
    )
    assert (
        editor_response_data[
            "responsible_party_investigator_affiliation_identifier_value"
        ]
        == "identifier"
    )
    assert (
        editor_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme"
        ]
        == "scheme"
    )
    assert (
        editor_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme_uri"
        ]
        == "uri"
    )
    assert editor_response_data["lead_sponsor_name"] == "name"
    assert editor_response_data["lead_sponsor_identifier"] == "identifier"
    assert editor_response_data["lead_sponsor_identifier_scheme"] == "scheme"
    assert editor_response_data["lead_sponsor_identifier_scheme_uri"] == "uri"

    assert viewer_response_data["responsible_party_type"] == "Sponsor"
    assert viewer_response_data["responsible_party_investigator_first_name"] == "name"
    assert viewer_response_data["responsible_party_investigator_last_name"] == "surname"
    assert (
        viewer_response_data["responsible_party_investigator_title"] == "title"
    )  # noqa: E501
    assert (
        viewer_response_data["responsible_party_investigator_identifier_value"]
        == "identifier"
    )
    assert (
        viewer_response_data["responsible_party_investigator_identifier_scheme"]
        == "scheme"
    )
    assert (
        viewer_response_data["responsible_party_investigator_identifier_scheme_uri"]
        == "uri"
    )
    assert (
        viewer_response_data["responsible_party_investigator_affiliation_name"]
        == "affiliation"
    )
    assert (
        viewer_response_data[
            "responsible_party_investigator_affiliation_identifier_value"
        ]
        == "identifier"
    )
    assert (
        viewer_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme"
        ]
        == "scheme"
    )
    assert (
        viewer_response_data[
            "responsible_party_investigator_affiliation_identifier_scheme_uri"
        ]
        == "uri"
    )
    assert viewer_response_data["lead_sponsor_name"] == "name"
    assert viewer_response_data["lead_sponsor_identifier"] == "identifier"
    assert viewer_response_data["lead_sponsor_identifier_scheme"] == "scheme"
    assert viewer_response_data["lead_sponsor_identifier_scheme_uri"] == "uri"


# ------------------- STATUS METADATA ------------------- #
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

    admin_response = _admin_client.put(
        f"/study/{study_id}/metadata/status",
        json={
            "overall_status": "Withdrawn",
            "why_stopped": "admin-test",
            "start_date": "test",
            "start_date_type": "Actual",
            "completion_date": "admin date",
            "completion_date_type": "Actual",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["overall_status"] == "Withdrawn"
    assert admin_response_data["why_stopped"] == "admin-test"
    assert admin_response_data["start_date"] == "test"
    assert admin_response_data["start_date_type"] == "Actual"
    assert admin_response_data["completion_date"] == "admin date"
    assert admin_response_data["completion_date_type"] == "Actual"

    editor_response = _editor_client.put(
        f"/study/{study_id}/metadata/status",
        json={
            "overall_status": "Withdrawn",
            "why_stopped": "editor-test",
            "start_date": "2023-11-15 00:00:00",
            "start_date_type": "Actual",
            "completion_date": "completion date",
            "completion_date_type": "Actual",
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["overall_status"] == "Withdrawn"
    assert editor_response_data["why_stopped"] == "editor-test"
    assert editor_response_data["start_date"] == "2023-11-15 00:00:00"
    assert editor_response_data["start_date_type"] == "Actual"
    assert editor_response_data["completion_date"] == "completion date"
    assert editor_response_data["completion_date_type"] == "Actual"


def test_get_status_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    WHEN the '/study/{study_id}/metadata/status' endpoint is requested (GET)
    THEN check that the response is valid and retrieves the status metadata
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore

    response = _logged_in_client.get(f"/study/{study_id}/metadata/status")
    admin_response = _admin_client.get(f"/study/{study_id}/metadata/status")
    editor_response = _editor_client.get(f"/study/{study_id}/metadata/status")
    viewer_response = _viewer_client.get(f"/study/{study_id}/metadata/status")

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data["overall_status"] == "Withdrawn"
    assert response_data["why_stopped"] == "editor-test"
    assert response_data["start_date"] == "2023-11-15 00:00:00"
    assert response_data["start_date_type"] == "Actual"
    assert response_data["completion_date"] == "completion date"
    assert response_data["completion_date_type"] == "Actual"

    assert admin_response_data["overall_status"] == "Withdrawn"
    assert admin_response_data["why_stopped"] == "editor-test"
    assert admin_response_data["start_date"] == "2023-11-15 00:00:00"
    assert admin_response_data["start_date_type"] == "Actual"
    assert admin_response_data["completion_date"] == "completion date"
    assert admin_response_data["completion_date_type"] == "Actual"

    assert editor_response_data["overall_status"] == "Withdrawn"
    assert editor_response_data["why_stopped"] == "editor-test"
    assert editor_response_data["start_date"] == "2023-11-15 00:00:00"
    assert editor_response_data["start_date_type"] == "Actual"
    assert editor_response_data["completion_date"] == "completion date"
    assert editor_response_data["completion_date_type"] == "Actual"

    assert viewer_response_data["overall_status"] == "Withdrawn"
    assert viewer_response_data["why_stopped"] == "editor-test"
    assert viewer_response_data["start_date"] == "2023-11-15 00:00:00"
    assert viewer_response_data["start_date_type"] == "Actual"
    assert viewer_response_data["completion_date"] == "completion date"
    assert viewer_response_data["completion_date_type"] == "Actual"
