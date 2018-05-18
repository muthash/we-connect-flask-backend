""""Contains views to register, login reset password and logout user"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from app.models import Business, Review
from app.utils import (
    require_json, check_missing_field, messages, remove_more_spaces)
from app.base_view import BaseView

rev = Blueprint('rev', __name__,
                url_prefix='/api/v1/businesses/<int:business_id>/reviews')


class ReviewManipulation(BaseView):
    """Method to manipulate business endpoints"""
    @jwt_required
    @require_json
    def post(self, business_id):
        """Endpoint to save the data to the database"""
        data = request.get_json()
        description = data.get('description')
        rating = data.get('rating')
        current_user = get_jwt_identity()

        data = dict(description=description, rating=rating)
        if check_missing_field(**data):
            return jsonify(check_missing_field(**data)), 422

        description = remove_more_spaces(description)
        business = Business.query.filter_by(id=business_id).first()
        if business.user_id == current_user:
            response = {'message': 'The operation is forbidden for' +
                                   ' own business'}
            return jsonify(response), 403

        review = Review(description, rating, business_id, current_user)
        review.save()
        response = {'message': 'Review for business with id' +
                               f' {business_id} created'}
        return jsonify(response), 201


review_view = ReviewManipulation.as_view('reviews')
rev.add_url_rule('', view_func=review_view, methods=['POST'])
