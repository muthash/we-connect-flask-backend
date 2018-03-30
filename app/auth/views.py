"""Contains views to register, login and logout user"""
import datetime
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token, create_refresh_token
)
from app.models import User
from app.utils import validate_email, validate_null

auth = Blueprint('auth', __name__, url_prefix='/api/v1')


class RegisterUser(MethodView):
    """Method to Register a new user"""
    def post(self):
        """Endpoint to save the data to the database"""
        if not request.get_json():
            response = {'error':'Bad Request. Request should be JSON format'}
            return jsonify(response), 400
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        null_input = validate_null(email=email, username=username, password=password)
        if null_input:
            response = {'message': null_input}
            return jsonify(response), 400

        if validate_email(email):
            user = user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=email, username=username, password=password)
                user.save()
                response = {'message': 'Account created successfully'}
                return jsonify(response), 201
            response = {'message': 'User already exists'}
            return jsonify(response), 409
        response = {'message': 'Please enter a valid email address'}
        return jsonify(response), 400


class LoginUser(MethodView):
    """Method to login a new user"""
    def post(self):
        """Endpoint to login a user"""
        if not request.get_json():
            response = {'error':'Bad Request. Request should be JSON format'}
            return jsonify(response), 400
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        null_input = validate_null(email=email, password=password)
        if null_input:
            response = {'message': null_input}
            return jsonify(response), 400

        if validate_email(email):
            user = user = User.query.filter_by(email=email).first()
            if user and user.password_is_valid(password):
                expires = datetime.timedelta(minutes=5)
                response = {
                    'message': 'Login successfull',
                    'access_token': create_access_token(identity=user.id, fresh=False, expires_delta=expires),
                    'refresh_token': create_refresh_token(identity=user.id)
                }
                return jsonify(response), 200
            response = {'message':'Invalid email or password, Please try again'}
            return jsonify(response), 401
        response = {'message': 'Please enter a valid email address'}
        return jsonify(response), 400


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
auth.add_url_rule('/login', view_func=LoginUser.as_view('login'))
