#!/usr/bin/env python3
""" Module of Users views
"""
import os
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    Handle user login

    This endpoint is used to login a user using the session authentication
    mechanism. It expects a JSON body with the email and password of the user.

    Return:
        dictionary representation of user if found else error message
    """
    # Get the email and password from the JSON body of the request
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the email and password are provided
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    # Search for the user with the given email
    users = User.search({"email": email})

    # Check if the user exists
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404

    # Iterate over the users and check if the password is valid
    for user in users:
        if user.is_valid_password(password):
            # Create a new session for the user
            from api.v1.app import auth
            session_id = auth.create_session(user.id)

            # Create a JSON response with the user data
            resp = jsonify(user.to_json())

            # Set the session cookie
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)

            # Return the response
            return resp

    # Return an error message if the password is invalid
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """
    Handle user logout

    This function is a Flask view that handles user logout. It is
    triggered when the client makes a DELETE request to the
    /auth_session/logout endpoint.

    It first checks if the session exists in the request. If the
    session exists, it is destroyed and a JSON response with a
    200 status code is returned. If the session does not exist,
    a 404 error is returned.

    Return:
        - JSON response with a 200 status code if the session has been
          successfully destroyed
        - 404 error if the session does not exist
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404, description="Session not found")
