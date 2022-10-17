import traceback
from flask import Blueprint, request, current_app as app
from .services import AnalyticsService

#Blueprint Configuration
analytics_bp = Blueprint(
    'analytics_bp',
    __name__
)

service = None
#factory method to create and configure
#a training image service instance
def get_service():
    if service is None:
        globals()["service"] = AnalyticsService(app.config)
    return service

#Ping endpoint used to test connections to the API
@analytics_bp.route('/ping', methods=["GET"])
def ping():
    return {}, 200

# check whether the daily snapshot has been posted
@analytics_bp.route('/snapshots/today/exists', methods=["GET"])
def check_daily_snapshot_posted():
    try:
        return { "snapshot_posted": get_service().snapshot_posted_today() }, 200
    except Exception as e:
        return { "error": str(e) }, 500

#Create endpoint to post a snapshot of training image data
@analytics_bp.route('/snapshots/training-images', methods=["POST"])
def post_training_image_snapshot():
    try:
        # one snapshot may comprise several rows as each
        # row in a fact table represents a single permutation of
        # the dimensions in that table
        snapshot = request.json["snapshot"]
        for summary in snapshot:
            validate_label(**summary)

            if "source" not in summary:
                raise Exception("Missing training image source from training image snapshot")

            if "count" not in summary:
                raise Exception("Missing count from training image snapshot")

        # create the snapshot
        get_service().create_training_images_snapshot(snapshot)

        return {}, 201
    except Exception as e:
        return { "error": str(e) }, 400

#Create endpoint to post a snapshot of prediction data
@analytics_bp.route('/snapshots/predictions', methods=["POST"])
def post_predictions_snapshot():
    try:
        snapshot = request.json["snapshot"]
        for summary in snapshot:
            validate_label(**summary)

            if not "user_review_status" in summary:
                raise Exception("Attribute user_review_status is missing from summary")

            if not "admin_review_status" in summary:
                raise Exception("Attribute admin_review_status is missing from summary")

            if "count" not in summary:
                raise Exception("Missing count from training image snapshot")
            
        get_service().create_predictions_snapshot(snapshot)

        return {}, 201
    except Exception as e:
        return { "error": str(e) }, 400

#Create endpoint to post a snapshot of prediction model data
@analytics_bp.route('/snapshots/prediction-models', methods=["POST"])
def post_prediction_models_snapshot():
    try:
        expected_args = [
                "training_started", "training_ended", "min_accuracy", "max_accuracy", "avg_accuracy",
                "min_loss", "max_loss", "avg_loss"
            ]
        snapshot = request.json["snapshot"]
        for summary in snapshot:

            # check that all args are present
            for arg in expected_args:
                if not arg in summary:
                    raise Exception("Missing " + arg + " in model snapshot summary")

        get_service().create_models_snapshot(snapshot)

        return {}, 201
    except Exception as e:
        return { "error": str(e) }, 400

# create endpoint to get training set analytics
@analytics_bp.route("/training-images")
def get_training_image_summary():
    try:
        return { "data": get_service().get_training_set_stats() }, 200
    except Exception as e:
        return { "error": str(e) }, 400

# create endpoint to get prediction metrics
@analytics_bp.route("/predictions")
def get_prediction_summary():
    try:
        return { "data": get_service().get_prediction_stats() }, 200
    except Exception as e:
        return { "error": str(e) }, 400

# create endpoint to get model metrics
@analytics_bp.route("/models")
def get_model_summary():
    try:
        return { "data": get_service().get_model_stats() }, 200
    except Exception as e:
        return { "error": str(e) }, 400

### HELPER FUNCTIONS ###
def validate_label(**kwargs):
    expected_args = ["is_unlabelled", "is_cat", "colour", "is_tabby", "pattern", "is_pointed"]

    # all expected args should be present
    for arg in expected_args:
        if not arg in kwargs:
            raise Exception("Label is missing attribute: " + arg)

    # if a cat is unlabelled, then all other args should be null
    if kwargs["is_unlabelled"]:
        for arg in expected_args[1:]:
            if not kwargs[arg] is None and not kwargs[arg] == False:
                raise Exception("Unlabelled image cannot have value for " + arg)

    # if no exception has been thrown yet, validation has passed
    return True