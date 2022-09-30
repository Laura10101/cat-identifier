from flask import Blueprint, request, current_app as app

#Blueprint Configuration
breeders_bp = Blueprint(
    'breeders_bp',
    __name__,
    template_folder="templates"
)