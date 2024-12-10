#import flask packages
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from sqlalchemy import text
from flask_smorest import Api
from flask_cors import CORS
from flask_migrate import Migrate


#import system pakcages
import logging
import coloredlogs
import os
import sys
from pathlib import Path


#import database
from .database import db

#import config setting
from .flaskconfig import CConfig

#import routes
from .routes.default_route import index_routes
from .routes.registration_page import registration_bp

def setup_database(app):
    with app.app_context():
        db.create_all()
    db.session.commit()    




def create_app(db_url=None):
    
    coloredlogs.install()
    logger=logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    app =Flask(__name__)
    #register blue prints


    # Load configuration
    app.config.from_object(CConfig)

    # Set OS env for password
    

    #Allow cross origin from all source
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    migrate = Migrate(app, db)
    api=Api(app)


    @app.errorhandler(404)
    def handle_404(httpStatus):
        return f"{httpStatus}"

    #registry blueprints
    api.register_blueprint(index_routes)
    api.register_blueprint(registration_bp)

    logger.info("Registered URLs:")
    for rule in app.url_map.iter_rules():
        logger.info(f"{rule.endpoint}: {rule}")
    return app