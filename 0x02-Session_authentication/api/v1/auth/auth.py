#!/usr/bin/env python3
"""
Module to manage the API authentication.
"""
from os import getenv
from flask import request
from typing import List, TypeVar



class Auth:
    """
    manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required to access path.
        /api/v1/status

        /api/v1/stat*
        ['/api/v1/stat', '']
        """
        # be slash tolerant: path=/api/v1/status and path=/api/v1/status/
        if path and not path.endswith('/'):
            path = path + '/'
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.split('*')[0]):
                return False

        # Returns True if path is None
        if not path or path not in excluded_paths:
            return True
        # Returns True if excluded_paths is None or empty
        if not excluded_paths or excluded_paths == []:
            return True
        # Returns False if path is in excluded_paths
        if path in excluded_paths:
            return False
        # You can assume excluded_paths contains string path always ending by a /
        return False
        
                
    
    def authorization_header(self, request=None) -> None:
        """
        Checks for authorization header in request

        'Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=='
        """
        key = 'Authorization'

        if request is None or key not in request.headers:
            return
        return request.headers.get(key)
    
    def current_user(self, request=None) -> None:
        """
        Only Returns None
        """
        return
    def session_cookie(self, request=None):
        if not request:
            return
        session_name = getenv("SESSION_NAME")
        cookie = request.cookies.get(session_name)
        return cookie
if __name__ == '__main__':
    pass
