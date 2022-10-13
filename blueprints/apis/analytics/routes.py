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
            service.create_training_images_snapshot(
                summary["is_unlabelled"],
                summary["is_cat"],
                summary["colour"],
                summary["is_tabby"],
                summary["pattern"],
                summary["is_pointed"],
                summary["source"],
                summary["count"]
            )

        return {}, 201
    except Exception as e:
        return { "error": str(e) }, 400

#Create endpoint to post a snapshot of prediction data
@analytics_bp.route('/snapshots/predictions', methods=["POST"])
def post_predictions_snapshot():
    try:
        summaries = request.json["summaries"]
        for summary in summaries:
            validate_label(**summary)

            if not "user_review_status" in summary:
                raise Exception("Attribute user_review_status is missing from summary")

            if not "admin_review_status" in summary:
                raise Exception("Attribute admin_review_status is missing from summary")

            if "count" not in summary:
                raise Exception("Missing count from training image snapshot")
            
            service.create_predictions_snapshot(
                summary["is_unlabelled"],
                summary["is_cat"],
                summary["colour"],
                summary["is_tabby"],
                summary["pattern"],
                summary["is_pointed"],
                summary["user_review_status"],
                summary["admin_review_status"],
                summary["count"]
            )

        return {}, 201
    except Exception as e:
        return { "error": str(e) }, 400

#Create endpoint to post a snapshot of prediction model data
@analytics_bp.route('/snapshots/prediction-models')
def post_prediction_models_snapshot():
    try:
        expected_args = [
                "training_started", "training_ended", "min_accuracy", "max_accuracy", "avg_accuracy",
                "min_loss", "max_loss", "avg_loss"
            ]
        summaries = request.json["summaries"]
        for summary in summaries:

            # check that all args are present
            for arg in expected_args:
                if not arg in summary:
                    raise Exception("Missing " + arg + " in model snapshot summary")

            service.create_models_snapshot(
                summary["training_started"],
                summary["training_ended"],
                summary["min_accuracy"],
                summary["max_accuracy"],
                summary["avg_accuracy"],
                summary["min_loss"],
                summary["max_loss"],
                summary["avg_loss"]
            )

        return {}, 201
    except Exception as e:
        return { "error": str(e) }, 400

# create endpoint to get size of training set by date

# create endpoint to get breakdown of training images by label

# create endpoint to get historical model performance over time

# create endpoint to get breakdown of prediction accuracy over time

# create endpoint to get breakdown of predictions by review status and date

# create endpoint to get breakdown of admin versus user acceptance of predictions

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