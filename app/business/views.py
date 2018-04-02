"""Contains views to register, login reset password and logout user"""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.models import User,  Business
from app.utils import (
    validate_null, random_string, send_reset_password, messages,
    remove_more_spaces
)
from app.base_view import BaseView

biz = Blueprint('biz', __name__, url_prefix='/api/v1/business')


class BusinessManipulation(BaseView):
    """Method to manipulate business endpoints"""
    @jwt_required
    def post(self):
        """Endpoint to save the data to the database"""
        if not self.invalid_json():
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            category = data.get('category')
            location = data.get('location')
            user_id = get_jwt_identity()
            
            data_ = dict(name=name, description=description, category=category, location=location)
            business_data = validate_null(**data_)
            if not self.null_input(business_data):
                user = User.query.filter_by(id=user_id).first()
                name = remove_more_spaces(name)
                description = remove_more_spaces(description)
                category = remove_more_spaces(category)
                location = remove_more_spaces(location)
                if user:
                    business = Business(**data_, user_id=user_id)
                    business.save()
                    return self.generate_response(messages['business_created'], 201)
                return self.generate_response(messages['valid_login'], 403)
            return self.null_input(business_data)
        return self.invalid_json()


biz.add_url_rule('', view_func=BusinessManipulation.as_view('businesses'))
