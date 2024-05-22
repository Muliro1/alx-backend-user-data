#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from typing import Dict, Tuple
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, abort
from flask_cors import CORS, cross_origin
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = None
if os.getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
elif os.getenv("AUTH_TYPE") == "auth":
    auth = Auth()


@app.before_request
def before_request_func() -> None:
    """
    This function is called before each request and checks if the request
    is authorized.

    If the request is not authorized, it will abort the request with a
    401 or 403 status code.
    """
    if auth is None:
        return
    if not auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/']):
        # If the request does not require authentication, return
        return
    if auth.authorization_header(request) is None:
        # If the request does not have an Authorization
        # header, abort with a 401 status code
        abort(401)
    if auth.current_user(request) is None:
        # If the request does not have a valid user,
        # abort with a 403 status code
        abort(403)


@app.errorhandler(401)
def unauthorized(error) -> Tuple[Dict[str, str], int]:
    """
    Error handler for 401 Unauthorized.

    Returns a JSON response with a 401 status code and an error message.

    :param error: the error to handle
    :return: a JSON response with a 401 status code and an error message
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> Tuple[Dict[str, str], int]:
    """
    Error handler for 403 Forbidden.

    Returns a JSON response with a 403 status code and an error message.

    :param error: the error to handle
    :return: a JSON response with a 403 status code and an error message
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> Tuple[Dict[str, str], int]:
    """
    Error handler for 404 Not Found.

    Returns a JSON response with a 404 status code and an error message.

    :param error: the error to handle
    :return: a JSON response with a 404 status code and an error message
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
