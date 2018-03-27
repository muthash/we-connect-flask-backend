""" The create_app function wraps the creation of a new Flask object, and
    returns it after it's loaded up with configuration settings
    using app.config
"""

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config


db = SQLAlchemy()


def create_app(config_name):
    """Function wraps the creation of a new Flask object, and returns it after it's
        loaded up with configuration settings
    """
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    return app
