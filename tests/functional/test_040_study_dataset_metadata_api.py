# pylint: disable=too-many-lines
"""Tests for the Dataset's Metadata API endpoints"""
import json
from time import sleep

import pytest


# ------------------- ACCESS-RIGHTS METADATA ------------------- #
def test_post_dataset_access_rights_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/access-rights' endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset access metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access-rights",
        json={
            "access":
                {
                    "type": "type",
                    "description": "description",
                    "url": "google.com",
                    "url_last_checked": 123,
                },
            "rights": [
                {
                    "identifier": "Identifier",
                    "identifier_scheme": "Identifier Scheme",
                    "identifier_scheme_uri": "Identifier Scheme",
                    "rights": "Rights",
                    "uri": "URI",
                    "license_text": "license text",
                }
            ]
        },
    )

    response_data = json.loads(response.data)
    assert response.status_code == 200
    pytest.global_dataset_rights_id = response_data["rights"][0]["id"]

    assert response_data["access"]["type"] == "type"
    assert response_data["access"]["description"] == "description"
    assert response_data["access"]["url"] == "google.com"
    assert response_data["access"]["url_last_checked"] == 123

    assert response_data["rights"][0]["identifier"] == "Identifier"
    assert response_data["rights"][0]["identifier_scheme"] == "Identifier Scheme"
    assert response_data["rights"][0]["identifier_scheme_uri"] == "Identifier Scheme"
    assert response_data["rights"][0]["rights"] == "Rights"
    assert response_data["rights"][0]["uri"] == "URI"
    assert response_data["rights"][0]["license_text"] == "license text"


    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access-rights",
        json={
            "access": {
                "type": "admin type",
                 "description": "admin description",
                 "url": "google.com",
                 "url_last_checked": 123,
                },
            "rights": [
                {
                    "identifier": "Admin Identifier",
                    "identifier_scheme": "Identifier Scheme",
                    "identifier_scheme_uri": "Identifier Scheme",
                    "rights": "Rights",
                    "uri": "URI",
                    "license_text": "license text",
                }
            ]
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_rights_id_admin = admin_response_data["rights"][0]["id"]

    assert admin_response_data["access"]["type"] == "admin type"
    assert admin_response_data["access"]["description"] == "admin description"
    assert admin_response_data["access"]["url"] == "google.com"
    assert admin_response_data["access"]["url_last_checked"] == 123

    assert admin_response_data["rights"][0]["identifier"] == "Admin Identifier"
    assert admin_response_data["rights"][0]["identifier_scheme"] == "Identifier Scheme"
    assert admin_response_data["rights"][0]["identifier_scheme_uri"] == "Identifier Scheme"
    assert admin_response_data["rights"][0]["rights"] == "Rights"
    assert admin_response_data["rights"][0]["uri"] == "URI"
    assert admin_response_data["rights"][0]["license_text"] == "license text"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access-rights",
        json={
            "access":
                {
                    "type": "editor type",
                    "description": "editor description",
                    "url": "google.com",
                    "url_last_checked": 123,
                },
            "rights": [
                {
                    "identifier": "Editor Identifier",
                    "identifier_scheme": "Identifier Scheme",
                    "identifier_scheme_uri": "Identifier Scheme",
                    "rights": "Rights",
                    "uri": "URI",
                    "license_text": "license text",
                }
            ]
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_rights_id_editor = editor_response_data["rights"][0]["id"]

    assert editor_response_data["access"]["type"] == "editor type"
    assert editor_response_data["access"]["description"] == "editor description"
    assert editor_response_data["access"]["url"] == "google.com"
    assert editor_response_data["access"]["url_last_checked"] == 123

    assert editor_response_data["rights"][0]["identifier"] == "Editor Identifier"
    assert editor_response_data["rights"][0]["identifier_scheme"] == "Identifier Scheme"
    assert editor_response_data["rights"][0]["identifier_scheme_uri"] == "Identifier Scheme"
    assert editor_response_data["rights"][0]["rights"] == "Rights"
    assert editor_response_data["rights"][0]["uri"] == "URI"
    assert editor_response_data["rights"][0]["license_text"] == "license text"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access-rights",
        json={
            "access":
                {
                    "type": "viewer type",
                    "description": "viewer description",
                    "url": "google.com",
                    "url_last_checked": 123,
                },
            "rights": [
                {
                    "identifier": "Viewer Identifier",
                    "identifier_scheme": "Identifier Scheme",
                    "identifier_scheme_uri": "Identifier Scheme",
                    "rights": "Rights",
                    "uri": "URI",
                    "license_text": "license text",
                }
            ]
        },
    )

    assert viewer_response.status_code == 403


def test_get_dataset_access_rights_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/access' endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset access metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access-rights"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access-rights"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access-rights"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/access-rights"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # Since editor was the last successful PUT request, the response data should match
    assert response_data["access"]["type"] == "editor type"
    assert response_data["access"]["description"] == "editor description"
    assert response_data["access"]["url"] == "google.com"
    assert response_data["access"]["url_last_checked"] == 123
###
    assert response_data["rights"][0]["identifier"] == "Identifier"
    assert response_data["rights"][0]["identifier_scheme"] == "Identifier Scheme"
    assert response_data["rights"][0]["identifier_scheme_uri"] == "Identifier Scheme"
    assert response_data["rights"][0]["rights"] == "Rights"
    assert response_data["rights"][0]["uri"] == "URI"
    assert response_data["rights"][0]["license_text"] == "license text"

    assert admin_response_data["rights"][0]["identifier"] == "Identifier"
    assert admin_response_data["rights"][0]["identifier_scheme"] == "Identifier Scheme"
    assert admin_response_data["rights"][0]["identifier_scheme_uri"] == "Identifier Scheme"
    assert admin_response_data["rights"][0]["rights"] == "Rights"
    assert admin_response_data["rights"][0]["uri"] == "URI"
    assert admin_response_data["rights"][0]["license_text"] == "license text"

    assert editor_response_data["rights"][0]["identifier"] == "Identifier"
    assert editor_response_data["rights"][0]["identifier_scheme"] == "Identifier Scheme"
    assert editor_response_data["rights"][0]["identifier_scheme_uri"] == "Identifier Scheme"
    assert editor_response_data["rights"][0]["rights"] == "Rights"
    assert editor_response_data["rights"][0]["uri"] == "URI"
    assert editor_response_data["rights"][0]["license_text"] == "license text"

    assert response_data["rights"][1]["identifier"] == "Admin Identifier"
    assert response_data["rights"][1]["identifier_scheme"] == "Identifier Scheme"
    assert response_data["rights"][1]["identifier_scheme_uri"] == "Identifier Scheme"
    assert response_data["rights"][1]["rights"] == "Rights"
    assert response_data["rights"][1]["uri"] == "URI"
    assert response_data["rights"][1]["license_text"] == "license text"

    assert admin_response_data["rights"][1]["identifier"] == "Admin Identifier"
    assert admin_response_data["rights"][1]["identifier_scheme"] == "Identifier Scheme"
    assert admin_response_data["rights"][1]["identifier_scheme_uri"] == "Identifier Scheme"
    assert admin_response_data["rights"][1]["rights"] == "Rights"
    assert admin_response_data["rights"][1]["uri"] == "URI"
    assert admin_response_data["rights"][1]["license_text"] == "license text"

    assert editor_response_data["rights"][1]["identifier"] == "Admin Identifier"
    assert editor_response_data["rights"][1]["identifier_scheme"] == "Identifier Scheme"
    assert editor_response_data["rights"][1]["identifier_scheme_uri"] == "Identifier Scheme"
    assert editor_response_data["rights"][1]["rights"] == "Rights"
    assert editor_response_data["rights"][1]["uri"] == "URI"
    assert editor_response_data["rights"][1]["license_text"] == "license text"

    assert response_data["rights"][2]["identifier"] == "Editor Identifier"
    assert response_data["rights"][2]["identifier_scheme"] == "Identifier Scheme"
    assert response_data["rights"][2]["identifier_scheme_uri"] == "Identifier Scheme"
    assert response_data["rights"][2]["rights"] == "Rights"
    assert response_data["rights"][2]["uri"] == "URI"
    assert response_data["rights"][2]["license_text"] == "license text"

    assert admin_response_data["rights"][2]["identifier"] == "Editor Identifier"
    assert admin_response_data["rights"][2]["identifier_scheme"] == "Identifier Scheme"
    assert admin_response_data["rights"][2]["identifier_scheme_uri"] == "Identifier Scheme"
    assert admin_response_data["rights"][2]["rights"] == "Rights"
    assert admin_response_data["rights"][2]["uri"] == "URI"
    assert admin_response_data["rights"][2]["license_text"] == "license text"

    assert editor_response_data["rights"][2]["identifier"] == "Editor Identifier"
    assert editor_response_data["rights"][2]["identifier_scheme"] == "Identifier Scheme"
    assert editor_response_data["rights"][2]["identifier_scheme_uri"] == "Identifier Scheme"
    assert editor_response_data["rights"][2]["rights"] == "Rights"
    assert editor_response_data["rights"][2]["uri"] == "URI"
    assert editor_response_data["rights"][2]["license_text"] == "license text"

    assert viewer_response_data["rights"][0]["identifier"] == "Identifier"
    assert viewer_response_data["rights"][0]["identifier_scheme"] == "Identifier Scheme"
    assert viewer_response_data["rights"][0]["identifier_scheme_uri"] == "Identifier Scheme"
    assert viewer_response_data["rights"][0]["rights"] == "Rights"
    assert viewer_response_data["rights"][0]["uri"] == "URI"
    assert viewer_response_data["rights"][0]["license_text"] == "license text"

    assert viewer_response_data["rights"][1]["identifier"] == "Admin Identifier"
    assert viewer_response_data["rights"][1]["identifier_scheme"] == "Identifier Scheme"
    assert viewer_response_data["rights"][1]["identifier_scheme_uri"] == "Identifier Scheme"
    assert viewer_response_data["rights"][1]["rights"] == "Rights"
    assert viewer_response_data["rights"][1]["uri"] == "URI"
    assert viewer_response_data["rights"][1]["license_text"] == "license text"

    assert viewer_response_data["rights"][2]["identifier"] == "Editor Identifier"
    assert viewer_response_data["rights"][2]["identifier_scheme"] == "Identifier Scheme"
    assert viewer_response_data["rights"][2]["identifier_scheme_uri"] == "Identifier Scheme"
    assert viewer_response_data["rights"][2]["rights"] == "Rights"
    assert viewer_response_data["rights"][2]["uri"] == "URI"
    assert viewer_response_data["rights"][2]["license_text"] == "license text"
#######
    assert admin_response_data["access"]["type"] == "editor type"
    assert admin_response_data["access"]["description"] == "editor description"
    assert admin_response_data["access"]["url"] == "google.com"
    assert admin_response_data["access"]["url_last_checked"] == 123

    assert editor_response_data["access"]["type"] == "editor type"
    assert editor_response_data["access"]["description"] == "editor description"
    assert editor_response_data["access"]["url"] == "google.com"
    assert editor_response_data["access"]["url_last_checked"] == 123

    assert viewer_response_data["access"]["type"] == "editor type"
    assert viewer_response_data["access"]["description"] == "editor description"
    assert viewer_response_data["access"]["url"] == "google.com"
    assert viewer_response_data["access"]["url_last_checked"] == 123

# ------------------- GENERAL INFORMATION METADATA ------------------- #
def test_post_dataset_general_information_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/general-description'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    general information metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/general-information",
        json={
            "titles": [{"title": "Owner Title", "type": "Subtitle"}],
            "descriptions": [{"description": "Owner Description", "type": "Methods"}],
            "dates": [{"date": 20210101, "type": "Accepted", "information": "Info"}]
              },
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 200
    response_data = json.loads(response.data)

    pytest.global_dataset_title_id = response_data["titles"][0]["id"]
    pytest.global_dataset_description_id = response_data["descriptions"][0]["id"]
    pytest.global_dataset_date_id = response_data["dates"][0]["id"]

    assert response_data["titles"][0]["title"] == "Owner Title"
    assert response_data["titles"][0]["type"] == "Subtitle"
    assert response_data["descriptions"][0]["description"] == "Owner Description"
    assert response_data["descriptions"][0]["type"] == "Methods"

    assert response_data["dates"][0]["date"] == 20210101
    assert response_data["dates"][0]["type"] == "Accepted"
    assert response_data["dates"][0]["information"] == "Info"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/general-information",
        json={
                "titles": [{"title": "Admin Title", "type": "Subtitle"}],
                "descriptions": [{"description": "Admin Description", "type": "Methods"}],
                "dates": [{"date": 20210102, "type": "Accepted", "information": "Info"}],
              },
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    # assert admin_response.status_code == 200

    admin_response_data = json.loads(admin_response.data)

    pytest.global_dataset_title_id_admin = admin_response_data["titles"][0]["id"]
    pytest.global_dataset_description_id_admin = admin_response_data["descriptions"][0]["id"]
    pytest.global_dataset_date_id_admin = admin_response_data["dates"][0]["id"]

    assert admin_response_data["titles"][0]["title"] == "Admin Title"
    assert admin_response_data["titles"][0]["type"] == "Subtitle"
    assert admin_response_data["descriptions"][0]["description"] == "Admin Description"
    assert admin_response_data["descriptions"][0]["type"] == "Methods"

    assert admin_response_data["dates"][0]["date"] == 20210102
    assert admin_response_data["dates"][0]["type"] == "Accepted"
    assert admin_response_data["dates"][0]["information"] == "Info"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/general-information",
        json= {
                "titles": [{"title": "Editor Title", "type": "Subtitle"}],
                "descriptions": [{"description": "Editor Description", "type": "Methods"}],
                "dates": [{"date": 20210103, "type": "Accepted", "information": "Info"}],
              },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_title_id_editor = editor_response_data["titles"][0]["id"]
    pytest.global_dataset_description_id_editor = editor_response_data["descriptions"][0]["id"]
    pytest.global_dataset_date_id_editor = editor_response_data["dates"][0]["id"]

    assert editor_response_data["titles"][0]["title"] == "Editor Title"
    assert editor_response_data["titles"][0]["type"] == "Subtitle"

    assert editor_response_data["descriptions"][0]["description"] == "Editor Description"
    assert editor_response_data["descriptions"][0]["type"] == "Methods"

    assert editor_response_data["dates"][0]["date"] == 20210103
    assert editor_response_data["dates"][0]["type"] == "Accepted"
    assert editor_response_data["dates"][0]["information"] == "Info"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/general-information",
        json={
            "titles": [{"title": "Viewer Title", "type": "Subtitle"}],
            "descriptions": [{"description": "Viewer Description", "type": "Methods"}],
            "dates": [{"date": 20210103, "type": "Accepted", "information": "Info"}]
            },
    )

    assert viewer_response.status_code == 403


