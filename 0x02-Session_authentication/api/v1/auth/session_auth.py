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
    """
    pass