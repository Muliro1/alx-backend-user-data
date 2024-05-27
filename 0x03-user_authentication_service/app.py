#!/usr/bin/env python3
""" doc doc doc """
from flask import Flask, jsonify, request, make_response
from flask import abort, Response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Response:
    """ Log the user in.

    This endpoint is used to log in a user. It receives an email and a
    password as form data. If the credentials are valid, it returns a
    JSON response with a 200 status code and sets a cookie with the
    session ID.

    If the credentials are invalid, it returns a 401 status code.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if the credentials are valid
    if AUTH.valid_login(email, password):
        # Create a JSON response with a 200 status code
        jsoni = jsonify({"email": email, "message": "logged in"}), 200
        response = make_response(jsoni)
        # Set a cookie with the session ID
        response.set_cookie("session_id", AUTH.create_session(email))
        return response

    # Abort with a 401 status code if the credentials are invalid
    abort(401)


@app.route("/users", methods=["POST"])
def users() -> Response:
    """doc doc doc

    This endpoint is used to create a new user. It receives an email and a
    password as form data. If the credentials are valid, it returns a
    JSON response with a 200 status code and the user's email.

    If the email is already registered, it returns a 400 status code.
    """
    email = request.form["email"]
    password = request.form["password"]
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/", methods=["GET"])
def welcome() -> Response:
    """This endpoint is used to return a welcome message.

    It receives a GET request and returns a JSON response with a 200
    status code.

    The response contains a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Response:
    """Deletes the user's session.

    This endpoint is used to log out a user. It receives a DELETE request
    and returns a 200 status code.

    If the session ID does not exist, it returns a 403 status code.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Response:
    """Retrieves the user's profile.

    This endpoint is used to retrieve the user's profile. It receives a GET
    request and returns a JSON response with a 200 status code.

    The response contains the user's email.

    If the user is not logged in, it returns a 403 status code.
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """This endpoint is used to retrieve a password reset token.

    It receives a POST request with an email as form data. If the user
    associated with the email exists, it returns a JSON response with a 200
    status code.

    The response contains the user's email and the password reset token.

    If the user associated with the email does not exist, it returns a 403
    status code.
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """This endpoint is used to update a user's password.

    It receives a PUT request with the user's email, the password reset
    token, and the new password as form data. If the password reset token
    is valid, it returns a JSON response with a 200 status code.

    The response contains the user's email and a message indicating the
    password has been updated.

    If the password reset token is invalid, it returns a 403 status code.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
