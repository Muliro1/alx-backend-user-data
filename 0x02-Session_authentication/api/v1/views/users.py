#!/usr/bin/env python3
""" Module of Users views
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users

    Return:
      - list of all User objects JSON represented
    """
    # Retrieve all users from the database
    all_users = User.all()

    # Create a list of User objects JSON represented
    all_users_json = [user.to_json() for user in all_users]

    # Return the list of all users as a JSON response
    return jsonify(all_users_json)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/:id

    Path parameter:
      - User ID

    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    # Check if the user_id is None
    if user_id is None:
        abort(404, description="User ID is missing")

    # Check if the user_id is "me"
    if user_id == 'me':
        # Check if there is a current_user
        if request.current_user is None:
            abort(404, description="User ID is \"me\" but no current user")
        else:
            # If the user_id is "me" and there is a current_user, return the
            # JSON representation of the current_user
            return jsonify(request.current_user.to_json())

    # Retrieve the user from the database using the User.get method
    user = User.get(user_id)

    # Check if the user was not found
    if user is None:
        abort(404, description="User not found")

    # Return the JSON representation of the user
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/:id

    Path parameter:
      - User ID

    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404, description="User ID is missing")

    # Retrieve the user from the database using the User.get method
    user = User.get(user_id)

    # Check if the user was not found
    if user is None:
        abort(404, description="User not found")

    # Delete the user
    user.remove()

    # Return an empty JSON response with a 200 status code
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    POST /api/v1/users/

    Creates a new user in the database using the provided information
    in the JSON body of the request.

    JSON body:
      - email (required)
      - password (required)
      - last_name (optional)
      - first_name (optional)

    Return:
      - User object JSON represented if the user has been successfully created
      - 400 status code and a JSON response with an error message if the user
        can't be created
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None

    # Check if the JSON body is correctly formatted
    if rj is None:
        error_msg = "Wrong format"
    # Check if the email is provided
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    # Check if the password is provided
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"

    # If there is an error, return a 400 status code and a JSON response with
    # the error message
    if error_msg is not None:
        return jsonify({'error': error_msg}), 400

    # Create a new user
    try:
        user = User()
        user.email = rj.get("email")
        user.password = rj.get("password")
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        # If the user can't be created, return a 400 status code and a JSON response with
        # the error message
        return jsonify({'error': "Can't create User: {}".format(e)}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    PUT /api/v1/users/:id

    Update a User based on the given User ID.

    Path parameter:
      - User ID

    JSON body:
      - last_name (optional)
      - first_name (optional)

    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    if user_id is None:
        # If the User ID is not provided, return a 404 error
        abort(404)

    # Retrieve the User object from the database using the User.get method
    user = User.get(user_id)

    # Check if the User object was not found
    if user is None:
        # If the User object was not found, return a 404 error
        abort(404)

    # Try to get the JSON body from the request
    try:
        rj = request.get_json()
    except Exception as e:
        # If the JSON body is not correctly formatted, return a 400 error
        return jsonify({'error': "Wrong format"}), 400

    # Check if the first_name and last_name are provided in the JSON body
    if rj.get('first_name') is not None:
        # Update the first_name of the User object
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        # Update the last_name of the User object
        user.last_name = rj.get('last_name')

    # Save the User object
    user.save()

    # Return the User object JSON represented
    return jsonify(user.to_json()), 200
