#!/usr/bin/python3
"""views for Review object.
    It handles all default RESTFul API actions
"""


from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_reviews(place_id):
    """return all reviews under a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([r.to_dict() for r in place.reviews])


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_a_review(review_id):
    """retrieve a review from data storage"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_a_review(review_id):
    """remove a review from data storage"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_a_place(place_id):
    """add new review to data storage"""
    place = storage.get(Place, place_id)
    new_review = request.get_json()
    if not place:
        abort(404)
    if not new_review:
        return jsonify({"error": "Not a JSON"}), 400
    if not ("text" in new_place):
        return jsonify({"error": "Missing text"}), 400
    if not ("user_id" in new_place):
        return jsonify({"error": "Missing user_id"}), 400
    if not storage.get(User, new_place["user_id"]):
        abort(404)
    new = Review(**new_review)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_a_place(review_id):
    """update a review obj in data storage"""
    review = storage.get(Review, review_id)
    changes = request.get_json()
    if not review:
        abort(404)
    if not changes:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in changes.items():
        if not (key in ("id", "created_at", "update_at",
                        "place_id", "user_id")):
            setattr(review, key, val)
    storage.save()
    return jsonify(review.to_dict())
