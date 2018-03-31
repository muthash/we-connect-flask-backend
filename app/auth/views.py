"""Contains views to register, login and logout user"""
import datetime
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token, get_raw_jwt, jwt_required,
    fresh_jwt_required, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from app.models import User, BlacklistToken
from app.utils import (
    validate_email, validate_null, random_string, send_reset_password
)

auth = Blueprint('auth', __name__, url_prefix='/api/v1')


class RegisterUser(MethodView):
    """Method to Register a new user"""
    def post(self):
        """Endpoint to save the data to the database"""
        if request.get_json(silent=True) is None:
            response = {'message':'Bad Request. Request should be JSON format'}
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
    """Method to login a user"""
    def post(self):
        """Endpoint to login a user"""
        if request.get_json(silent=True) is None:
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
            user = User.query.filter_by(email=email).first()
            if user and user.password_is_valid(password):
                if not user.update_pass:
                    expires = datetime.timedelta(hours=1)
                    response = {
                        'message': 'Login successfull',
                        'access_token': create_access_token(identity=user.id, fresh=False, expires_delta=expires)
                    }
                    return jsonify(response), 200
                else:
                    expires = datetime.timedelta(minutes=5)
                    response = {
                        'message': 'Change your password inorder to continue',
                        'access_token': create_access_token(identity=user.id, fresh=True, expires_delta=expires)
                    }
                    return jsonify(response), 200
            response = {'message':'Invalid email or password, Please try again'}
            return jsonify(response), 401
        response = {'message': 'Please enter a valid email address'}
        return jsonify(response), 400


class LogoutUser(MethodView):
    """Method to logout a user"""
    @jwt_required
    def post(self):
        """Endpoint to logout a user"""
        jti = get_raw_jwt()['jti']
        blacklist = BlacklistToken(token=jti)
        blacklist.save()
        response = {'message': 'Successfully logged out'}
        return jsonify(response), 200


class ResetPassword(MethodView):
    """Method to reset a user password"""
    def post(self):
        """Endpoint to reset a user password"""
        if request.get_json(silent=True) is None:
            response = {'error':'Bad Request. Request should be JSON format'}
            return jsonify(response), 400
        data = request.get_json()
        email = data.get('email')

        null_input = validate_null(email=email)
        if null_input:
            response = {'message': null_input}
            return jsonify(response), 400

        if validate_email(email):
            user = User.query.filter_by(email=email).first()
            if user:
                password = random_string()
                sent = send_reset_password(email, password)
                if sent:
                    user_id = user.id
                    password_ = Bcrypt().generate_password_hash(password).decode()
                    User.update(User, user_id, password=password_, update_pass=True)
                    response = {'password': password,
                                'message':'An email has been sent with your new password'}
                    return jsonify(response), 201
                response = {'message':'Password was not reset, Try again'}
                return jsonify(response), 500
            response = {'message': 'Email does not exists'}
            return jsonify(response), 400
        response = {'message': 'Please enter a valid email address'}
        return jsonify(response), 400


class ChangePassword(MethodView):
    """Method to change a user password"""
    @fresh_jwt_required
    def put(self):
        """Endpoint to change a user password"""
        if request.get_json(silent=True) is None:
            response = {'error':'Bad Request. Request should be JSON format'}
            return jsonify(response), 400
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user_id = get_jwt_identity()

        null_input = validate_null(old_password=old_password, new_password=new_password)
        if null_input:
            response = {'message': null_input}
            return jsonify(response), 400

        user = User.query.filter_by(id=user_id).first()
        if user:
            if user.password_is_valid(old_password):
                User.update(User, user_id, password=new_password, update_pass=False)
                response = {'message':'Password changed successfully'}
                return jsonify(response), 200
            response = {'message':'Invalid old password, Please try again'}
            return jsonify(response), 401
        response = {'message': 'User does not exists'}
        return jsonify(response), 400


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
auth.add_url_rule('/login', view_func=LoginUser.as_view('login'))
auth.add_url_rule('/logout', view_func=LogoutUser.as_view('logout'))
auth.add_url_rule('/reset-password', view_func=ResetPassword.as_view('reset-password'))
auth.add_url_rule('/change-password', view_func=ChangePassword.as_view('change-password'))
