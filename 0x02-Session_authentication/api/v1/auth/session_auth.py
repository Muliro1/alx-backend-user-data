#!/usr/bin/env python3
"""
Definition of class BasicAuth
"""
import base64
from .auth import Auth
from typing import TypeVar

from models.user import User


class SessionAuth(Auth):
    """ Implement Basic Authorization protocol methods

    The SessionAuth class implements the protocol for Basic Authorization.
    This protocol consists of the methods `current_user`, `extract_base64_authorization_header`,
    `decode_base64_authorization_header`, `extract_user_credentials` and `user_object_from_credentials`.
    """
    pass
