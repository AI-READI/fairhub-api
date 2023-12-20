"""Tests for user settings"""


# ------------------- Password Change ------------------- #
def test_post_password_change(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/auth/password/change' endpoint is requested (PUT)
    THEN check that the response is valid and the password is changed
    """
    _logged_in_client = clients[0]

    response = _logged_in_client.post(
        "/auth/password/change",
        json={
            "confirm_password": "Updatedpassword4testing!",
            "new_password": "Updatedpassword4testing!",
            "old_password": "Testingyeshello11!",
        },
    )

    assert response.status_code == 200


def test_post_password_login_invalid_old_password(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/auth/login' endpoint is requested (POST)
    THEN check that the response is an error when old password is provided
    """
    _logged_in_client = clients[0]
    response = _logged_in_client.post(
        "/auth/login",
        json={
            "email_address": "test@fairhub.io",
            "password": "Testingyeshello11!",
        },
    )

    assert response.status_code == 401


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
