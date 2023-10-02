#!/usr/bin/python3
"""RESTful api manipulation for user object"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/users", strict_slashes=False)
def get_all_users():
    """return a list of all users in the storage engine"""
    all_users = storage.all(User).values()
    return jsonify([u.to_dict() for u in all_users])


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_a_user(user_id):
    """retrieve a user from the data storage"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """permanently remove a user from data storage"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """added new user to the data storage"""
    new_user = request.get_json()
    if not new_user:
        return jsonify({"error": "Not a JSON"}), 400
    if not ("email" in new_user):
        return jsonify({"error": "Missing email"}), 400
    if not ("password" in new_user):
        return jsonify({"error": "Missing password"}), 400
    new = User(**new_user)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user_detail(user_id):
    user = storage.get(User, user_id)
    changes = request.get_json()
    if not user:
        abort(404)
    if not changes:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in changes.items():
        if not (key in ("id", "created_at", "email", "updated_at")):
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict())
