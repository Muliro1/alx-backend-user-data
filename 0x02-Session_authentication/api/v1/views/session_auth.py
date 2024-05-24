#!/usr/bin/env python3
"""
Module for Basic Authentication
"""
from base64 import b64decode
import uuid
from typing import Optional, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Class that handles basic authentication
    """
    pass


if __name__ == '__main__':
    pass
