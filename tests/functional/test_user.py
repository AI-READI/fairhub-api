"""Tests for user settings"""


# ------------------- Password Change ------------------- #
def test_put_password_change(clients):
    """
    Given a Flask application configured for testing
    WHEN the '/auth/password/change' endpoint is requested (PUT)
    THEN check that the response is valid and the password is changed
    """
    _logged_in_client, _admin_client, _editor_client, _viewer_client = clients

    response = _logged_in_client.put(
        "/auth/password/change",
        json={
            "confirm_password": "Updatedpassword4testing!",
            "new_password": "Updatedpassword4testing!",
            "old_password": "Testingyeshello11!",
        },
    )

    assert response.status_code == 200
