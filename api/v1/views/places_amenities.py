#!/usr/bin/python3
"""view for the link between Place objects and Amenity objects.
    It handles all default RESTFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage_t, storage


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def get_a_place_amenities(place_id):
    """return a list of place amenities"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage_t == "db":
        return jsonify([a.to_dict() for a in place.amenities])
    return jsonify([a for a in place.amenity_ids])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_a_place_amenity(place_id, amenity_id):
    """delete an amenity of a place obj"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    check = None
    if not (place and amenity):
        abort(404)
    if storage_t == "db":
        for a in place.amenities:
            if a.id == amenity_id:
                check = 1
                break
    elif not (amenity_id in places.amenity_ids):
        check = 1
    if not check:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def add_amenities_to_place(place_id, amenity_id):
    """add amenity to place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    check = None
    if not (place and amenity):
        abort(404)
    if storage_t == "db":
        for a in place.amenities:
            if a.id == amenity_id:
                check = 1
                break
    elif (amenity_id in places.amenity_ids):
        check = 1
    if check:
        return jsonify(amenity.to_dict())
    if storage_t == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
