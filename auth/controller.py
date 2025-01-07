from flask import Blueprint, request, jsonify
from auth.service import *
auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    return auth_service.signup(email, password)
@auth_bp.route('/signin', methods=['POST'])
def signin():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    return auth_service.signin(email, password)

@auth_bp.route('/signout', methods=['POST'])
def signout():
    request_data = request.get_json()
    email = request_data['email']
    return auth_service.signout(email)
