"""Contains views to register, login and logout user"""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from app.models import User

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
