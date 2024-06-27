from model.db import db

# ------------------- Password Change ------------------- #


def test_post_password_change(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/auth/password/change' endpoint is requested (PUT)
    THEN check that the response is valid and the password is changed
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients

    response = _logged_in_client.post(
        "/auth/password/change",
        json={
            "confirm_password": "Updatedpassword4testing!",
            "new_password": "Updatedpassword4testing!",
            "old_password": "Testingyeshello11!",
        },
    )
    a_response = _admin_client.post(
        "/auth/password/change",
        json={
            "confirm_password": "Updatedpassword4testing!",
            "new_password": "Updatedpassword4testing!",
            "old_password": "Testingyeshello11!",
        },
    )
    e_response = _editor_client.post(
        "/auth/password/change",
        json={
            "confirm_password": "Updatedpassword4testing!",
            "new_password": "Updatedpassword4testing!",
            "old_password": "Testingyeshello11!",
        },
    )
    v_response = _viewer_client.post(
        "/auth/password/change",
        json={
            "confirm_password": "Updatedpassword4testing!",
            "new_password": "Updatedpassword4testing!",
            "old_password": "Testingyeshello11!",
        },
    )

    assert response.status_code == 200
    assert a_response.status_code == 200
    assert e_response.status_code == 200
    assert v_response.status_code == 200
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        if table.name == 'session':
            session_entries = db.session.execute(table.select()).fetchall()
            assert len(session_entries) == 0


def test_post_password_login_invalid_old_password(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/auth/login' endpoint is requested (POST)
    THEN check that the response is an error when old password is provided
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients
    response = _logged_in_client.post(
        "/auth/login",
        json={
            "email_address": "test@fairhub.io",
            "password": "Testingyeshello11!",
        },
    )
    a_response = _admin_client.post(
        "/auth/login",
        json={
            "email_address": "admin@fairhub.io",
            "password": "Testingyeshello11!",
        },
    )
    e_response = _editor_client.post(
        "/auth/login",
        json={
            "email_address": "editor@fairhub.io",
            "password": "Testingyeshello11!",
        },
    )
    v_response = _viewer_client.post(
        "/auth/login",
        json={
            "email_address": "viewer@fairhub.io",
            "password": "Testingyeshello11!",
        },
    )
    assert response.status_code == 401
    assert a_response.status_code == 401
    assert e_response.status_code == 401
    assert v_response.status_code == 401


def test_post_login_new_password(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/auth/login' endpoint is requested (POST)
    THEN check that the response is valid when new password is provided
    """
    _logged_in_client = clients[0]
    response = _logged_in_client.post(
        "/auth/login",
        json={
            "email_address": "test@fairhub.io",
            "password": "Updatedpassword4testing!",
        },
    )
    assert response.status_code == 200
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        if table.name == 'session':
            session_entries = db.session.execute(table.select()).fetchall()
            assert len(session_entries) == 1


def test_post_logout(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/auth/login' endpoint is requested (POST)
    THEN check that the response is valid when new password is provided
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients

    response = _logged_in_client.post(
        "/auth/logout"
    )
    a_response = _admin_client.post(
        "/auth/logout"
    )
    e_response = _editor_client.post(
        "/auth/logout"
    )
    v_response = _viewer_client.post(
        "/auth/logout"
    )

    assert response.status_code == 204
    assert a_response.status_code == 204
    assert e_response.status_code == 204
    assert v_response.status_code == 204
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        if table.name == 'session':
            session_entries = db.session.execute(table.select()).fetchall()
            assert len(session_entries) == 0

