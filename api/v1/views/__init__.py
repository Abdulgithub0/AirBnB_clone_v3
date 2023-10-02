from flask import Blueprint
#from api.v1.views.index import * - getting circular import error

# create an instance of Blueprint with name app_views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# app_views's views and routes
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
