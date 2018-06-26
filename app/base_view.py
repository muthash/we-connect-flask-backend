import datetime
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token


class BaseView(MethodView):
    """Base view method"""
    @staticmethod
    def generate_token(message, user, expires=datetime.timedelta(hours=1)):
        """Return access token and response to user"""
        response = {
            'message': message,
            'username': user.username,
            'access_token': create_access_token(identity=user.id,
                                                expires_delta=expires)
        }
        return jsonify(response), 200

    @staticmethod
    def generate_response(message, status):
        """Return application/json object"""
        response = {'message': message}
        return jsonify(response), status
