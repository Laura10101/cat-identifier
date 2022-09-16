from flask import Blueprint, request, current_app as app

#Blueprint Configuration
reporting_bp = Blueprint(
    'reporting_bp',
    __name__
)