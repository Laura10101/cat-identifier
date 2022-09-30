from flask import Blueprint, request, current_app as app
from werkzeug.security import generate_password_hash
from .services import UserService

#Blueprint Configuration
user_bp = Blueprint(
    'user_bp',
    __name__
)

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        username = request.json["username"]
        password = request.json["password"]
        service = UserService()
        token = service.login(username, password)
        if token == None:
            return { "error": "Unrecognised username and/or password" }, 401
        return { "token": token }, 200
    except Exception as e:
        return { "error": "Unrecognised username and/or password"}, 401

@user_bp.route('/authorize', methods=['POST'])
def authorize():
    try:
        username = request.json["username"]
        token = request.json["token"]
        service = UserService()
        token = service.authorize(username, token)
        if token == None:
            return { "error": "User authorization failed"}, 401
        return { "token": token }, 200
    except Exception as e:
        return { "error": "User authorization failed"}, 401

@user_bp.route('/', methods=['POST'])
def register():
    try:
        username = request.json["username"]
        password = generate_password_hash(request.json["password"])
        service = UserService()
        service.register_user(username, password)
        return {}, 200
    except Exception as e:
        return { "error": str(e) }, 400