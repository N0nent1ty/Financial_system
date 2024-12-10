from flask import request
from flask_smorest import Blueprint
from flask import jsonify
from flask import make_response
import sys
from sqlalchemy.exc import IntegrityError # Handle to unique key problem

index_routes= Blueprint('index_routes', __name__)

#=====================================================
#Index page
#=====================================================
@index_routes.route("/", methods=["GET"])
def showDefautIndexPage():
    return "Wellcome to the index page"
