#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from os import getenv


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

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


@ app.errorhandler(404)
def not_found(error) -> tuple:
    """ Handle 404 errors by returning a JSON response

    Args:
        error (flask.utils.RequestException): Exception instance

    Returns:
        tuple: A tuple containing a JSON response
        and a 404 status code
    """
    return jsonify({"error": "Not found"}), 404


@ app.errorhandler(401)
def unauthorized_error(error) -> tuple:
    """
    Unauthorized handler

    Args:
        error (flask.utils.RequestException): Exception instance

    Returns:
        tuple: A tuple containing a JSON response and a 401 status code

    Description:
        This function is used to handle unauthorized errors.
        It returns a JSON response with an "error"
        key set to "Unauthorized"
        and a 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


@ app.errorhandler(403)
def forbidden_error(error) -> tuple:
    """Forbidden handler

    This function is used to handle 403 errors.
    It returns a JSON response with an "error"
    key set to "Forbidden"
    and a 403 status code.

    Args:
        error (flask.utils.RequestException): Exception instance

    Returns:
        tuple: A tuple containing a JSON response and a 403 status code
    """
    return jsonify({"error": "Forbidden"}), 403


@ app.before_request
def before_request() -> str:
    """ Before Request Handler

    This function is called before each request.
    It checks if the request is authorized (i.e., the
    request has a valid authentication token or a valid
    session cookie).

    If the request is not authorized, it raises a 401
    error. If the request is authorized, it sets the
    `current_user` attribute of the request object to
    the current user.

    Args:
        request (Request): The Flask request object

    Returns:
        str: None
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None \
            and auth.session_cookie(request) is None:
        abort(401)

    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)

    request.current_user = current_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
