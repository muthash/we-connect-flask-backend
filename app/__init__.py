""" The create_app function wraps the creation of a new Flask object, and
    returns it after it's loaded up with configuration settings
    using app.config
"""
from flask import jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from instance.config import app_config


db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()


def create_app(config_name):
    """Function wraps the creation of a new Flask object, and returns it after it's
        loaded up with configuration settings
    """
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from app.auth.views import auth


    app.register_blueprint(auth)

    return app
