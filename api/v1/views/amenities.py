#!/usr/bin/python3
"""views for Amenity objects
    It handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False)
def get_all_amenities():
    """return list of all amenities instans in storage engine"""
    amenity = storage.all(Amenity).values()
    return jsonify([a.to_dict() for a in amenity])


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_an_amenity(amenity_id):
    """retrieve an amenity by its id from the storage engine"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete__amenity(amenity_id):
    """remove an amenity from storage"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """add new amenity to the storage engine"""
    new_amenity = request.get_json()
    if not new_amenity:
        return jsonify({"error": "Not a JSON"}), 400
    if not ("name" in new_amenity):
        return jsonify({"error": "Missing name"}), 400
    new = Amenity(**new_amenity)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_an_amenity(amenity_id):
    """update an amenity in the storage engine"""
    update_obj = storage.get(Amenity, amenity_id)
    changes = request.get_json()
    print(request.headers["Content-Type"])
    if not update_obj:
        abort(404)
    if not changes:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in changes.items():
        if not (k in ("id", "created_at", "updated_at")):
            setattr(update_obj, k, v)
    update_obj.save()
    return jsonify(update_obj.to_dict())
