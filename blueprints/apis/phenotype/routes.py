from flask import Blueprint, request, current_app as app

#Blueprint Configuration
phenotype_bp = Blueprint(
    'phenotype_bp',
    __name__
)