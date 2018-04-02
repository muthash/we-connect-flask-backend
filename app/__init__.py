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
    from app.business.views import biz
    from app.models import BlacklistToken

    @app.errorhandler(400)
    def bad_request(error):
        """Error handler for a bad request"""
        return jsonify({'message':'The Server did not understand the request'}), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Error handler for wrong method to an endpoint"""
        return jsonify({'message':'Method not allowed'}), 405

    @app.errorhandler(500)
    def server_error(error):
        """Error handler for wrong method to an endpoint"""
        return jsonify({'message':'Database connection failed! Try Again'}), 500

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """Check if token is blacklisted"""
        jti = decrypted_token['jti']
        blacklist = BlacklistToken.query.filter_by(token=jti).first()
        if blacklist is None:
            return False
        return blacklist.revoked

    app.register_blueprint(auth)
    app.register_blueprint(biz)

    return app
