#!/usr/bin/python3
"""RESTful Api for the cities object model"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def cities_under_a_state(state_id):
    """retrieve all the cities belonging to a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_a_city(city_id):
    """retrieve a city obj by its id from storage engine"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_a_city(city_id):
    """remove a city obj from the the storage engine"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """create a city under a selected state"""
    state = storage.get(State, state_id)
    new_city = request.get_json()
    if not state:
        abort(404)
    if not new_city:
        return jsonify({"error": "Not a JSON"}), 400
    if not ("name" in new_city):
        return jsonify({"error": "Missing name"}), 400
    new_city.update({"state_id": state_id})
    new = City(**new_city)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_a_city(city_id):
    """update a city if found in storage engine else abort"""
    city = storage.get(City, city_id)
    new_update = request.get_json()
    if not city:
        abort(404)
    if not new_update:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in new_update.items():
        if not (key in ("id", "created_at", "updated_at")):
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict())
