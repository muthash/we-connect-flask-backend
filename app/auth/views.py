"""Contains views to register, login and logout user"""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from app.models import User
from app.utils import validate_email, validate_null

auth = Blueprint('auth', __name__, url_prefix='/api/v1')


class RegisterUser(MethodView):
    """
    This Method view is used to Register a new user
    using the POST method
    """
    def post(self):
        """Endpoint used to save the data to the database"""
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
            return jsonify(response), 201
        if validate_email(email):
            user = user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=email, username=username, password=password)
                user.save()
                response = {
                    'message': 'You registered successfully'
                }
                return jsonify(response), 201


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
