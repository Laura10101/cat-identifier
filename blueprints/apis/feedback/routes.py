from flask import Blueprint, request, current_app as app

#Blueprint Configuration
feedback_bp = Blueprint(
    'feedback_bp',
    __name__
)