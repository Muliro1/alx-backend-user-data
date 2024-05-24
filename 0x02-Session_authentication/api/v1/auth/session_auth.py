#!/usr/bin/env python3
"""
Definition of class BasicAuth
"""
import base64
from .auth import Auth
from typing import TypeVar
from uuid import uuid4
import uuid

from models.user import User


class SessionAuth(Auth):
    """ Implement Basic Authorization protocol methods

    The SessionAuth class implements the protocol for Basic Authorization.
    This protocol consists of the methods `current_user`, `extract_base64_authorization_header`,
    `decode_base64_authorization_header`, `extract_user_credentials` and `user_object_from_credentials`.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str: 
        if not user_id or not isinstance(user_id, str):
            return
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        if not session_id or not isinstance(session_id, str):
            return
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
