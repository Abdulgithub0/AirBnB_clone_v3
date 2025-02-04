#!/usr/bin/python3
"""Instantiate a Flask application"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

# create flask instance
app = Flask(__name__)
relax_sop = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# register blueprint app_views
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """close open storage session after a request"""
    storage.close()


@app.errorhandler(404)
def handle_error(err):
    """handle resource not found error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """launch the flask instance"""
    ht = getenv("HBNB_API_HOST", "0.0.0.0")
    pt = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=ht, port=pt, threaded=True)
