#!/usr/bin/env python3
""" doc doc doc """

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import TypeVar


def _hash_password(password: str) -> bytes:
    """
    Hashes a password with a randomly generated salt using bcrypt.

    Args:
        password: The password to hash.

    Returns:
        A bytes object containing the hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a randomly generated UUID.

    Returns:
        A string containing the randomly generated UUID.
    """
    return str(uuid.uuid4())


UserT = TypeVar("UserT", bound=User)


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the user's login is valid.

        Args:
            email: The user's email.
            password: The user's password.

        Returns:
            True if the user's login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email: The user's email.
            password: The user's password.

        Returns:
            The newly created user.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user

    def create_session(self, email: str) -> str:
        """Creates a new session for the user.

        Args:
            email: The user's email.

        Returns:
            The newly created session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> UserT:
        """Gets the user from a session ID.

        Args:
            session_id: The session ID.

        Returns:
            The user associated with the session ID.
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user's session.

        Args:
            user_id: The user's ID.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Gets a reset password token for the user.

        Args:
            email: The user's email.

        Returns:
            The reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the user's password.

        Args:
            reset_token: The reset password token.
            password: The new password.
        """
        if reset_token is None or password is None:
            raise ValueError

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        pw = _hash_password(password)
        self._db.update_user(user.id, hashed_password=pw, reset_token=None)
