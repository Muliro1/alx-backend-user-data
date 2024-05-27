#!/usr/bin/env python3

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Registers a new user.

    Args:
        email: The user's email.
        password: The user's password.
    """
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password}
    )
    assert response.status_code == 200
    # Check that the response is correct
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in a user with a wrong password.

    Args:
        email: The user's email.
        password: The user's password.
    """
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in a user.

    Args:
        email: The user's email.
        password: The user's password.

    Returns:
        The session ID of the logged in user.
    """
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 200
    # Check that the response is correct
    assert response.json() == {"email": email, "message": "logged in"}
    # Return the session ID
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Tests the profile endpoint with an unlogged user.

    This test tests the profile endpoint by sending a GET request to
    it. Since the user is not logged in, the endpoint should return a
    403 status code.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Tests the profile endpoint with a logged user.

    This test tests the profile endpoint by sending a GET request to
    it. Since the user is logged in, the endpoint should return a
    200 status code and the user's email.
    """
    response = requests.get(
        f"{BASE_URL}/profile",
        cookies={"session_id": session_id}
    )
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """
    Logs out a user.

    This function tests the logout endpoint by sending a DELETE request
    to it. Since the user is logged in, the endpoint should return a
    200 status code and a message indicating the user has been logged out.

    Args:
        session_id: The session ID of the logged in user.
    """
    response = requests.delete(
        f"{BASE_URL}/sessions", cookies={"session_id": session_id}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Gets the reset token of a user.

    This function tests the reset password endpoint by sending a POST
    request to it. Since the user is not logged in, the endpoint should
    return a 200 status code.

    Args:
        email: The user's email.

    Returns:
        The reset token of the user.
    """
    response = requests.post(
        f"{BASE_URL}/reset_password",
        data={"email": email}
    )
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates a user's password.

    This function tests the reset password endpoint by sending a PUT
    request to it. Since the user is not logged in, the endpoint
    should return a 200 status code.

    Args:
        email: The user's email.
        reset_token: The reset password token.
        new_password: The new password.
    """
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        },
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
