#!/usr/bin/python3
"""handle views for State obj related"""

from api.v1.views import app_views
from flask import jsonify, abort, request
import models as m


@app_views.route("/states", strict_slashes=False)
def get_all_states():
    """get all instans of class State from the storage engine"""
    states = m.storage.all(m.state.State).values()
    obj_lst = [state.to_dict() for state in states]
    return jsonify(obj_lst)


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_a_state(state_id):
    """return a state obj by using it id from storage engine"""
    obj = m.storage.get(m.state.State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_a_state(state_id):
    """remove a state obj from the storage engine"""
    obj = m.storage.get(m.state.State, state_id)
    if not obj:
        abort(404)
    m.storage.delete(obj)
    m.storage.save()
    return (jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_a_state():
    """add new state into storage engine"""
    try:
        new_state = request.get_json()
        if not new_state:
            raise TypeError("Not a JSON")
        if not ("name" in new_state):
            raise ValueError("Missing name")
    except (TypeError, ValueError) as e:
        return jsonify({"error": e}), 400
    new_state = m.state.State(**new_state)
    new_state.save()
    return (jsonify(new_state.to_dict(), 201))


@app_views.route("states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_a_state(state_id):
    """update an existing state obj by its id on storage engine"""
    obj = m.storage.get(m.state.State, state_id)
    new_changes = request.get_json()
    if not obj:
        abort(404)
    if not new_changes:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in new_changes.items():
        if not (key in ("updated_at", "created_at", "id")):
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict())
