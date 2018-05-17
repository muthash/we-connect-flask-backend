"""Contains views to register, login reset password and logout user"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from app.models import User,  Business
from app.utils import require_json, check_missing_field, messages, remove_more_spaces, remove_none_fields, filter_business
from app.base_view import BaseView

biz = Blueprint('biz', __name__, url_prefix='/api/v1/businesses')


class BusinessManipulation(BaseView):
    """Method to manipulate business endpoints"""
    @jwt_required
    @require_json
    def post(self):
        """Endpoint to save the data to the database"""
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        location = data.get('location')
        user_id = get_jwt_identity()
            
        data = dict(name=name, description=description, category=category, location=location)
        if check_missing_field(**data):
            return jsonify(check_missing_field(**data)), 422
                
        user = User.query.filter_by(id=user_id).first()
        name = remove_more_spaces(name)
        description = remove_more_spaces(description)

        if not user:
            return self.generate_response(messages['valid_login'], 403)
        business = Business(name, description, category, location, user_id)
        business.save()
        return self.generate_response(messages['business_created'], 201)
    
    @jwt_required
    @require_json
    def put(self, business_id):
        """update a single business"""
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        location = data.get('location')
        user_id = get_jwt_identity()

        data = dict(name=name, description=description, category=category, location=location)
        if not remove_none_fields(**data):
            return self.generate_response(messages['one_update'], 422)
        
        update_data = remove_none_fields(**data)
        business = Business.query.filter_by(id=business_id).first()
        if not business:
            return self.generate_response(messages['not_found'], 200)
        if business.user_id != user_id:
            return self.generate_response(messages['forbidden'], 403)
        business.update(business, **update_data)
        response = {'message': messages['business_updated'],
                    'business': business.serialize()}
        return jsonify(response), 200


    @jwt_required
    @require_json
    def delete(self, business_id):
        """delete a single business"""
        data = request.get_json()
        password = data.get('password')
        user_id = get_jwt_identity()

        user_data = dict(password=password)
        if check_missing_field(**user_data):
            return jsonify(check_missing_field(**user_data)), 422
        
        user = User.query.filter_by(id=user_id).first()
        if not user.password_is_valid(password):
            return self.generate_response(messages['incorrect'], 401)
        business = Business.query.filter_by(id=business_id).first()
        if not business:
            return self.generate_response(messages['not_found'], 404)
        if business.user_id != user_id:
            return self.generate_response(messages['forbidden'], 403)
        business.delete()
        return self.generate_response(messages['business_delete'], 200)
        


    @jwt_optional
    def get(self, business_id):
        """return a list of all businesses else a single business"""
        if business_id is None:
            category = request.args.get('cat', "", type=str)
            location = request.args.get('loc', "", type=str)
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 2, type=int)

            page_items = Business.query.paginate(page, limit, False)
            if category or location:
                return filter_business(page_items, category=category, location=location)
            
            page_items_list = [business.serialize() for business in page_items.items]
            if page_items_list:
                next_url = page_items.next_num  if page_items.has_next else None
                prev_url = page_items.prev_num  if page_items.has_prev else None
                response = {'businesses': page_items_list,
                            'next_page': next_url,
                            'prev_page': prev_url
                }
                return jsonify(response), 200
            return self.generate_response(messages['no_business'], 404)
        else:
            business = Business.query.filter_by(id=business_id).first()
            if business:
                reviews = [business.reviews.serialize() for review in business.reviews]
                response = {'business': business.serialize(),
                            'number_of_reviews': len(business.reviews),
                            'reviews': reviews
                }
                return jsonify(response), 200
            return self.generate_response(messages['not_found'], 404)


business_view = BusinessManipulation.as_view('businesses')
biz.add_url_rule('', defaults={'business_id':None}, view_func=business_view, methods=['GET',])
biz.add_url_rule('', view_func=business_view, methods=['POST',])
biz.add_url_rule('/<int:business_id>', view_func=business_view, methods=['GET', 'PUT', 'DELETE'])
biz.add_url_rule('/<int:business_id>/reviews', view_func=business_view,
                 methods=['GET'])
