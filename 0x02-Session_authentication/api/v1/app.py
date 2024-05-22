#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """
    Filter each request before it's handled by the proper route.

    This function is a Flask hook that runs before each request.
    It checks if the current request requires authentication and
    if the user is authorized to access the requested resource.
    If the request requires authentication and the user is not authorized,
    it aborts the request with a 401 status code.
    If the request requires authentication and the user is authorized but
    does not have the required permissions, it aborts the request with a
    403 status code.
    """
    if auth is None:
        # If AUTH_TYPE is not set, do not perform any authentication
        pass
    else:
        # Get the current user from the request
        setattr(request, "current_user", auth.current_user(request))
        excluded = [
            # The following paths do not require authentication
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
        if auth.require_auth(request.path, excluded):
            # If the request requires authentication, check if the user is authorized
            cookie = auth.session_cookie(request)
            if auth.authorization_header(request) is None and cookie is None:
                # If the user is not authorized, abort the request with a 401 status code
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                # If the user is authorized but does not have the required permissions,
                # abort the request with a 403 status code
                abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found handler.

    This function is a Flask error handler that runs when the client
    makes a request to a non-existent resource. It returns a JSON
    response with a 404 status code and a message indicating that
    the requested resource was not found.

    Args:
        error (int): The error code that triggered this handler.

    Returns:
        str: A JSON response with a 404 status code and a message
            indicating that the requested resource was not found.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Request unauthorized handler.

    This function is a Flask error handler that runs when the client
    makes a request to a resource that requires authentication but
    the user is not authorized to access the requested resource.
    It returns a JSON response with a 401 status code and a message
    indicating that the user is unauthorized to access the requested
    resource.

    Args:
        error (int): The error code that triggered this handler.

    Returns:
        str: A JSON response with a 401 status code and a message
            indicating that the user is unauthorized to access the requested
            resource.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Request unauthorized handler.

    This function is a Flask error handler that runs when the client
    makes a request to a resource that requires authentication and
    authorization but the user is not authorized to access the
    requested resource.

    It returns a JSON response with a 403 status code and a message
    indicating that the user is not authorized to access the requested
    resource.

    Args:
        error (int): The error code that triggered this handler.

    Returns:
        str: A JSON response with a 403 status code and a message
            indicating that the user is not authorized to access the requested
            resource.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
