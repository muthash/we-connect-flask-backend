"""Contains views to search for businesses"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_optional
from app.models import Business
from app.utils import check_missing_field, filter_business
from app.base_view import BaseView

search = Blueprint('search', __name__, url_prefix='/api/v1/search')


class SearchManipulation(BaseView):
    """Method to manipulate business endpoints"""
    @jwt_optional
    def get(self):
        category = request.args.get('cat', "", type=str)
        location = request.args.get('loc', "", type=str)
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        search = request.args.get('q', "", type=str)
        data = {'search_parameter': search}

        if check_missing_field(**data):
            return jsonify(check_missing_field(**data)), 422
        business = Business.query.filter(
                   Business.name.ilike('%' + search + '%')
                   ).paginate(page, limit, False)
        if not business.items:
            response = {'message': f'The search for {search} did ' +
                        'not match any business'}
            return jsonify(response), 200
        if category or location:
            return filter_business(business, category=category,
                                   location=location)
        businesses = [biz.serialize() for biz in business.items]
        response = {'businesses': businesses}
        return jsonify(response), 200


search_view = SearchManipulation.as_view('search')
search.add_url_rule('', view_func=search_view, methods=['GET'])
