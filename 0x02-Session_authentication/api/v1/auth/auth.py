#!/usr/bin/env python3
""" Auth module for API authentication """
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if a path requires authentication
        Args:
            path (str): The path to check
            excluded_paths (List[str]): List of paths that do not require
            authentication
        Returns:
            bool: True if authentication is required, False otherwise
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Add trailing slash to the path if it's not already there
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Add trailing slash to the excluded path if it's not already there
            if not excluded_path.endswith('/'):
                excluded_path += '/'
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method to get the authorization header
        Args:
            request (Request): The Flask request object
        Returns:
            str: None (for now, will be implemented later)
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get the current user
        Args:
            request (Request): The Flask request object
        Returns:
            TypeVar('User'): None (for now, will be implemented later)
        """
        return None
    def session_cookie(self, request=None):
        if not request:
            return None
        session_name = getenv('SESSION_NAME')
        cookie = request.cookies.get(session_name)
        return cookie
