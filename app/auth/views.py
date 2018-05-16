"""Contains views to register, login reset password and logout user"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

from app.utils import (
    require_json, check_missing_field, check_email, check_password,
    validate_registration, normalise_email, random_string,
    send_reset_password, messages
)
from app.models import User, BlacklistToken
from app.base_view import BaseView

auth = Blueprint('auth', __name__, url_prefix='/api/v1')


class RegisterUser(BaseView):
    """Method to Register a new user"""
    @require_json
    def post(self):
        """Endpoint to save the data to the database"""
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        user_data = dict(email=email, username=username, password=password)
        
        if check_missing_field(**user_data):
            return jsonify(check_missing_field(**user_data)), 422
        if validate_registration(email, username, password):
            return validate_registration(email, username, password)
        
        email = normalise_email(email) 
        user = User.query.filter_by(email=email).first()
        if user:
            return self.generate_response(messages['exists'], 409)
        user = User(email=email, username=username, password=password)
        user.save()
        return self.generate_response(messages['account_created'], 201)


class LoginUser(BaseView):
    """Method to login a user"""
    @require_json
    def post(self):
        """Endpoint to login a user"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user_data = dict(email=email, password=password)

        if check_missing_field(**user_data):
            return jsonify(check_missing_field(**user_data)), 422

        email = normalise_email(email)
        user = User.query.filter_by(email=email).first()
        if user and user.password_is_valid(password):
            return self.generate_token(messages['login'], user.id)
        return self.generate_response(messages['valid_epass'], 401)
            

class LogoutUser(BaseView):
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
    @require_json
    def post(self):
        """Endpoint to reset a user password"""
        data = request.get_json()
        email = data.get('email')

        user_data = dict(email=email)
        if check_missing_field(**user_data):
            return jsonify(check_missing_field(**user_data)), 422
        if check_email(email):
            return check_email(email)
        
        email = normalise_email(email)
        user = User.query.filter_by(email=email).first()
        if not user:
            return self.generate_response(messages['valid_email'], 401)
        password = random_string()
        hash_password = Bcrypt().generate_password_hash(password).decode()
        send_reset_password(email, password)
        user.update(user, password=hash_password)
        return self.generate_response(messages['sent_mail'], 201)
               

class ChangePassword(BaseView):
    """Method to change a user password"""
    @jwt_required
    @require_json
    def put(self):
        """Endpoint to change a user password"""
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user_id = get_jwt_identity()
        jti = get_raw_jwt()['jti']

        user_data = dict(old_password=old_password, new_password=new_password)
        if check_missing_field(**user_data):
            return jsonify(check_missing_field(**user_data)), 422
        if check_password(new_password):
            return check_password(new_password)
                
        user = User.query.filter_by(id=user_id).first()
        if user and user.password_is_valid(old_password):
            hash_password = Bcrypt().generate_password_hash(new_password).decode()                
            user.update(user, password=hash_password)
            blacklist = BlacklistToken(token=jti)
            blacklist.save()
            return self.generate_response(messages['password'], 201)
        return self.generate_response(messages['valid_pass'], 401)

# class DeleteAccount(BaseView):
#     """Method to used to delete a user's account"""
#     @jwt_required
#     @require_json
#     def delete(self):
#         """Endpoint to change a user password"""
#         data = request.get_json()
#         password = data.get('password')
#         user_id = get_jwt_identity()
#         jti = get_raw_jwt()['jti']

#         if check_missing_field(**user_data):
#             return jsonify(check_missing_field(**user_data)), 422
    
#         user = User.query.filter_by(id=user_id).first()
#         if user and user.password_is_valid(password):
#             user.delete()
#             blacklist = BlacklistToken(token=jti)
#             blacklist.save()
#             return self.generate_response(messages['delete'], 200)
#         return self.generate_response(messages['valid_pass'], 401)


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
auth.add_url_rule('/login', view_func=LoginUser.as_view('login'))
auth.add_url_rule('/logout', view_func=LogoutUser.as_view('logout'))
auth.add_url_rule('/reset-password', view_func=ResetPassword.as_view('reset-password'))
auth.add_url_rule('/change-password', view_func=ChangePassword.as_view('change-password'))
# auth.add_url_rule('/delete-account', view_func=DeleteAccount.as_view('delete-account'))
