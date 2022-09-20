from flask import Blueprint, request, current_app as app

#Blueprint Configuration
user_bp = Blueprint(
    'user_bp',
    __name__
)