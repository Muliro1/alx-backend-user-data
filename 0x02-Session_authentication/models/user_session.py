#!/usr/bin/env python3
""" UserSession module
"""
from models.base import Base


class UserSession(Base):
    """
    Represents a user session

    A user session is a link between a user and a session ID.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a UserSession instance

        Args:
            *args: list of arguments
            **kwargs: dictionary of keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
