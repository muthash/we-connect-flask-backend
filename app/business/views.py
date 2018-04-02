"""Contains views to register, login reset password and logout user"""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity, jwt_optional
from flask_bcrypt import Bcrypt
from app.models import User,  Business
from app.utils import (
    validate_null, random_string, send_reset_password, messages,
    remove_more_spaces
)
from app.base_view import BaseView

biz = Blueprint('biz', __name__, url_prefix='/api/v1/business')
POSTS_PER_PAGE = 1


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
    
    @jwt_required
    def put(self, business_id):
        """update a single business"""
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
                business = Business.query.filter_by(id=business_id, user_id=user_id).first()
                if business:
                    Business.update(Business, business_id, **data_)
                    return self.generate_response(messages['business_updated'], 200)
                return self.generate_response(messages['forbidden'], 403)
            return self.null_input(business_data)
        return self.invalid_json()

    @jwt_required
    def delete(self, business_id):
        """delete a single business"""
        if not self.invalid_json():
            data = request.get_json()
            password = data.get('password')
            user_id = get_jwt_identity()

            user_data = validate_null(password=password)
            if not self.null_input(user_data):
                user = User.query.filter_by(id=user_id).first()
                if user and user.password_is_valid(password):
                    business = Business.query.filter_by(id=business_id, user_id=user_id).first()
                    if business:
                        business.delete()
                        return self.generate_response(messages['business_delete'], 200)
                    return self.generate_response(messages['forbidden'], 403)
                return self.generate_response(messages['valid_pass'], 401)
            return self.null_input(user_data)
        return self.invalid_json()

    @jwt_optional
    def get(self, business_id):
        """return a list of all businesses else a single business"""
        if business_id is None:
            page = request.args.get('page', 1, type=int)
            page_items = Business.query.paginate(page, POSTS_PER_PAGE, False)
            page_items_list = [Business.serialize() for Business in page_items.items]
            if page_items_list:
                next_url = page_items.next_num  if page_items.has_next else None
                prev_url = page_items.prev_num  if page_items.has_prev else None
                response = {
                    'message': messages['businesses'],
                    'businesses': page_items_list,
                    'next_page': next_url,
                    'prev_page': prev_url
                }
                return jsonify(response), 200
            return self.generate_response(messages['no_business'], 404)
        else:
            business = Business.query.filter_by(id=business_id).first()
            if business:
                reviews = [business.reviews.serialize() for review in business.reviews]
                response = {
                    'message': 'Business found',
                    'business': business.serialize(),
                    'number_of_reviews': len(business.reviews),
                    'reviews': reviews
                }
                return jsonify(response), 200
            return self.generate_response(messages['not_found'], 404)


business_view = BusinessManipulation.as_view('businesses')
biz.add_url_rule('', defaults={'business_id':None}, view_func=business_view, methods=['GET',])
biz.add_url_rule('', view_func=business_view, methods=['POST',])
biz.add_url_rule('/<int:business_id>', view_func=business_view, methods=['GET', 'PUT', 'DELETE'])


# biz.add_url_rule('', view_func=BusinessManipulation.as_view('businesses'))
# biz.add_url_rule('/<int:category>/<int:location>', view_func=BusinessManipulation.as_view('filter-businesses'))
# biz.add_url_rule('/<int:business_id>/<int:my>', view_func=business_view, methods=['GET', 'PUT', 'DELETE'])
