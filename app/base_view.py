import datetime
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from app.utils import validate_email, messages


class BaseView(MethodView):
    """Base view method"""
    def invalid_email(self, email):
        """Returns false if email is valid"""
        if not validate_email(email):
            return self.generate_response(messages['valid_email'], 400)
        return False

    @staticmethod
    def invalid_json():
        """Returns false if request is json"""
        if request.get_json(silent=True) is None:
            response = {'message':'Bad Request. Request should be JSON format'}
            return jsonify(response), 400
        return False

    @staticmethod
    def null_input(user_data):
        """Returns false if user input contains data"""
        if user_data:
            response = {'message': user_data}
            return jsonify(response), 400
        return False

    @staticmethod
    def generate_token(message, user, expires=datetime.timedelta(hours=1)):
        """Return access token and response to user"""
        response = {
            'message': message,
            'access_token': create_access_token(identity=user, expires_delta=expires)
        }
        return jsonify(response), 200

    @staticmethod
    def generate_response(message, status):
        """Return application/json object"""
        response = {'message': message}
        return jsonify(response), status

    def invalid_null_input(self, user_data, email):
        """Return false if not invalid"""
        if not self.null_input(user_data):
            if not self.invalid_email(email):
                return False
            return self.invalid_email(email)
        return self.null_input(user_data)