# ------------------- DELETE GENERAL INFORMATION METADATA ------------------- #
def test_get_dataset_general_information_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/general-information'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    general information metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/general-information"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/general-information"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/general-information"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/general-information"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    owner_titles = response_data["titles"]
    owner_descriptions = response_data["descriptions"]
    owner_dates = response_data["dates"]

    admin_titles = admin_response_data["titles"]
    admin_descriptions = admin_response_data["descriptions"]
    admin_dates = admin_response_data["dates"]

    editor_titles = editor_response_data["titles"]
    editor_descriptions = editor_response_data["descriptions"]
    editor_dates = editor_response_data["dates"]

    viewer_titles = viewer_response_data["titles"]
    viewer_descriptions = viewer_response_data["descriptions"]
    viewer_dates = viewer_response_data["dates"]

    assert len(owner_titles) == 4
    assert len(admin_titles) == 4
    assert len(editor_titles) == 4
    assert len(viewer_titles) == 4

    # search for maintitle index
    # pylint: disable=line-too-long
    main_title = next(
        (index for (index, d) in enumerate(owner_titles) if d["type"] == "MainTitle"),
        None,
    )
    a_main_title = next(
        (
            index
            for (index, d) in enumerate(admin_response_data["titles"])
            if d["type"] == "MainTitle"
        ),
        None,
    )
    e_main_title = next(
        (
            index
            for (index, d) in enumerate(editor_titles)
            if d["type"] == "MainTitle"
        ),
        None,
    )
    v_main_title = next(
        (
            index
            for (index, d) in enumerate(viewer_titles)
            if d["type"] == "MainTitle"
        ),
        None,
    )
    # search for admin title index
    admin_title = next(
        (
            index
            for (index, d) in enumerate(owner_titles)
            if d["title"] == "Admin Title"
        ),
        None,
    )
    a_admin_title = next(
        (
            index
            for (index, d) in enumerate(admin_titles)
            if d["title"] == "Admin Title"
        ),
        None,
    )
    e_admin_title = next(
        (
            index
            for (index, d) in enumerate(editor_titles)
            if d["title"] == "Admin Title"
        ),
        None,
    )
    v_admin_title = next(
        (
            index
            for (index, d) in enumerate(viewer_titles)
            if d["title"] == "Admin Title"
        ),
        None,
    )

    # search for editor title index
    editor_title = next(
        (
            index
            for (index, d) in enumerate(owner_titles)
            if d["title"] == "Editor Title"
        ),
        None,
    )
    a_editor_title = next(
        (
            index
            for (index, d) in enumerate(admin_titles)
            if d["title"] == "Editor Title"
        ),
        None,
    )
    e_editor_title = next(
        (
            index
            for (index, d) in enumerate(editor_titles)
            if d["title"] == "Editor Title"
        ),
        None,
    )
    v_editor_title = next(
        (
            index
            for (index, d) in enumerate(viewer_titles)
            if d["title"] == "Editor Title"
        ),
        None,
    )

    # search for owner title index
    own_title = next(
        (
            index
            for (index, d) in enumerate(owner_titles)
            if d["title"] == "Owner Title"
        ),
        None,
    )
    a_own_title = next(
        (
            index
            for (index, d) in enumerate(admin_titles)
            if d["title"] == "Owner Title"
        ),
        None,
    )
    e_own_title = next(
        (
            index
            for (index, d) in enumerate(editor_titles)
            if d["title"] == "Owner Title"
        ),
        None,
    )
    v_own_title = next(
        (
            index
            for (index, d) in enumerate(viewer_titles)
            if d["title"] == "Owner Title"
        ),
        None,
    )

    assert owner_titles[main_title]["title"] == "Dataset Title"
    assert owner_titles[main_title]["type"] == "MainTitle"
    assert owner_titles[own_title]["title"] == "Owner Title"
    assert owner_titles[own_title]["type"] == "Subtitle"
    assert owner_titles[admin_title]["title"] == "Admin Title"
    assert owner_titles[admin_title]["type"] == "Subtitle"
    assert owner_titles[editor_title]["title"] == "Editor Title"
    assert owner_titles[editor_title]["type"] == "Subtitle"

    assert admin_titles[a_main_title]["title"] == "Dataset Title"
    assert admin_titles[a_main_title]["type"] == "MainTitle"
    assert admin_titles[a_own_title]["title"] == "Owner Title"
    assert admin_titles[a_own_title]["type"] == "Subtitle"
    assert admin_titles[a_admin_title]["title"] == "Admin Title"
    assert admin_titles[a_admin_title]["type"] == "Subtitle"
    assert admin_titles[a_editor_title]["title"] == "Editor Title"
    assert admin_titles[a_editor_title]["type"] == "Subtitle"

    assert editor_titles[e_main_title]["title"] == "Dataset Title"
    assert editor_titles[e_main_title]["type"] == "MainTitle"
    assert editor_titles[e_own_title]["title"] == "Owner Title"
    assert editor_titles[e_own_title]["type"] == "Subtitle"
    assert editor_titles[e_admin_title]["title"] == "Admin Title"
    assert editor_titles[e_admin_title]["type"] == "Subtitle"
    assert editor_titles[e_editor_title]["title"] == "Editor Title"
    assert editor_titles[e_editor_title]["type"] == "Subtitle"

    assert viewer_titles[v_main_title]["title"] == "Dataset Title"
    assert viewer_titles[v_main_title]["type"] == "MainTitle"
    assert viewer_titles[v_own_title]["title"] == "Owner Title"
    assert viewer_titles[v_own_title]["type"] == "Subtitle"
    assert viewer_titles[v_admin_title]["title"] == "Admin Title"
    assert viewer_titles[v_admin_title]["type"] == "Subtitle"
    assert viewer_titles[v_editor_title]["title"] == "Editor Title"
    assert viewer_titles[v_editor_title]["type"] == "Subtitle"


    assert len(owner_descriptions) == 4
    assert len(admin_descriptions) == 4
    assert len(editor_descriptions) == 4
    assert len(viewer_descriptions) == 4

    # seacrch for type abstract index
    main_descrip = next(
        (index for (index, d) in enumerate(owner_descriptions) if d["type"] == "Abstract"),
        None,
    )
    a_main_descrip = next(
        (
            index
            for (index, d) in enumerate(admin_descriptions)
            if d["type"] == "Abstract"
        ),
        None,
    )
    e_main_descrip = next(
        (
            index
            for (index, d) in enumerate(editor_descriptions)
            if d["type"] == "Abstract"
        ),
        None,
    )
    v_main_descrip = next(
        (
            index
            for (index, d) in enumerate(viewer_descriptions)
            if d["type"] == "Abstract"
        ),
        None,
    )
    # search for owner description
    # pylint: disable=line-too-long
    own_descrip = next(
        (
            index
            for (index, d) in enumerate(owner_descriptions)
            if d["description"] == "Owner Description"
        ),
        None,
    )
    a_own_descrip = next(
        (
            index
            for (index, d) in enumerate(admin_descriptions)
            if d["description"] == "Owner Description"
        ),
        None,
    )
    e_own_descrip = next(
        (
            index
            for (index, d) in enumerate(editor_descriptions)
            if d["description"] == "Owner Description"
        ),
        None,
    )
    v_own_descrip = next(
        (
            index
            for (index, d) in enumerate(viewer_descriptions)
            if d["description"] == "Owner Description"
        ),
        None,
    )

    # search for admin description
    admin_descrip = next(
        (
            index
            for (index, d) in enumerate(owner_descriptions)
            if d["description"] == "Admin Description"
        ),
        None,
    )
    a_admin_descrip = next(
        (
            index
            for (index, d) in enumerate(admin_descriptions)
            if d["description"] == "Admin Description"
        ),
        None,
    )
    e_admin_descrip = next(
        (
            index
            for (index, d) in enumerate(editor_descriptions)
            if d["description"] == "Admin Description"
        ),
        None,
    )
    v_admin_descrip = next(
        (
            index
            for (index, d) in enumerate(viewer_descriptions)
            if d["description"] == "Admin Description"
        ),
        None,
    )

    # search for editor description
    edit_descrip = next(
        (
            index
            for (index, d) in enumerate(owner_descriptions)
            if d["description"] == "Editor Description"
        ),
        None,
    )
    a_edit_descrip = next(
        (
            index
            for (index, d) in enumerate(admin_descriptions)
            if d["description"] == "Editor Description"
        ),
        None,
    )
    e_edit_descrip = next(
        (
            index
            for (index, d) in enumerate(editor_descriptions)
            if d["description"] == "Editor Description"
        ),
        None,
    )
    v_edit_descrip = next(
        (
            index
            for (index, d) in enumerate(viewer_descriptions)
            if d["description"] == "Editor Description"
        ),
        None,
    )

    assert owner_descriptions[main_descrip]["description"] == "Dataset Description"
    assert owner_descriptions[main_descrip]["type"] == "Abstract"
    assert owner_descriptions[own_descrip]["description"] == "Owner Description"
    assert owner_descriptions[own_descrip]["type"] == "Methods"
    assert owner_descriptions[admin_descrip]["description"] == "Admin Description"
    assert owner_descriptions[admin_descrip]["type"] == "Methods"
    assert owner_descriptions[edit_descrip]["description"] == "Editor Description"
    assert owner_descriptions[edit_descrip]["type"] == "Methods"

    assert admin_descriptions[a_main_descrip]["description"] == "Dataset Description"
    assert admin_descriptions[a_main_descrip]["type"] == "Abstract"
    assert admin_descriptions[a_own_descrip]["description"] == "Owner Description"
    assert admin_descriptions[a_own_descrip]["type"] == "Methods"
    assert admin_descriptions[a_admin_descrip]["description"] == "Admin Description"
    assert admin_descriptions[a_admin_descrip]["type"] == "Methods"
    assert admin_descriptions[a_edit_descrip]["description"] == "Editor Description"
    assert admin_descriptions[a_edit_descrip]["type"] == "Methods"

    assert editor_descriptions[e_main_descrip]["description"] == "Dataset Description"
    assert editor_descriptions[e_main_descrip]["type"] == "Abstract"
    assert editor_descriptions[e_own_descrip]["description"] == "Owner Description"
    assert editor_descriptions[e_own_descrip]["type"] == "Methods"
    assert editor_descriptions[e_admin_descrip]["description"] == "Admin Description"
    assert editor_descriptions[e_admin_descrip]["type"] == "Methods"
    assert editor_descriptions[e_edit_descrip]["description"] == "Editor Description"
    assert editor_descriptions[e_edit_descrip]["type"] == "Methods"

    assert viewer_descriptions[v_main_descrip]["description"] == "Dataset Description"
    assert viewer_descriptions[v_main_descrip]["type"] == "Abstract"
    assert viewer_descriptions[v_own_descrip]["description"] == "Owner Description"
    assert viewer_descriptions[v_own_descrip]["type"] == "Methods"
    assert viewer_descriptions[v_admin_descrip]["description"] == "Admin Description"
    assert viewer_descriptions[v_admin_descrip]["type"] == "Methods"
    assert viewer_descriptions[v_edit_descrip]["description"] == "Editor Description"
    assert viewer_descriptions[v_edit_descrip]["type"] == "Methods"

    assert len(owner_dates) == 3
    assert len(admin_dates) == 3
    assert len(editor_dates) == 3
    assert len(viewer_dates) == 3

    assert owner_dates[0]["date"] == 20210101
    assert owner_dates[0]["type"] == "Accepted"
    assert owner_dates[0]["information"] == "Info"
    assert owner_dates[1]["date"] == 20210102
    assert owner_dates[1]["type"] == "Accepted"
    assert owner_dates[1]["information"] == "Info"
    assert owner_dates[2]["date"] == 20210103
    assert owner_dates[2]["type"] == "Accepted"

    assert admin_dates[0]["date"] == 20210101
    assert admin_dates[0]["type"] == "Accepted"
    assert admin_dates[0]["information"] == "Info"
    assert admin_dates[1]["date"] == 20210102
    assert admin_dates[1]["type"] == "Accepted"
    assert admin_dates[1]["information"] == "Info"
    assert admin_dates[2]["date"] == 20210103
    assert admin_dates[2]["type"] == "Accepted"

    assert editor_dates[0]["date"] == 20210101
    assert editor_dates[0]["type"] == "Accepted"
    assert editor_dates[0]["information"] == "Info"
    assert editor_dates[1]["date"] == 20210102
    assert editor_dates[1]["type"] == "Accepted"
    assert editor_dates[1]["information"] == "Info"
    assert editor_dates[2]["date"] == 20210103
    assert editor_dates[2]["type"] == "Accepted"

    assert viewer_dates[0]["date"] == 20210101
    assert viewer_dates[0]["type"] == "Accepted"
    assert viewer_dates[0]["information"] == "Info"
    assert viewer_dates[1]["date"] == 20210102
    assert viewer_dates[1]["type"] == "Accepted"
    assert viewer_dates[1]["information"] == "Info"
    assert viewer_dates[2]["date"] == 20210103
    assert viewer_dates[2]["type"] == "Accepted"


