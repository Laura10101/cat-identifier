from flask import Blueprint, request, current_app as app

#Blueprint Configuration
admin_bp = Blueprint(
    'admin_bp',
    __name__
)