#!/usr/bin/env python3
""" doc doc doc """

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """doc doc doc

    Represents a user in the database.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    """The user's ID."""

    email = Column(String(250), nullable=False)
    """The user's email."""

    hashed_password = Column(String(250), nullable=False)
    """The user's hashed password."""

    session_id = Column(String(250), nullable=True)
    """The user's session ID if logged in."""

    reset_token = Column(String(250), nullable=True)
    """The user's reset password token."""