# ------------------- DELETE TITLE METADATA ------------------- #
def test_delete_dataset_title_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/title/{title_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    title metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    title_id = pytest.global_dataset_title_id
    admin_title_id = pytest.global_dataset_title_id_admin
    editor_title_id = pytest.global_dataset_title_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title/{title_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title/{title_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title/{admin_title_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/title/{editor_title_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DELETE DESCRIPTION METADATA ------------------- #
def test_delete_dataset_description_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/description'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    description_id = pytest.global_dataset_description_id
    admin_description_id = pytest.global_dataset_description_id_admin
    editor_description_id = pytest.global_dataset_description_id_editor

    # Verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{description_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{description_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{admin_description_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/description/{editor_description_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DELETE DATE METADATA ------------------- #
def test_delete_dataset_date_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/date'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset date metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    date_id = pytest.global_dataset_date_id
    admin_date_id = pytest.global_dataset_date_id_admin
    editor_date_id = pytest.global_dataset_date_id_editor

    # Verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{date_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{date_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{admin_date_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/date/{editor_date_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DATASET TEAM METADATA ------------------- #
def test_post_dataset_team_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/team'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    team metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/team",
        json=
            {
            "creators": [
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
            "contributors": [
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
            "managing_organization": {
                "name": "Managing Organization Name",
                "identifier": "identifier",
                "identifier_scheme": "identifier scheme",
                "identifier_scheme_uri": "identifier scheme_uri",
            },
            "funders": [
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
            }

    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 200
    response_data = json.loads(response.data)

    creators = response_data["creators"]
    contributors = response_data["contributors"]
    funders = response_data["funders"]
    managing_organization = response_data["managing_organization"]

    pytest.global_dataset_funder_id = funders[0]["id"]
    pytest.global_dataset_creator_id = creators[0]["id"]
    pytest.global_dataset_contributor_id = contributors[0]["id"]

    assert creators[0]["given_name"] == "Given Name here"
    assert creators[0]["family_name"] == "Family Name here"
    assert creators[0]["name_type"] == "Personal"
    assert creators[0]["name_identifier"] == "Name identifier"
    assert creators[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert creators[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert creators[0]["creator"] is True
    assert creators[0]["affiliations"][0]["name"] == "Test"
    assert creators[0]["affiliations"][0]["identifier"] == "yes"
    assert creators[0]["affiliations"][0]["scheme"] == "uh"
    assert creators[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert funders[0]["name"] == "Name"
    assert funders[0]["award_number"] == "award number"
    assert funders[0]["award_title"] == "Award Title"
    assert funders[0]["award_uri"] == "Award URI"
    assert funders[0]["identifier"] == "Identifier"
    assert funders[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert funders[0]["identifier_type"] == "Identifier Type"

    assert contributors[0]["given_name"] == "Given Name here"
    assert contributors[0]["family_name"] == "Family Name here"
    assert contributors[0]["name_type"] == "Personal"
    assert contributors[0]["name_identifier"] == "Name identifier"
    assert contributors[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert contributors[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert contributors[0]["creator"] is False
    assert contributors[0]["contributor_type"] == "Con Type"
    assert contributors[0]["affiliations"][0]["name"] == "Test"
    assert contributors[0]["affiliations"][0]["identifier"] == "yes"
    assert contributors[0]["affiliations"][0]["scheme"] == "uh"
    assert contributors[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert managing_organization["name"] == "Managing Organization Name"
    assert managing_organization["identifier"] == "identifier"
    assert managing_organization["identifier_scheme"] == "identifier scheme"
    assert managing_organization["identifier_scheme_uri"] == "identifier scheme_uri"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/team",
        json=
            {
            "creators": [
                {
                    "given_name": "Admin Given Name here",
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
            "contributors": [
                {
                    "given_name": "Admin Given Name here",
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
            "managing_organization": {
                "name": "admin Managing Organization Name",
                "identifier": "identifier",
                "identifier_scheme": "identifier scheme",
                "identifier_scheme_uri": "identifier scheme_uri",
        },
            "funders": [
                 {
                "name": "Admin Name",
                "award_number": "award number",
                "award_title": "Award Title",
                "award_uri": "Award URI",
                "identifier": "Identifier",
                "identifier_scheme_uri": "Identifier Scheme URI",
                "identifier_type": "Identifier Type",
            }
             ],
            }

    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    admin_creators = admin_response_data["creators"]
    admin_managing_organization = admin_response_data["managing_organization"]
    admin_funders = admin_response_data["funders"]
    admin_contributors = admin_response_data["contributors"]

    pytest.global_dataset_funder_id_admin = admin_funders[0]["id"]
    pytest.global_dataset_creator_id_admin = admin_creators[0]["id"]
    pytest.global_dataset_contributor_id_admin = admin_contributors[0]["id"]

    assert admin_creators[0]["given_name"] == "Admin Given Name here"
    assert admin_creators[0]["family_name"] == "Family Name here"
    assert admin_creators[0]["name_type"] == "Personal"
    assert admin_creators[0]["name_identifier"] == "Name identifier"
    assert admin_creators[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_creators[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_creators[0]["creator"] is True
    assert admin_creators[0]["affiliations"][0]["name"] == "Test"
    assert admin_creators[0]["affiliations"][0]["identifier"] == "yes"
    assert admin_creators[0]["affiliations"][0]["scheme"] == "uh"
    assert admin_creators[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert admin_funders[0]["name"] == "Admin Name"
    assert admin_funders[0]["award_number"] == "award number"
    assert admin_funders[0]["award_title"] == "Award Title"
    assert admin_funders[0]["award_uri"] == "Award URI"
    assert admin_funders[0]["identifier"] == "Identifier"
    assert admin_funders[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert admin_funders[0]["identifier_type"] == "Identifier Type"

    assert admin_contributors[0]["given_name"] == "Admin Given Name here"
    assert admin_contributors[0]["family_name"] == "Family Name here"
    assert admin_contributors[0]["name_type"] == "Personal"
    assert admin_contributors[0]["name_identifier"] == "Name identifier"
    assert admin_contributors[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_contributors[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_contributors[0]["creator"] is False
    assert admin_contributors[0]["contributor_type"] == "Con Type"
    assert admin_contributors[0]["affiliations"][0]["name"] == "Test"
    assert admin_contributors[0]["affiliations"][0]["identifier"] == "yes"
    assert admin_contributors[0]["affiliations"][0]["scheme"] == "uh"
    assert admin_contributors[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert admin_managing_organization["name"] == "admin Managing Organization Name"
    assert admin_managing_organization["identifier"] == "identifier"
    assert admin_managing_organization["identifier_scheme"] == "identifier scheme"
    assert admin_managing_organization["identifier_scheme_uri"] == "identifier scheme_uri"


    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/team",
        json=
        {
            "creators": [
            {
                "given_name": "Editor Given Name here",
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
            "contributors": [
                {
                    "given_name": "Editor Given Name here",
                    "family_name": "Editor Family Name here",
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
            "managing_organization": {
                "name": "editor Managing Organization Name",
                "identifier": "identifier",
                "identifier_scheme": "identifier scheme",
                "identifier_scheme_uri": "identifier scheme_uri",
            },
            "funders": [
                {
                    "name": "Editor Name",
                    "award_number": "award number",
                    "award_title": "Award Title",
                    "award_uri": "Award URI",
                    "identifier": "Identifier",
                    "identifier_scheme_uri": "Identifier Scheme URI",
                    "identifier_type": "Identifier Type",
                }
            ],
        }
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    editor_creators = editor_response_data["creators"]
    editor_managing_organization = editor_response_data["managing_organization"]
    editor_funders = editor_response_data["funders"]
    editor_contributors = editor_response_data["contributors"]

    pytest.global_dataset_funder_id_editor = editor_funders[0]["id"]
    pytest.global_dataset_creator_id_editor = editor_creators[0]["id"]
    pytest.global_dataset_contributor_id_editor = editor_contributors[0]["id"]

    assert editor_creators[0]["given_name"] == "Editor Given Name here"
    assert editor_creators[0]["family_name"] == "Family Name here"
    assert editor_creators[0]["name_type"] == "Personal"
    assert editor_creators[0]["name_identifier"] == "Name identifier"
    assert editor_creators[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_creators[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_creators[0]["creator"] is True
    assert editor_creators[0]["affiliations"][0]["name"] == "Test"
    assert editor_creators[0]["affiliations"][0]["identifier"] == "yes"
    assert editor_creators[0]["affiliations"][0]["scheme"] == "uh"
    assert editor_creators[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert editor_contributors[0]["given_name"] == "Editor Given Name here"
    assert editor_contributors[0]["family_name"] == "Editor Family Name here"
    assert editor_contributors[0]["name_type"] == "Personal"
    assert editor_contributors[0]["name_identifier"] == "Name identifier"
    assert editor_contributors[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_contributors[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_contributors[0]["creator"] is False
    assert editor_contributors[0]["contributor_type"] == "Con Type"
    assert editor_contributors[0]["affiliations"][0]["name"] == "Test"
    assert editor_contributors[0]["affiliations"][0]["identifier"] == "yes"
    assert editor_contributors[0]["affiliations"][0]["scheme"] == "uh"
    assert editor_contributors[0]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert editor_funders[0]["name"] == "Editor Name"
    assert editor_funders[0]["award_number"] == "award number"
    assert editor_funders[0]["award_title"] == "Award Title"
    assert editor_funders[0]["award_uri"] == "Award URI"
    assert editor_funders[0]["identifier"] == "Identifier"
    assert (
        editor_funders[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    )  # pylint: disable=line-too-long
    assert editor_funders[0]["identifier_type"] == "Identifier Type"

    assert editor_managing_organization["name"] == "editor Managing Organization Name"
    assert editor_managing_organization["identifier"] == "identifier"
    assert editor_managing_organization["identifier_scheme"] == "identifier scheme"
    assert editor_managing_organization["identifier_scheme_uri"] == "identifier scheme_uri"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/team",
        json= {
            "creators": [
                {
                    "given_name": "Viewer Given Name here",
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
            "contributors": [
            {
                "given_name": "Viewer Given Name here",
                "family_name": "Viewer Family Name here",
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
            "managing_organization": {
                "name": "editor Managing Organization Name",
                "identifier": "identifier",
                "identifier_scheme": "identifier scheme",
                "identifier_scheme_uri": "identifier scheme_uri",
            },
            "funders": [
                {
                    "name": "Viewer Name",
                    "award_number": "award number",
                    "award_title": "Award Title",
                    "award_uri": "Award URI",
                    "identifier": "Identifier",
                    "identifier_scheme_uri": "Identifier Scheme URI",
                    "identifier_type": "Identifier Type",
                }
            ],
        }
    )

    assert viewer_response.status_code == 403


def test_get_dataset_team_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/team'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    team metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/team"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/team"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/team"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/team"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    creators = response_data["creators"]
    contributors = response_data["contributors"]
    funders = response_data["funders"]
    managing_organization = response_data["managing_organization"]

    admin_creators = admin_response_data["creators"]
    admin_managing_organization = admin_response_data["managing_organization"]
    admin_funders = admin_response_data["funders"]
    admin_contributors = admin_response_data["contributors"]

    editor_creators = editor_response_data["creators"]
    editor_managing_organization = editor_response_data["managing_organization"]
    editor_funders = editor_response_data["funders"]
    editor_contributors = editor_response_data["contributors"]

    viewer_creators = editor_response_data["creators"]
    viewer_managing_organization = editor_response_data["managing_organization"]
    viewer_funders = editor_response_data["funders"]
    viewer_contributors = editor_response_data["contributors"]

    assert len(funders) == 3
    assert len(admin_funders) == 3
    assert len(editor_funders) == 3
    assert len(viewer_funders) == 3

    assert funders[0]["name"] == "Name"
    assert funders[0]["award_number"] == "award number"
    assert funders[0]["award_title"] == "Award Title"
    assert funders[0]["award_uri"] == "Award URI"
    assert funders[0]["identifier"] == "Identifier"
    assert funders[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert funders[0]["identifier_type"] == "Identifier Type"
    assert funders[1]["name"] == "Admin Name"
    assert funders[1]["award_number"] == "award number"
    assert funders[1]["award_title"] == "Award Title"
    assert funders[1]["award_uri"] == "Award URI"
    assert funders[1]["identifier"] == "Identifier"
    assert funders[1]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert funders[1]["identifier_type"] == "Identifier Type"
    assert funders[2]["name"] == "Editor Name"
    assert funders[2]["award_number"] == "award number"
    assert funders[2]["award_title"] == "Award Title"
    assert funders[2]["award_uri"] == "Award URI"
    assert funders[2]["identifier"] == "Identifier"
    assert funders[2]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert funders[2]["identifier_type"] == "Identifier Type"

    assert admin_funders[0]["name"] == "Name"
    assert admin_funders[0]["award_number"] == "award number"
    assert admin_funders[0]["award_title"] == "Award Title"
    assert admin_funders[0]["award_uri"] == "Award URI"
    assert admin_funders[0]["identifier"] == "Identifier"
    assert admin_funders[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert admin_funders[0]["identifier_type"] == "Identifier Type"
    assert admin_funders[1]["name"] == "Admin Name"
    assert admin_funders[1]["award_number"] == "award number"
    assert admin_funders[1]["award_title"] == "Award Title"
    assert admin_funders[1]["award_uri"] == "Award URI"
    assert admin_funders[1]["identifier"] == "Identifier"
    assert admin_funders[1]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert admin_funders[1]["identifier_type"] == "Identifier Type"
    assert admin_funders[2]["name"] == "Editor Name"
    assert admin_funders[2]["award_number"] == "award number"
    assert admin_funders[2]["award_title"] == "Award Title"
    assert admin_funders[2]["award_uri"] == "Award URI"
    assert admin_funders[2]["identifier"] == "Identifier"
    assert admin_funders[2]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert admin_funders[2]["identifier_type"] == "Identifier Type"

    assert editor_funders[0]["name"] == "Name"
    assert editor_funders[0]["award_number"] == "award number"
    assert editor_funders[0]["award_title"] == "Award Title"
    assert editor_funders[0]["award_uri"] == "Award URI"
    assert editor_funders[0]["identifier"] == "Identifier"
    assert editor_funders[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert editor_funders[0]["identifier_type"] == "Identifier Type"
    assert editor_funders[1]["name"] == "Admin Name"
    assert editor_funders[1]["award_number"] == "award number"
    assert editor_funders[1]["award_title"] == "Award Title"
    assert editor_funders[1]["award_uri"] == "Award URI"
    assert editor_funders[1]["identifier"] == "Identifier"
    assert editor_funders[1]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert editor_funders[1]["identifier_type"] == "Identifier Type"
    assert editor_funders[2]["name"] == "Editor Name"
    assert editor_funders[2]["award_number"] == "award number"
    assert editor_funders[2]["award_title"] == "Award Title"
    assert editor_funders[2]["award_uri"] == "Award URI"
    assert editor_funders[2]["identifier"] == "Identifier"
    assert editor_funders[2]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert editor_funders[2]["identifier_type"] == "Identifier Type"

    assert viewer_funders[0]["name"] == "Name"
    assert viewer_funders[0]["award_number"] == "award number"
    assert viewer_funders[0]["award_title"] == "Award Title"
    assert viewer_funders[0]["award_uri"] == "Award URI"
    assert viewer_funders[0]["identifier"] == "Identifier"
    assert viewer_funders[0]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert viewer_funders[0]["identifier_type"] == "Identifier Type"
    assert viewer_funders[1]["name"] == "Admin Name"
    assert viewer_funders[1]["award_number"] == "award number"
    assert viewer_funders[1]["award_title"] == "Award Title"
    assert viewer_funders[1]["award_uri"] == "Award URI"
    assert viewer_funders[1]["identifier"] == "Identifier"
    assert viewer_funders[1]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert viewer_funders[1]["identifier_type"] == "Identifier Type"
    assert viewer_funders[2]["name"] == "Editor Name"
    assert viewer_funders[2]["award_number"] == "award number"
    assert viewer_funders[2]["award_title"] == "Award Title"
    assert viewer_funders[2]["award_uri"] == "Award URI"
    assert viewer_funders[2]["identifier"] == "Identifier"
    assert viewer_funders[2]["identifier_scheme_uri"] == "Identifier Scheme URI"
    assert viewer_funders[2]["identifier_type"] == "Identifier Type"

    assert len(creators) == 3
    assert len(admin_creators) == 3
    assert len(editor_creators) == 3
    assert len(viewer_creators) == 3

    assert creators[0]["id"] == pytest.global_dataset_creator_id
    assert creators[0]["given_name"] == "Given Name here"
    assert creators[0]["family_name"] == "Family Name here"
    assert creators[0]["name_type"] == "Personal"
    assert creators[0]["name_identifier"] == "Name identifier"
    assert creators[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert creators[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert creators[0]["creator"] is True
    assert creators[0]["affiliations"][0]["name"] == "Test"
    assert creators[0]["affiliations"][0]["identifier"] == "yes"
    assert creators[0]["affiliations"][0]["scheme"] == "uh"
    assert creators[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert creators[1]["id"] == pytest.global_dataset_creator_id_admin
    assert creators[1]["given_name"] == "Admin Given Name here"
    assert creators[1]["family_name"] == "Family Name here"
    assert creators[1]["name_type"] == "Personal"
    assert creators[1]["name_identifier"] == "Name identifier"
    assert creators[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert creators[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert creators[1]["creator"] is True
    assert creators[1]["affiliations"][0]["name"] == "Test"
    assert creators[1]["affiliations"][0]["identifier"] == "yes"
    assert creators[1]["affiliations"][0]["scheme"] == "uh"
    assert creators[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert creators[2]["id"] == pytest.global_dataset_creator_id_editor
    assert creators[2]["given_name"] == "Editor Given Name here"
    assert creators[2]["family_name"] == "Family Name here"
    assert creators[2]["name_type"] == "Personal"
    assert creators[2]["name_identifier"] == "Name identifier"
    assert creators[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert creators[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert creators[2]["creator"] is True
    assert creators[2]["affiliations"][0]["name"] == "Test"
    assert creators[2]["affiliations"][0]["identifier"] == "yes"
    assert creators[2]["affiliations"][0]["scheme"] == "uh"
    assert creators[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert admin_creators[0]["given_name"] == "Given Name here"
    assert admin_creators[0]["family_name"] == "Family Name here"
    assert admin_creators[0]["name_type"] == "Personal"
    assert admin_creators[0]["name_identifier"] == "Name identifier"
    assert admin_creators[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_creators[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_creators[0]["creator"] is True
    assert admin_creators[0]["affiliations"][0]["name"] == "Test"
    assert admin_creators[0]["affiliations"][0]["identifier"] == "yes"
    assert admin_creators[0]["affiliations"][0]["scheme"] == "uh"
    assert admin_creators[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert admin_creators[1]["given_name"] == "Admin Given Name here"
    assert admin_creators[1]["family_name"] == "Family Name here"
    assert admin_creators[1]["name_type"] == "Personal"
    assert admin_creators[1]["name_identifier"] == "Name identifier"
    assert admin_creators[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_creators[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_creators[1]["creator"] is True
    assert admin_creators[1]["affiliations"][0]["name"] == "Test"
    assert admin_creators[1]["affiliations"][0]["identifier"] == "yes"
    assert admin_creators[1]["affiliations"][0]["scheme"] == "uh"
    assert admin_creators[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert admin_creators[2]["given_name"] == "Editor Given Name here"
    assert admin_creators[2]["family_name"] == "Family Name here"
    assert admin_creators[2]["name_type"] == "Personal"
    assert admin_creators[2]["name_identifier"] == "Name identifier"
    assert admin_creators[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_creators[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_creators[2]["creator"] is True
    assert admin_creators[2]["affiliations"][0]["name"] == "Test"
    assert admin_creators[2]["affiliations"][0]["identifier"] == "yes"
    assert admin_creators[2]["affiliations"][0]["scheme"] == "uh"
    assert admin_creators[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert editor_creators[0]["given_name"] == "Given Name here"
    assert editor_creators[0]["family_name"] == "Family Name here"
    assert editor_creators[0]["name_type"] == "Personal"
    assert editor_creators[0]["name_identifier"] == "Name identifier"
    assert editor_creators[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_creators[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_creators[0]["creator"] is True
    assert editor_creators[0]["affiliations"][0]["name"] == "Test"
    assert editor_creators[0]["affiliations"][0]["identifier"] == "yes"
    assert editor_creators[0]["affiliations"][0]["scheme"] == "uh"
    assert editor_creators[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert editor_creators[1]["given_name"] == "Admin Given Name here"
    assert editor_creators[1]["family_name"] == "Family Name here"
    assert editor_creators[1]["name_type"] == "Personal"
    assert editor_creators[1]["name_identifier"] == "Name identifier"
    assert editor_creators[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_creators[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_creators[1]["creator"] is True
    assert editor_creators[1]["affiliations"][0]["name"] == "Test"
    assert editor_creators[1]["affiliations"][0]["identifier"] == "yes"
    assert editor_creators[1]["affiliations"][0]["scheme"] == "uh"
    assert editor_creators[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert editor_creators[2]["given_name"] == "Editor Given Name here"
    assert editor_creators[2]["family_name"] == "Family Name here"
    assert editor_creators[2]["name_type"] == "Personal"
    assert editor_creators[2]["name_identifier"] == "Name identifier"
    assert editor_creators[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_creators[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_creators[2]["creator"] is True
    assert editor_creators[2]["affiliations"][0]["name"] == "Test"
    assert editor_creators[2]["affiliations"][0]["identifier"] == "yes"
    assert editor_creators[2]["affiliations"][0]["scheme"] == "uh"
    assert editor_creators[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert viewer_creators[0]["given_name"] == "Given Name here"
    assert viewer_creators[0]["family_name"] == "Family Name here"
    assert viewer_creators[0]["name_type"] == "Personal"
    assert viewer_creators[0]["name_identifier"] == "Name identifier"
    assert viewer_creators[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert viewer_creators[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert viewer_creators[0]["creator"] is True
    assert viewer_creators[0]["affiliations"][0]["name"] == "Test"
    assert viewer_creators[0]["affiliations"][0]["identifier"] == "yes"
    assert viewer_creators[0]["affiliations"][0]["scheme"] == "uh"
    assert viewer_creators[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert viewer_creators[1]["given_name"] == "Admin Given Name here"
    assert viewer_creators[1]["family_name"] == "Family Name here"
    assert viewer_creators[1]["name_type"] == "Personal"
    assert viewer_creators[1]["name_identifier"] == "Name identifier"
    assert viewer_creators[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert viewer_creators[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert viewer_creators[1]["creator"] is True
    assert viewer_creators[1]["affiliations"][0]["name"] == "Test"
    assert viewer_creators[1]["affiliations"][0]["identifier"] == "yes"
    assert viewer_creators[1]["affiliations"][0]["scheme"] == "uh"
    assert viewer_creators[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert viewer_creators[2]["given_name"] == "Editor Given Name here"
    assert viewer_creators[2]["family_name"] == "Family Name here"
    assert viewer_creators[2]["name_type"] == "Personal"
    assert viewer_creators[2]["name_identifier"] == "Name identifier"
    assert viewer_creators[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert viewer_creators[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert viewer_creators[2]["creator"] is True
    assert viewer_creators[2]["affiliations"][0]["name"] == "Test"
    assert viewer_creators[2]["affiliations"][0]["identifier"] == "yes"
    assert viewer_creators[2]["affiliations"][0]["scheme"] == "uh"
    assert viewer_creators[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert contributors[0]["given_name"] == "Given Name here"
    assert contributors[0]["family_name"] == "Family Name here"
    assert contributors[0]["name_type"] == "Personal"
    assert contributors[0]["name_identifier"] == "Name identifier"
    assert contributors[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert contributors[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert contributors[0]["creator"] is False
    assert contributors[0]["contributor_type"] == "Con Type"
    assert contributors[0]["affiliations"][0]["name"] == "Test"
    assert contributors[0]["affiliations"][0]["identifier"] == "yes"
    assert contributors[0]["affiliations"][0]["scheme"] == "uh"
    assert contributors[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert contributors[1]["given_name"] == "Admin Given Name here"
    assert contributors[1]["family_name"] == "Family Name here"
    assert contributors[1]["name_type"] == "Personal"
    assert contributors[1]["name_identifier"] == "Name identifier"
    assert contributors[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert contributors[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert contributors[1]["creator"] is False
    assert contributors[1]["contributor_type"] == "Con Type"
    assert contributors[1]["affiliations"][0]["name"] == "Test"
    assert contributors[1]["affiliations"][0]["identifier"] == "yes"
    assert contributors[1]["affiliations"][0]["scheme"] == "uh"
    assert contributors[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert contributors[2]["given_name"] == "Editor Given Name here"
    assert contributors[2]["family_name"] == "Editor Family Name here"
    assert contributors[2]["name_type"] == "Personal"
    assert contributors[2]["name_identifier"] == "Name identifier"
    assert contributors[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert contributors[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert contributors[2]["creator"] is False
    assert contributors[2]["contributor_type"] == "Con Type"
    assert contributors[2]["affiliations"][0]["name"] == "Test"
    assert contributors[2]["affiliations"][0]["identifier"] == "yes"
    assert contributors[2]["affiliations"][0]["scheme"] == "uh"
    assert contributors[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert admin_contributors[0]["given_name"] == "Given Name here"
    assert admin_contributors[0]["family_name"] == "Family Name here"
    assert admin_contributors[0]["name_type"] == "Personal"
    assert admin_contributors[0]["name_identifier"] == "Name identifier"
    assert admin_contributors[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_contributors[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_contributors[0]["creator"] is False
    assert admin_contributors[0]["contributor_type"] == "Con Type"
    assert admin_contributors[0]["affiliations"][0]["name"] == "Test"
    assert admin_contributors[0]["affiliations"][0]["identifier"] == "yes"
    assert admin_contributors[0]["affiliations"][0]["scheme"] == "uh"
    assert admin_contributors[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert admin_contributors[1]["given_name"] == "Admin Given Name here"
    assert admin_contributors[1]["family_name"] == "Family Name here"
    assert admin_contributors[1]["name_type"] == "Personal"
    assert admin_contributors[1]["name_identifier"] == "Name identifier"
    assert admin_contributors[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_contributors[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_contributors[1]["creator"] is False
    assert admin_contributors[1]["contributor_type"] == "Con Type"
    assert admin_contributors[1]["affiliations"][0]["name"] == "Test"
    assert admin_contributors[1]["affiliations"][0]["identifier"] == "yes"
    assert admin_contributors[1]["affiliations"][0]["scheme"] == "uh"
    assert admin_contributors[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert admin_contributors[2]["given_name"] == "Editor Given Name here"
    assert admin_contributors[2]["family_name"] == "Editor Family Name here"
    assert admin_contributors[2]["name_type"] == "Personal"
    assert admin_contributors[2]["name_identifier"] == "Name identifier"
    assert admin_contributors[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert admin_contributors[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert admin_contributors[2]["creator"] is False
    assert admin_contributors[2]["contributor_type"] == "Con Type"
    assert admin_contributors[2]["affiliations"][0]["name"] == "Test"
    assert admin_contributors[2]["affiliations"][0]["identifier"] == "yes"
    assert admin_contributors[2]["affiliations"][0]["scheme"] == "uh"
    assert admin_contributors[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert editor_contributors[0]["given_name"] == "Given Name here"
    assert editor_contributors[0]["family_name"] == "Family Name here"
    assert editor_contributors[0]["name_type"] == "Personal"
    assert editor_contributors[0]["name_identifier"] == "Name identifier"
    assert editor_contributors[0]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_contributors[0]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_contributors[0]["creator"] is False
    assert editor_contributors[0]["contributor_type"] == "Con Type"
    assert editor_contributors[0]["affiliations"][0]["name"] == "Test"
    assert editor_contributors[0]["affiliations"][0]["identifier"] == "yes"
    assert editor_contributors[0]["affiliations"][0]["scheme"] == "uh"
    assert editor_contributors[0]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert editor_contributors[1]["given_name"] == "Admin Given Name here"
    assert editor_contributors[1]["family_name"] == "Family Name here"
    assert editor_contributors[1]["name_type"] == "Personal"
    assert editor_contributors[1]["name_identifier"] == "Name identifier"
    assert editor_contributors[1]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_contributors[1]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_contributors[1]["creator"] is False
    assert editor_contributors[1]["contributor_type"] == "Con Type"
    assert editor_contributors[1]["affiliations"][0]["name"] == "Test"
    assert editor_contributors[1]["affiliations"][0]["identifier"] == "yes"
    assert editor_contributors[1]["affiliations"][0]["scheme"] == "uh"
    assert editor_contributors[1]["affiliations"][0]["scheme_uri"] == "scheme uri"
    assert editor_contributors[2]["given_name"] == "Editor Given Name here"
    assert editor_contributors[2]["family_name"] == "Editor Family Name here"
    assert editor_contributors[2]["name_type"] == "Personal"
    assert editor_contributors[2]["name_identifier"] == "Name identifier"
    assert editor_contributors[2]["name_identifier_scheme"] == "Name Scheme ID"
    assert editor_contributors[2]["name_identifier_scheme_uri"] == "Name ID Scheme URI"
    assert editor_contributors[2]["creator"] is False
    assert editor_contributors[2]["contributor_type"] == "Con Type"
    assert editor_contributors[2]["affiliations"][0]["name"] == "Test"
    assert editor_contributors[2]["affiliations"][0]["identifier"] == "yes"
    assert editor_contributors[2]["affiliations"][0]["scheme"] == "uh"
    assert editor_contributors[2]["affiliations"][0]["scheme_uri"] == "scheme uri"

    assert managing_organization["name"] == "editor Managing Organization Name"
    assert managing_organization["identifier"] == "identifier"
    assert managing_organization["identifier_scheme"] == "identifier scheme"
    assert managing_organization["identifier_scheme_uri"] == "identifier scheme_uri"

    assert admin_managing_organization["name"] == "editor Managing Organization Name"
    assert admin_managing_organization["identifier"] == "identifier"
    assert admin_managing_organization["identifier_scheme"] == "identifier scheme"
    assert admin_managing_organization["identifier_scheme_uri"] == "identifier scheme_uri"

    assert editor_managing_organization["name"] == "editor Managing Organization Name"
    assert editor_managing_organization["identifier"] == "identifier"
    assert editor_managing_organization["identifier_scheme"] == "identifier scheme"
    assert editor_managing_organization["identifier_scheme_uri"] == "identifier scheme_uri"

    assert viewer_managing_organization["name"] == "editor Managing Organization Name"
    assert viewer_managing_organization["identifier"] == "identifier"
    assert viewer_managing_organization["identifier_scheme"] == "identifier scheme"
    assert viewer_managing_organization["identifier_scheme_uri"] == "identifier scheme_uri"


# ------------------- DELETE CONTRIBUTOR METADATA ------------------- #
def test_delete_dataset_contributor_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/contributor'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset contributor metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    contributor_id = pytest.global_dataset_contributor_id
    admin_contributor_id = pytest.global_dataset_contributor_id_admin
    editor_contributor_id = pytest.global_dataset_contributor_id_editor

    # Verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor/{contributor_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor/{contributor_id}"
    )
    # pylint: disable=line-too-long
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor/{admin_contributor_id}"
    )
    # pylint: disable=line-too-long
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/contributor/{editor_contributor_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DELETE CREATOR METADATA ------------------- #
def test_delete_dataset_creator_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/creator'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset creator metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    creator_id = pytest.global_dataset_creator_id
    admin_creator_id = pytest.global_dataset_creator_id_admin
    editor_creator_id = pytest.global_dataset_creator_id_editor

    # Verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{creator_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{creator_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{admin_creator_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/creator/{editor_creator_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DELETE DATASET FUNDER METADATA ------------------- #
def test_delete_dataset_funder_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/funder'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset
    funder metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    funder_id = pytest.global_dataset_funder_id
    a_funder_id = pytest.global_dataset_funder_id_admin
    e_funder_id = pytest.global_dataset_funder_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{funder_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{funder_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{a_funder_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/funder/{e_funder_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- OTHER METADATA ------------------- #
def test_put_other_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    other metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other",
        json={
            "acknowledgement": "Yes",
            "language": "English",
            "resource_type": "Resource Type",
            "size": ["Size"],
            "format": ["Format"],
            "standards_followed": "Standards Followed",
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert response_data["acknowledgement"] == "Yes"
    assert response_data["language"] == "English"

    assert response_data["size"] == ["Size"]
    assert response_data["format"] == ["Format"]
    assert response_data["standards_followed"] == "Standards Followed"

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other",
        json={
            "acknowledgement": "Yes",
            "language": "English",
            "resource_type": "Resource Type",
            "size": ["Size"],
            "format": ["Format"],
            "standards_followed": "Standards Followed",
        },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    assert admin_response_data["acknowledgement"] == "Yes"
    assert admin_response_data["language"] == "English"
    assert admin_response_data["size"] == ["Size"]
    assert admin_response_data["format"] == ["Format"]
    assert admin_response_data["standards_followed"] == "Standards Followed"

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other",
        json={
            "acknowledgement": "Yes",
            "language": "English",
            "resource_type": "Resource Type",
            "size": ["Size"],
            "format": ["Format"],
            "standards_followed": "Standards Followed",
        },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    assert editor_response_data["acknowledgement"] == "Yes"
    assert editor_response_data["language"] == "English"
    assert editor_response_data["size"] == ["Size"]
    assert editor_response_data["format"] == ["Format"]
    assert editor_response_data["standards_followed"] == "Standards Followed"

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other",
        json={
            "acknowledgement": "Yes",
            "language": "English",
            "resource_type": "Resource Type",
            "size": ["Size"],
            "format": ["Format"],
            "standards_followed": "Standards Followed",
        },
    )
    assert viewer_response.status_code == 403


def test_get_other_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    other metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/other"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    # assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # Editor was the last to update the metadata successfully so
    # the response should reflect that
    assert response_data["acknowledgement"] == "Yes"
    assert response_data["language"] == "English"
    # assert response_data["resource_type"] == "Editor Resource Type"
    assert response_data["size"] == ["Size"]
    assert response_data["format"] == ["Format"]
    assert response_data["standards_followed"] == "Standards Followed"

    assert admin_response_data["acknowledgement"] == "Yes"
    assert admin_response_data["language"] == "English"
    # assert admin_response_data["resource_type"] == "Editor Resource Type"
    assert admin_response_data["size"] == ["Size"]
    assert admin_response_data["format"] == ["Format"]
    assert admin_response_data["standards_followed"] == "Standards Followed"

    assert editor_response_data["acknowledgement"] == "Yes"
    assert editor_response_data["language"] == "English"
    # assert editor_response_data["resource_type"] == "Editor Resource Type"
    assert editor_response_data["size"] == ["Size"]
    assert editor_response_data["format"] == ["Format"]
    assert editor_response_data["standards_followed"] == "Standards Followed"

    assert viewer_response_data["acknowledgement"] == "Yes"
    assert viewer_response_data["language"] == "English"
    assert viewer_response_data["size"] == ["Size"]
    assert viewer_response_data["format"] == ["Format"]
    assert viewer_response_data["standards_followed"] == "Standards Followed"


# ------------------- RELATED IDENTIFIER METADATA ------------------- #
def test_post_dataset_related_identifier_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset
    related identifier metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier",
        json=[
            {
                "identifier": "test identifier",
                "identifier_type": "test identifier type",
                "relation_type": "test relation type",
                "related_metadata_scheme": "test",
                "scheme_uri": "test",
                "scheme_type": "test",
                "resource_type": "test",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)

    pytest.global_dataset_related_identifier_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "test identifier"
    assert response_data[0]["identifier_type"] == "test identifier type"
    assert response_data[0]["relation_type"] == "test relation type"
    assert response_data[0]["related_metadata_scheme"] == "test"
    assert response_data[0]["scheme_uri"] == "test"
    assert response_data[0]["scheme_type"] == "test"
    assert response_data[0]["resource_type"] == "test"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier",
        json=[
            {
                "identifier": "admin test identifier",
                "identifier_type": "test identifier type",
                "relation_type": "test relation type",
                "related_metadata_scheme": "test",
                "scheme_uri": "test",
                "scheme_type": "test",
                "resource_type": "test",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert admin_response.status_code == 201
    admin_response_data = json.loads(admin_response.data)
    pytest.global_dataset_related_identifier_id_admin = admin_response_data[0]["id"]

    assert admin_response_data[0]["identifier"] == "admin test identifier"
    assert admin_response_data[0]["identifier_type"] == "test identifier type"
    assert admin_response_data[0]["relation_type"] == "test relation type"
    assert admin_response_data[0]["related_metadata_scheme"] == "test"
    assert admin_response_data[0]["scheme_uri"] == "test"
    assert admin_response_data[0]["scheme_type"] == "test"
    assert admin_response_data[0]["resource_type"] == "test"
    editor_response = _editor_client.post(
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

    assert editor_response.status_code == 201
    editor_response_data = json.loads(editor_response.data)
    pytest.global_dataset_related_identifier_id_editor = editor_response_data[0]["id"]

    assert editor_response_data[0]["identifier"] == "editor test identifier"
    assert editor_response_data[0]["identifier_type"] == "test identifier type"
    assert editor_response_data[0]["relation_type"] == "test relation type"
    assert editor_response_data[0]["related_metadata_scheme"] == "test"
    assert editor_response_data[0]["scheme_uri"] == "test"
    assert editor_response_data[0]["scheme_type"] == "test"
    assert editor_response_data[0]["resource_type"] == "test"
    viewer_client = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier",
        json=[
            {
                "identifier": "viewer test identifier",
                "identifier_type": "test identifier type",
                "relation_type": "test relation type",
                "related_metadata_scheme": "test",
                "scheme_uri": "test",
                "scheme_type": "test",
                "resource_type": "test",
            }
        ],
    )

    assert viewer_client.status_code == 403


def test_get_dataset_related_identifier_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    related identifier metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    # seach for main title and subtitle index in response_data[n]["titles"]
    # pylint: disable=line-too-long

    # assert len(response_data) == 3
    # assert len(admin_response_data) == 3
    # assert len(editor_response_data) == 3
    # assert len(viewer_response_data) == 3
    assert response_data[0]["identifier"] == "test identifier"
    assert response_data[0]["identifier_type"] == "test identifier type"
    assert response_data[0]["relation_type"] == "test relation type"
    assert response_data[0]["related_metadata_scheme"] == "test"
    assert response_data[0]["scheme_uri"] == "test"
    assert response_data[0]["scheme_type"] == "test"
    assert response_data[0]["resource_type"] == "test"
    assert response_data[1]["identifier"] == "admin test identifier"
    assert response_data[1]["identifier_type"] == "test identifier type"
    assert response_data[1]["relation_type"] == "test relation type"
    assert response_data[1]["related_metadata_scheme"] == "test"
    assert response_data[1]["scheme_uri"] == "test"
    assert response_data[1]["scheme_type"] == "test"
    assert response_data[1]["resource_type"] == "test"
    assert response_data[2]["identifier"] == "editor test identifier"
    assert response_data[2]["identifier_type"] == "test identifier type"
    assert response_data[2]["relation_type"] == "test relation type"
    assert response_data[2]["related_metadata_scheme"] == "test"
    assert response_data[2]["scheme_uri"] == "test"
    assert response_data[2]["scheme_type"] == "test"
    assert response_data[2]["resource_type"] == "test"

    assert admin_response_data[0]["identifier"] == "test identifier"
    assert admin_response_data[0]["identifier_type"] == "test identifier type"
    assert admin_response_data[0]["relation_type"] == "test relation type"
    assert admin_response_data[0]["related_metadata_scheme"] == "test"
    assert admin_response_data[0]["scheme_uri"] == "test"
    assert admin_response_data[0]["scheme_type"] == "test"
    assert admin_response_data[0]["resource_type"] == "test"
    assert admin_response_data[1]["identifier"] == "admin test identifier"
    assert admin_response_data[1]["identifier_type"] == "test identifier type"
    assert admin_response_data[1]["relation_type"] == "test relation type"
    assert admin_response_data[1]["related_metadata_scheme"] == "test"
    assert admin_response_data[1]["scheme_uri"] == "test"
    assert admin_response_data[1]["scheme_type"] == "test"
    assert admin_response_data[1]["resource_type"] == "test"
    assert admin_response_data[2]["identifier"] == "editor test identifier"
    assert admin_response_data[2]["identifier_type"] == "test identifier type"
    assert admin_response_data[2]["relation_type"] == "test relation type"
    assert admin_response_data[2]["related_metadata_scheme"] == "test"
    assert admin_response_data[2]["scheme_uri"] == "test"
    assert admin_response_data[2]["scheme_type"] == "test"
    assert admin_response_data[2]["resource_type"] == "test"

    assert editor_response_data[0]["identifier"] == "test identifier"
    assert editor_response_data[0]["identifier_type"] == "test identifier type"
    assert editor_response_data[0]["relation_type"] == "test relation type"
    assert editor_response_data[0]["related_metadata_scheme"] == "test"
    assert editor_response_data[0]["scheme_uri"] == "test"
    assert editor_response_data[0]["scheme_type"] == "test"
    assert editor_response_data[0]["resource_type"] == "test"
    assert editor_response_data[1]["identifier"] == "admin test identifier"
    assert editor_response_data[1]["identifier_type"] == "test identifier type"
    assert editor_response_data[1]["relation_type"] == "test relation type"
    assert editor_response_data[1]["related_metadata_scheme"] == "test"
    assert editor_response_data[1]["scheme_uri"] == "test"
    assert editor_response_data[1]["scheme_type"] == "test"
    assert editor_response_data[1]["resource_type"] == "test"
    assert editor_response_data[2]["identifier"] == "editor test identifier"
    assert editor_response_data[2]["identifier_type"] == "test identifier type"
    assert editor_response_data[2]["relation_type"] == "test relation type"
    assert editor_response_data[2]["related_metadata_scheme"] == "test"
    assert editor_response_data[2]["scheme_uri"] == "test"
    assert editor_response_data[2]["scheme_type"] == "test"
    assert editor_response_data[2]["resource_type"] == "test"

    assert viewer_response_data[0]["identifier"] == "test identifier"
    assert viewer_response_data[0]["identifier_type"] == "test identifier type"
    assert viewer_response_data[0]["relation_type"] == "test relation type"
    assert viewer_response_data[0]["related_metadata_scheme"] == "test"
    assert viewer_response_data[0]["scheme_uri"] == "test"
    assert viewer_response_data[0]["scheme_type"] == "test"
    assert viewer_response_data[0]["resource_type"] == "test"
    assert viewer_response_data[1]["identifier"] == "admin test identifier"
    assert viewer_response_data[1]["identifier_type"] == "test identifier type"
    assert viewer_response_data[1]["relation_type"] == "test relation type"
    assert viewer_response_data[1]["related_metadata_scheme"] == "test"
    assert viewer_response_data[1]["scheme_uri"] == "test"
    assert viewer_response_data[1]["scheme_type"] == "test"
    assert viewer_response_data[1]["resource_type"] == "test"
    assert viewer_response_data[2]["identifier"] == "editor test identifier"
    assert viewer_response_data[2]["identifier_type"] == "test identifier type"
    assert viewer_response_data[2]["relation_type"] == "test relation type"
    assert viewer_response_data[2]["related_metadata_scheme"] == "test"
    assert viewer_response_data[2]["scheme_uri"] == "test"
    assert viewer_response_data[2]["scheme_type"] == "test"
    assert viewer_response_data[2]["resource_type"] == "test"


def test_delete_dataset_related_identifier_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (DELETE)
    Then check that the response is valid and retrieves the dataset
    related identifier metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    identifier_id = pytest.global_dataset_related_identifier_id
    a_identifier_id = pytest.global_dataset_related_identifier_id_admin
    e_identifier_id = pytest.global_dataset_related_identifier_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier/{identifier_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier/{identifier_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier/{a_identifier_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/related-identifier/{e_identifier_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DATA MANAGEMENT METADATA ------------------- #
def test_post_dataset_data_management_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/data-management' endpoint is requested (PUT)
    Then check that the response is valid and updates the data management metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/data-management",
        json={
            "consent":
                {
                    "type": "test",
                     "noncommercial": True,
                     "geog_restrict": True,
                     "research_type": True,
                     "genetic_only": True,
                     "no_methods": True,
                     "details": "test",
                 },
            "deident": {
                "type": "Level",
                "direct": True,
                "hipaa": True,
                "dates": True,
                "nonarr": True,
                "k_anon": True,
                "details": "Details",
            },
            "subjects":
                [{
                    "classification_code": "Classification Code",
                    "scheme": "Scheme",
                    "scheme_uri": "Scheme URI",
                    "subject": "Subject",
                    "value_uri": "Value URI",
                }]
        },
    )

    assert response.status_code == 200
    response_data = json.loads(response.data)
    consent = response_data["consent"]
    deident = response_data["deident"]
    subjects = response_data["subjects"]
    pytest.global_dataset_subject_id = subjects[0]["id"]

    assert subjects[0]["scheme"] == "Scheme"
    assert subjects[0]["scheme_uri"] == "Scheme URI"
    assert subjects[0]["subject"] == "Subject"
    assert subjects[0]["value_uri"] == "Value URI"
    assert subjects[0]["classification_code"] == "Classification Code"

    assert consent["type"] == "test"
    assert consent["noncommercial"] is True
    assert consent["geog_restrict"] is True
    assert consent["research_type"] is True
    assert consent["genetic_only"] is True
    assert consent["no_methods"] is True
    assert consent["details"] == "test"

    assert deident["type"] == "Level"
    assert deident["direct"] is True
    assert deident["hipaa"] is True
    assert deident["dates"] is True
    assert deident["nonarr"] is True
    assert deident["k_anon"] is True
    assert deident["details"] == "Details"


    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/data-management",
        json={
            "consent":
                {
                    "type": "admin test",
                     "noncommercial": True,
                     "geog_restrict": True,
                     "research_type": True,
                     "genetic_only": True,
                     "no_methods": True,
                     "details": "admin details test",
                 },
            "deident": {
                    "type": "Level",
                    "direct": True,
                    "hipaa": True,
                    "dates": True,
                    "nonarr": True,
                    "k_anon": True,
                    "details": "Details",
                },
            "subjects": [
                    {
                        "classification_code": "Classification Code",
                        "scheme": "Admin Scheme",
                        "scheme_uri": "Scheme URI",
                        "subject": "Subject",
                        "value_uri": "Admin Value URI",
                    }
                ],
    },
    )

    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)

    admin_consent = admin_response_data["consent"]
    admin_deident = admin_response_data["deident"]
    admin_subjects = admin_response_data["subjects"]

    pytest.global_dataset_subject_id_admin = admin_subjects[0]["id"]

    assert admin_subjects[0]["scheme"] == "Admin Scheme"
    assert admin_subjects[0]["scheme_uri"] == "Scheme URI"
    assert admin_subjects[0]["subject"] == "Subject"
    assert admin_subjects[0]["value_uri"] == "Admin Value URI"
    assert admin_subjects[0]["classification_code"] == "Classification Code"

    assert admin_consent["type"] == "admin test"
    assert admin_consent["details"] == "admin details test"
    assert admin_consent["noncommercial"] is True
    assert admin_consent["geog_restrict"] is True
    assert admin_consent["research_type"] is True
    assert admin_consent["genetic_only"] is True
    assert admin_consent["no_methods"] is True

    assert admin_deident["type"] == "Level"
    assert admin_deident["direct"] is True
    assert admin_deident["hipaa"] is True
    assert admin_deident["dates"] is True
    assert admin_deident["nonarr"] is True
    assert admin_deident["k_anon"] is True
    assert admin_deident["details"] == "Details"

    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/data-management",
        json = {
                "consent":
                    {
                        "type": "editor test",
                        "noncommercial": True,
                        "geog_restrict": True,
                        "research_type": True,
                        "genetic_only": True,
                        "no_methods": True,
                        "details": "editor details test",
                    },
                "deident": {
                    "type": "Level",
                    "direct": True,
                    "hipaa": True,
                    "dates": True,
                    "nonarr": True,
                    "k_anon": True,
                    "details": "Details",
                },
                "subjects": [
                        {
                            "classification_code": "Classification Code",
                            "scheme": "Editor Scheme",
                            "scheme_uri": "Scheme URI",
                            "subject": "Subject",
                            "value_uri": "Editor Value URI",
                        }
                    ],
    },
    )

    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)

    editor_consent = editor_response_data["consent"]
    editor_deident = editor_response_data["deident"]
    editor_subjects = editor_response_data["subjects"]
    pytest.global_dataset_subject_id_editor = editor_subjects[0]["id"]

    assert editor_subjects[0]["scheme"] == "Editor Scheme"
    assert editor_subjects[0]["scheme_uri"] == "Scheme URI"
    assert editor_subjects[0]["subject"] == "Subject"
    assert editor_subjects[0]["value_uri"] == "Editor Value URI"
    assert editor_subjects[0]["classification_code"] == "Classification Code"

    assert editor_consent["type"] == "editor test"
    assert editor_consent["details"] == "editor details test"
    assert editor_consent["noncommercial"] is True
    assert editor_consent["geog_restrict"] is True
    assert editor_consent["research_type"] is True
    assert editor_consent["genetic_only"] is True
    assert editor_consent["no_methods"] is True

    assert editor_deident["type"] == "Level"
    assert editor_deident["direct"] is True
    assert editor_deident["hipaa"] is True
    assert editor_deident["dates"] is True
    assert editor_deident["nonarr"] is True
    assert editor_deident["k_anon"] is True
    assert editor_deident["details"] == "Details"

    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/data-management",
        json= {
                "consent":
                    {
                        "type": "viewer test",
                        "noncommercial": True,
                        "geog_restrict": True,
                        "research_type": True,
                        "genetic_only": True,
                        "no_methods": True,
                        "details": "viewer details test",
                    },
                "deident": {
                    "type": "Level",
                    "direct": True,
                    "hipaa": True,
                    "dates": True,
                    "nonarr": True,
                    "k_anon": True,
                    "details": "Details",
                },
                "subjects": [
                        {
                            "classification_code": "Classification Code",
                            "scheme": "Viewer Scheme",
                            "scheme_uri": "Scheme URI",
                            "subject": "Subject",
                            "value_uri": "Viewer Value URI",
                        }
                    ],
    },
    )

    assert viewer_response.status_code == 403


def test_get_dataset_data_management_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/data-management' endpoint is requested (GET)
    Then check that the response is valid and retrieves the data management metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/data-management"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/data-management"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/data-management"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/data-management"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    consent = response_data["consent"]
    deident = response_data["deident"]
    subjects = response_data["subjects"]

    admin_consent = admin_response_data["consent"]
    admin_deident = admin_response_data["deident"]
    admin_subjects = admin_response_data["subjects"]

    editor_consent = editor_response_data["consent"]
    editor_deident = editor_response_data["deident"]
    editor_subjects = editor_response_data["subjects"]

    viewer_consent = viewer_response_data["consent"]
    viewer_deident = viewer_response_data["deident"]
    viewer_subjects = viewer_response_data["subjects"]

    assert consent["type"] == "editor test"
    assert consent["noncommercial"] is True
    assert consent["geog_restrict"] is True
    assert consent["research_type"] is True
    assert consent["genetic_only"] is True
    assert consent["no_methods"] is True
    assert consent["details"] == "editor details test"
    assert admin_consent["type"] == "editor test"
    assert admin_consent["noncommercial"] is True
    assert admin_consent["geog_restrict"] is True
    assert admin_consent["research_type"] is True
    assert admin_consent["genetic_only"] is True
    assert admin_consent["no_methods"] is True
    assert admin_consent["details"] == "editor details test"
    assert editor_consent["type"] == "editor test"
    assert editor_consent["noncommercial"] is True
    assert editor_consent["geog_restrict"] is True
    assert editor_consent["research_type"] is True
    assert editor_consent["genetic_only"] is True
    assert editor_consent["no_methods"] is True
    assert editor_consent["details"] == "editor details test"
    assert viewer_consent["type"] == "editor test"
    assert viewer_consent["noncommercial"] is True
    assert viewer_consent["geog_restrict"] is True
    assert viewer_consent["research_type"] is True
    assert viewer_consent["genetic_only"] is True
    assert viewer_consent["no_methods"] is True
    assert viewer_consent["details"] == "editor details test"

    assert subjects[0]["scheme"] == "Scheme"
    assert subjects[0]["scheme_uri"] == "Scheme URI"
    assert subjects[0]["subject"] == "Subject"
    assert subjects[0]["value_uri"] == "Value URI"
    assert subjects[0]["classification_code"] == "Classification Code"
    assert subjects[1]["scheme"] == "Admin Scheme"
    assert subjects[1]["scheme_uri"] == "Scheme URI"
    assert subjects[1]["subject"] == "Subject"
    assert subjects[1]["value_uri"] == "Admin Value URI"
    assert subjects[1]["classification_code"] == "Classification Code"
    assert subjects[2]["scheme"] == "Editor Scheme"
    assert subjects[2]["scheme_uri"] == "Scheme URI"
    assert subjects[2]["subject"] == "Subject"
    assert subjects[2]["value_uri"] == "Editor Value URI"
    assert subjects[2]["classification_code"] == "Classification Code"

    assert admin_subjects[0]["scheme"] == "Scheme"
    assert admin_subjects[0]["scheme_uri"] == "Scheme URI"
    assert admin_subjects[0]["subject"] == "Subject"
    assert admin_subjects[0]["value_uri"] == "Value URI"
    assert admin_subjects[0]["classification_code"] == "Classification Code"
    assert admin_subjects[1]["scheme"] == "Admin Scheme"
    assert admin_subjects[1]["scheme_uri"] == "Scheme URI"
    assert admin_subjects[1]["subject"] == "Subject"
    assert admin_subjects[1]["value_uri"] == "Admin Value URI"
    assert admin_subjects[1]["classification_code"] == "Classification Code"
    assert admin_subjects[2]["scheme"] == "Editor Scheme"
    assert admin_subjects[2]["scheme_uri"] == "Scheme URI"
    assert admin_subjects[2]["subject"] == "Subject"
    assert admin_subjects[2]["value_uri"] == "Editor Value URI"
    assert admin_subjects[2]["classification_code"] == "Classification Code"

    assert editor_subjects[0]["scheme"] == "Scheme"
    assert editor_subjects[0]["scheme_uri"] == "Scheme URI"
    assert editor_subjects[0]["subject"] == "Subject"
    assert editor_subjects[0]["value_uri"] == "Value URI"
    assert editor_subjects[0]["classification_code"] == "Classification Code"
    assert editor_subjects[1]["scheme"] == "Admin Scheme"
    assert editor_subjects[1]["scheme_uri"] == "Scheme URI"
    assert editor_subjects[1]["subject"] == "Subject"
    assert editor_subjects[1]["value_uri"] == "Admin Value URI"
    assert editor_subjects[1]["classification_code"] == "Classification Code"
    assert editor_subjects[2]["scheme"] == "Editor Scheme"
    assert editor_subjects[2]["scheme_uri"] == "Scheme URI"
    assert editor_subjects[2]["subject"] == "Subject"
    assert editor_subjects[2]["value_uri"] == "Editor Value URI"
    assert editor_subjects[2]["classification_code"] == "Classification Code"

    assert viewer_subjects[0]["scheme"] == "Scheme"
    assert viewer_subjects[0]["scheme_uri"] == "Scheme URI"
    assert viewer_subjects[0]["subject"] == "Subject"
    assert viewer_subjects[0]["value_uri"] == "Value URI"
    assert viewer_subjects[0]["classification_code"] == "Classification Code"
    assert viewer_subjects[1]["scheme"] == "Admin Scheme"
    assert viewer_subjects[1]["scheme_uri"] == "Scheme URI"
    assert viewer_subjects[1]["subject"] == "Subject"
    assert viewer_subjects[1]["value_uri"] == "Admin Value URI"
    assert viewer_subjects[1]["classification_code"] == "Classification Code"
    assert viewer_subjects[2]["scheme"] == "Editor Scheme"
    assert viewer_subjects[2]["scheme_uri"] == "Scheme URI"
    assert viewer_subjects[2]["subject"] == "Subject"
    assert viewer_subjects[2]["value_uri"] == "Editor Value URI"
    assert viewer_subjects[2]["classification_code"] == "Classification Code"

    assert deident["type"] == "Level"
    assert deident["direct"] is True
    assert deident["hipaa"] is True
    assert deident["dates"] is True
    assert deident["nonarr"] is True
    assert deident["k_anon"] is True
    assert deident["details"] == "Details"
    assert admin_deident["type"] == "Level"
    assert admin_deident["direct"] is True
    assert admin_deident["hipaa"] is True
    assert admin_deident["dates"] is True
    assert admin_deident["nonarr"] is True
    assert admin_deident["k_anon"] is True
    assert admin_deident["details"] == "Details"
    assert editor_deident["type"] == "Level"
    assert editor_deident["direct"] is True
    assert editor_deident["hipaa"] is True
    assert editor_deident["dates"] is True
    assert editor_deident["nonarr"] is True
    assert editor_deident["k_anon"] is True
    assert editor_deident["details"] == "Details"
    assert viewer_deident["type"] == "Level"
    assert viewer_deident["direct"] is True
    assert viewer_deident["hipaa"] is True
    assert viewer_deident["dates"] is True
    assert viewer_deident["nonarr"] is True
    assert viewer_deident["k_anon"] is True
    assert viewer_deident["details"] == "Details"


def test_delete_dataset_subject_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/subject'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    subjects metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    subject_id = pytest.global_dataset_subject_id
    admin_sub_id = pytest.global_dataset_subject_id_admin
    editor_sub_id = pytest.global_dataset_subject_id_editor

    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject/{subject_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject/{subject_id}"
    )
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject/{admin_sub_id}"
    )
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/subject/{editor_sub_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- ALTERNATIVE IDENTIFIER METADATA ------------------- #
def test_post_alternative_identifier(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier'
    endpoint is requested (POST)
    Then check that the response is valid and creates the dataset alternative identifier
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "identifier test",
                "type": "ARK",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)

    assert response.status_code == 201
    response_data = json.loads(response.data)
    pytest.global_alternative_identifier_id = response_data[0]["id"]

    assert response_data[0]["identifier"] == "identifier test"
    assert response_data[0]["type"] == "ARK"

    admin_response = _admin_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "admin test",
                "type": "ARK",
            }
        ],
    )
    # Add a one second delay to prevent duplicate timestamps
    sleep(1)
    editor_response = _editor_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "editor test",
                "type": "ARK",
            }
        ],
    )
    viewer_response = _viewer_client.post(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier",
        json=[
            {
                "identifier": "viewer test",
                "type": "ARK",
            }
        ],
    )

    assert admin_response.status_code == 201
    assert editor_response.status_code == 201
    assert viewer_response.status_code == 403

    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    pytest.global_alternative_identifier_id_admin = admin_response_data[0]["id"]
    pytest.global_alternative_identifier_id_editor = editor_response_data[0]["id"]

    assert admin_response_data[0]["identifier"] == "admin test"
    assert admin_response_data[0]["type"] == "ARK"
    assert editor_response_data[0]["identifier"] == "editor test"
    assert editor_response_data[0]["type"] == "ARK"


def test_get_alternative_identifier(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset alternative identifier content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )
    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )
    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )
    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier"
    )

    assert response.status_code == 200
    assert admin_response.status_code == 200
    assert editor_response.status_code == 200
    assert viewer_response.status_code == 200

    response_data = json.loads(response.data)
    admin_response_data = json.loads(admin_response.data)
    editor_response_data = json.loads(editor_response.data)
    viewer_response_data = json.loads(viewer_response.data)

    assert response_data[0]["identifier"] == "identifier test"
    assert response_data[0]["type"] == "ARK"
    assert response_data[1]["identifier"] == "admin test"
    assert response_data[1]["type"] == "ARK"
    assert response_data[2]["identifier"] == "editor test"
    assert response_data[2]["type"] == "ARK"

    assert admin_response_data[0]["identifier"] == "identifier test"
    assert admin_response_data[0]["type"] == "ARK"
    assert admin_response_data[1]["identifier"] == "admin test"
    assert admin_response_data[1]["type"] == "ARK"
    assert admin_response_data[2]["identifier"] == "editor test"
    assert admin_response_data[2]["type"] == "ARK"

    assert editor_response_data[0]["identifier"] == "identifier test"
    assert editor_response_data[0]["type"] == "ARK"
    assert editor_response_data[1]["identifier"] == "admin test"
    assert editor_response_data[1]["type"] == "ARK"
    assert editor_response_data[2]["identifier"] == "editor test"
    assert editor_response_data[2]["type"] == "ARK"

    assert viewer_response_data[0]["identifier"] == "identifier test"
    assert viewer_response_data[0]["type"] == "ARK"
    assert viewer_response_data[1]["identifier"] == "admin test"
    assert viewer_response_data[1]["type"] == "ARK"
    assert viewer_response_data[2]["identifier"] == "editor test"
    assert viewer_response_data[2]["type"] == "ARK"


def test_delete_alternative_identifier(clients):
    """
    Given a Flask application configured for testing and a study ID
    When the '/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier'
    endpoint is requested (DELETE)
    Then check that the response is valid and deletes the dataset alternative identifier content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id
    identifier_id = pytest.global_alternative_identifier_id
    admin_identifier_id = pytest.global_alternative_identifier_id_admin
    editor_identifier_id = pytest.global_alternative_identifier_id_editor

    # verify Viewer cannot delete
    viewer_response = _viewer_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{identifier_id}"
    )
    response = _logged_in_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{identifier_id}"
    )
    # pylint: disable=line-too-long
    admin_response = _admin_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{admin_identifier_id}"
    )
    # pylint: disable=line-too-long
    editor_response = _editor_client.delete(
        f"/study/{study_id}/dataset/{dataset_id}/metadata/alternative-identifier/{editor_identifier_id}"
    )

    assert viewer_response.status_code == 403
    assert response.status_code == 204
    assert admin_response.status_code == 204
    assert editor_response.status_code == 204


# ------------------- DATASET HEALTHSHEET MOTIVATION METADATA ------------------- #
def test_put_healthsheet_motivation_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation",
        json={"motivation": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["motivation"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation",
        json={"motivation": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation",
        json={"motivation": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation",
        json={"motivation": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_motivation_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["motivation"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/motivation"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["motivation"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# # ------------------- DATASET HEALTHSHEET COMPOSITION METADATA ------------------- #
def test_put_healthsheet_composition_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/composition'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet composition metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition",
        json={"composition": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["composition"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition",
        json={"composition": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition",
        json={"composition": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition",
        json={"composition": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_composition_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/composition'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["composition"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/composition"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["composition"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# ------------------- DATASET HEALTHSHEET COLLECTION METADATA ------------------- #
def test_put_healthsheet_collection_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/collection'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet collection metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection",
        json={"collection": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["collection"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection",
        json={"collection": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection",
        json={"collection": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection",
        json={"collection": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_collection_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/collection'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["collection"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/collection"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["collection"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# ------------------- DATASET HEALTHSHEET PREPROCESSING METADATA ------------------- #
def test_put_healthsheet_preprocessing_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet preprocessing metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing",
        json={"preprocessing": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["preprocessing"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing",
        json={"preprocessing": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing",
        json={"preprocessing": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing",
        json={"preprocessing": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_preprocessing_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["preprocessing"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/preprocessing"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["preprocessing"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# # ------------------- DATASET HEALTHSHEET USES METADATA ------------------- #
def test_put_healthsheet_uses_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/uses'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet uses metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses",
        json={"uses": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses",
        json={"uses": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert admin_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses",
        json={"uses": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses",
        json={"uses": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_uses_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/uses'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    description metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert admin_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/uses"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["uses"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# ------------------- DATASET HEALTHSHEET DISTRIBUTION METADATA ------------------- #
def test_put_healthsheet_distribution_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/distribution'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet distribution metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution",
        json={"distribution": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["distribution"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution",
        json={"distribution": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution",
        json={"distribution": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution",
        json={"distribution": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_distribution_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    distribution metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["distribution"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/distribution"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["distribution"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match


# ------------------- DATASET HEALTHSHEET MAINTENANCE METADATA ------------------- #
def test_put_healthsheet_maintenance_dataset_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/healthsheet/maintenance'
    endpoint is requested (PUT)
    Then check that the response is valid and updates the dataset
    healthsheet maintenance metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance",
        json={"maintenance": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["maintenance"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance",
        json={"maintenance": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance",
        json={"maintenance": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.put(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance",
        json={"maintenance": '[{"id":1,"question":"For","response":"new"}]'},
    )
    assert viewer_response.status_code == 403


def test_get_dataset_healthsheet_maintenance_metadata(clients):
    """
    Given a Flask application configured for testing and a study ID and dataset ID
    When the '/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance'
    endpoint is requested (GET)
    Then check that the response is valid and retrieves the dataset
    maintenance metadata content
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    study_id = pytest.global_study_id["id"]  # type: ignore
    dataset_id = pytest.global_dataset_id

    response = _logged_in_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance"
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert (
        response_data["maintenance"] == '[{"id":1,"question":"For","response":"new"}]'
    )

    admin_response = _admin_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance"
    )
    assert admin_response.status_code == 200
    admin_response_data = json.loads(admin_response.data)
    assert (
        admin_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    editor_response = _editor_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance"
    )
    assert editor_response.status_code == 200
    editor_response_data = json.loads(editor_response.data)
    assert (
        editor_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    viewer_response = _viewer_client.get(
        f"/study/{study_id}/dataset/{dataset_id}/healthsheet/maintenance"
    )
    assert viewer_response.status_code == 200
    viewer_response_data = json.loads(viewer_response.data)
    assert (
        viewer_response_data["maintenance"]
        == '[{"id":1,"question":"For","response":"new"}]'
    )

    # Editor was the last successful PUT request, so the response data should match

