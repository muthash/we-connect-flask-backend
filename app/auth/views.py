"""Contains views to register, login reset password and logout user"""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.models import User, BlacklistToken
from app.utils import (
    validate_null, random_string, send_reset_password, messages
)
from app.base_view import BaseView

auth = Blueprint('auth', __name__, url_prefix='/api/v1')


class RegisterUser(BaseView):
    """Method to Register a new user"""
    def post(self):
        """Endpoint to save the data to the database"""
        if not self.invalid_json():
            data = request.get_json()
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')

            user_data = validate_null(email=email, username=username, password=password)
            if not self.invalid_null_input(user_data, email):
                user = User.query.filter_by(email=email).first()
                if not user:
                    user = User(email=email, username=username, password=password)
                    user.save()
                    return self.generate_response(messages['account_created'], 201)
                return self.generate_response(messages['exists'], 409)
            return self.invalid_null_input(user_data, email)
        return self.invalid_json()


class LoginUser(BaseView):
    """Method to login a user"""
    def post(self):
        """Endpoint to login a user"""
        if not self.invalid_json():
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            user_data = validate_null(email=email, password=password)
            if not self.invalid_null_input(user_data, email):
                user = User.query.filter_by(email=email).first()
                if user and user.password_is_valid(password):
                    return self.generate_token(messages['login'], user.id)
                return self.generate_response(messages['valid_epass'], 401)
            return self.invalid_null_input(user_data, email)
        return self.invalid_json()


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


class ResetPassword(BaseView):
    """Method to reset a user password"""
    def post(self):
        """Endpoint to reset a user password"""
        if not self.invalid_json():
            data = request.get_json()
            email = data.get('email')

            user_data = validate_null(email=email)
            if not self.invalid_null_input(user_data, email):
                user = User.query.filter_by(email=email).first()
                if user:
                    password = random_string()
                    sent = send_reset_password(email, password)
                    if sent:
                        user_id = user.id
                        password_ = Bcrypt().generate_password_hash(password).decode()
                        User.update(User, user_id, password=password_, update_pass=True)
                        # return self.generate_response(messages['sent_mail'], 201)
                        response = {'password': password,
                                    'message':'An email has been sent with your new password'}
                        return jsonify(response), 201
                    return self.generate_response(messages['not_reset'], 500)
                return self.generate_response(messages['valid_email'], 400)
            self.invalid_null_input(user_data, email)
        return self.invalid_json()


class ChangePassword(BaseView):
    """Method to change a user password"""
    @jwt_required
    def put(self):
        """Endpoint to change a user password"""
        if not self.invalid_json():
            data = request.get_json()
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            user_id = get_jwt_identity()
            jti = get_raw_jwt()['jti']

            user_data = validate_null(old_password=old_password, new_password=new_password)
            if not self.null_input(user_data):
                user = User.query.filter_by(id=user_id).first()
                if user:
                    if user.password_is_valid(old_password):
                        User.update(User, user_id, password=new_password, update_pass=False)
                        blacklist = BlacklistToken(token=jti)
                        blacklist.save()
                        return self.generate_response(messages['password'], 200)
                    return self.generate_response(messages['valid_pass'], 401)
                return self.generate_response(messages['valid_login'], 400)
            return self.null_input(user_data)
        return self.invalid_json()


class DeleteAccount(BaseView):
    """Method to used to delete a user's account"""
    @jwt_required
    def delete(self):
        """Endpoint to change a user password"""
        if not self.invalid_json():
            data = request.get_json()
            password = data.get('password')
            user_id = get_jwt_identity()
            jti = get_raw_jwt()['jti']

            user_data = validate_null(password=password)
            if not self.null_input(user_data):
                user = User.query.filter_by(id=user_id).first()
                if user and user.password_is_valid(password):
                    user.delete()
                    blacklist = BlacklistToken(token=jti)
                    blacklist.save()
                    return self.generate_response(messages['delete'], 200)
                return self.generate_response(messages['valid_pass'], 401)
            return self.null_input(user_data)
        return self.invalid_json()


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
auth.add_url_rule('/login', view_func=LoginUser.as_view('login'))
auth.add_url_rule('/logout', view_func=LogoutUser.as_view('logout'))
auth.add_url_rule('/reset-password', view_func=ResetPassword.as_view('reset-password'))
auth.add_url_rule('/change-password', view_func=ChangePassword.as_view('change-password'))
auth.add_url_rule('/delete-account', view_func=DeleteAccount.as_view('delete-account'))
