import traceback
from flask import Blueprint, request, current_app as app
from werkzeug.security import generate_password_hash
from .data import UserRepository
from .services import UserService

#Blueprint Configuration
user_bp = Blueprint(
    'user_bp',
    __name__
)

service = None

#factory method to create and configure
#a user service
def get_service():
    if service is None:
        repo = UserRepository(app.config)
        globals()["service"] = UserService(repo)
    return service

#Ping endpoint used to test connections to the API
@user_bp.route('/ping', methods=["GET"])
def ping():
    return {}, 200

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        username = request.json["username"]
        password = request.json["password"]
        token = get_service().login(username, password)
        if token == None:
            return { "error": "Unrecognised username and/or password" }, 401
        return { "token": token }, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": "Unrecognised username and/or password"}, 401

@user_bp.route('/authorize', methods=['POST'])
def authorize():
    try:
        username = request.json["username"]
        token = request.json["token"]
        token = get_service().authorize(username, token)
        if token == None:
            return { "error": "User authorization failed"}, 401
        return { "token": token }, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": "User authorization failed"}, 401

@user_bp.route('/', methods=['POST'])
def register():
    try:
        username = request.json["username"]
        password = generate_password_hash(request.json["password"])
        get_service().register_user(username, password)
        return {}, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": str(e) }, 400