#!/usr/bin/env python3
"""doc doc doc """
import fnmatch
from typing import List, TypeVar
from flask import request


class Auth:
    """doc doc doc"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if the given path is in the excluded paths list
        :param path: the path to check
        :param excluded_paths: the list of paths to exclude
        :return: True if the path is in
        the excluded_paths list, False otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the value of the Authorization header from the given request
        :param request: the request object
        :return: the value of the Authorization header
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> object:
        """
        Get the current user from the given request
        :param request: the request object
        :return: the current user
        """
        return None
