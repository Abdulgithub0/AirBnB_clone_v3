#!/usr/bin/python3
"""view for Place objects.
    It handles all default RESTFul API actions
"""

from models import storage
from api.v1.views import app_views
from models.place import Place
from flask import jsonify, abort, request
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id):
    """return all places under a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([p.to_dict() for p in city.places])


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_a_place(place_id):
    """retrieve a place from data storage"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_a_place(place_id):
    """remove a place from data storage"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_a_place(city_id):
    """all new place to data storage"""
    city = storage.get(City, city_id)
    new_place = request.get_json()
    if not city:
        abort(404)
    if not new_place:
        return jsonify({"error": "Not a JSON"}), 400
    if not ("name" in new_place):
        return jsonify({"error": "Missing name"}), 400
    if not ("user_id" in new_place):
        return jsonify({"error": "Missing user_id"}), 400
    if not storage.get(User, new_place["user_id"]):
        abort(404)
    new = Place(**new_place)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_a_place(place_id):
    """update a place detail in data storage"""
    place = storage.get(Place, place_id)
    changes = request.get_json()
    if not place:
        abort(404)
    if not changes:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in changes.items():
        if not (key in ("id", "created_at", "update_at",
                        "city_id", "user_id")):
            setattr(place, key, val)
    storage.save()
    return jsonify(place.to_dict())

@app_views.route("/places_search", strict_slashes=False)
def handler_for_places():
    """retrieves all Place objects depending of
        the JSON in the body of the request
    """
    body = request.get_json()
    if not body:
        return jsonify({"error": "Not a JSON"}), 400
    if len(body):
        return jsonify([p.to_dict() for p in storage.all(Place)])
    if len(filter(lambda x: len(x) > 0, body.values())) == 0:
        return jsonify([p.to_dict() for p in storage.all(Place)])
    if body.get("states") and len(body.get("states")

