#!/usr/bin/python3
"""defined the views with their respective routes"""

from api.v1.views import app_views
from flask import jsonify
from models.base_model import BaseModel
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """return status"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats", strict_slashes=False)
def obj_stats_view():
    """retrieve the total number instan obj per each class"""
    all_cls = BaseModel.__subclasses__()
    cls_count = {}
    for cls in all_cls:
        cls_count[cls.__name__.lower()] = storage.count(cls)
    return jsonify(cls_count)
