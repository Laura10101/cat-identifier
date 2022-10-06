import traceback
from flask import Blueprint, request, current_app as app
from .services import AnalyticsService

#Blueprint Configuration
analytics_bp = Blueprint(
    'analytics_bp',
    __name__
)

#factory method to create and configure
#a training image service instance
def make_service():
    return AnalyticsService(app.config)

#global user service instance
service = make_service()

#Ping endpoint used to test connections to the API
@analytics_bp.route('/ping', methods=["GET"])
def ping():
    return {}, 200
