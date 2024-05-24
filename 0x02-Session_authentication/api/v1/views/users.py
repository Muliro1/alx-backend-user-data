#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users

    Return:
        - list of all User objects JSON represented
    """
    # Get all users from the database and convert them to JSON
    all_users = [user.to_json() for user in User.all()]
    # Return the list of users in JSON format
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id

    Path parameter:
      - User ID

    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if not user_id or (user_id == 'me' and not request.current_user):
        # If no user_id is provided or it is 'me' and the
        # user is not logged in, return a 404
        return abort(404)

    if user_id == 'me' and request.current_user:
        # If the user_id is 'me', return the current user
        # as JSON
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        # If the user with the given user_id doesn't exist,
        # return a 404
        abort(404)

    # Return the user with the given user_id as JSON
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id

    Path parameter:
      - User ID

    Return:
        - empty JSON is the User has been correctly deleted
        - 404 if the User ID doesn't exist
    """
    if user_id is None:
        # If no user_id is provided, return a 404
        abort(404)
    user = User.get(user_id)
    if user is None:
        # If the user with the given user_id doesn't exist, return a 404
        abort(404)
    # Remove the user from the database
    user.remove()
    # Return an empty JSON
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/

    JSON body:
        - email: a required string representing the user's email address
        - password: a required string representing the user's password
        - last_name (optional): a string representing the user's last name
        - first_name (optional): a string representing the user's first name

    Return:
        - User object JSON represented
        - 400 if can't create the new User
    """
    rj = None
    error_msg = None
    try:
        # Get the JSON body
        rj = request.get_json()
    except Exception as e:
        # If the JSON body is malformed, store an error message
        rj = None
    if rj is None:
        # If there is no JSON body, store an error message
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        # If there is no email, store an error message
        error_msg = "email missing"
    if error_msg is None and rj.get("password", "") == "":
        # If there is no password, store an error message
        error_msg = "password missing"
    if error_msg is None:
        # If there is no error message, try to create a new user
        try:
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            # Return the new user as JSON
            return jsonify(user.to_json()), 201
        except Exception as e:
            # If there is an error, store an error message
            error_msg = "Can't create User: {}".format(e)
    # Return an error message if there is one
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id

    Path parameter:
        - user_id: The ID of the user to update

    JSON body:
        - last_name (optional): The new last name of the user
        - first_name (optional): The new first name of the user

    Return:
        - User object JSON represented
        - 404 if the User ID doesn't exist
        - 400 if can't update the User
    """
    if user_id is None:
        abort(404)

    # Get the User with the given user_id
    user = User.get(user_id)
    if user is None:
        abort(404)

    # Get the JSON body
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None

    # If the JSON body is malformed, return an error message
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400

    # Update the user's first and last names if they are present in the JSON body
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')

    # Save the updated user
    user.save()

    # Return the updated user as JSON
    return jsonify(user.to_json()), 200
