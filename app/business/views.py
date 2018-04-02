"""Contains views to register, login reset password and logout user"""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.models import User,  Business
from app.utils import (
    validate_null, random_string, send_reset_password, messages
)
from app.base_view import BaseView

business = Blueprint('business', __name__, url_prefix='/api/v1/business')
