#!/usr/bin/env python3
"""
Definition of class Auth
"""
import os
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """
    Manages the API authentication
    """
    def __init__(self, excluded_paths: List[str]):
        self.excluded_paths = set(excluded_paths)

    def require_auth(self, path: str) -> bool:
        """
        Determines whether a given path requires authentication or not.

        Args:
            path (str): Url path to be checked

        Returns:
            bool: True if path is not in excluded_paths, else False
        """
        if path is None:
            return True
        for excluded_path in self.excluded_paths:
            if path.startswith(excluded_path):
                return False
            if excluded_path.endswith("*") and path.startswith(excluded_path[:-1]):
                return False
        return True

    def authorization_header(self, request: 'flask.Request') -> str:
        """
        Returns the authorization header from a request object.

        Args:
            request (flask.Request): Request object to be checked

        Returns:
            str: Value of the Authorization header from the request object
        """
        return request.headers.get('Authorization')

    def current_user(self, request: 'flask.Request') -> TypeVar('User'):
        """
        Returns a User instance from information from a request object.

        Args:
            request (flask.Request): Request object to be checked

        Returns:
            User: User instance from the request object
        """
        return None

    def session_cookie(self, request: 'flask.Request') -> str:
        """
        Returns a cookie from a request.

        Args:
            request (flask.Request): Request object to be checked

        Returns:
            str: Value of the _my_session_id cookie from the request object
        """
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
