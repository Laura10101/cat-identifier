from flask import Blueprint, request, current_app as app

#Blueprint Configuration
prediction_bp = Blueprint(
    'prediction_bp',
    __name__
)