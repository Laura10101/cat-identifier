import io
from flask import Blueprint, request, current_app as app
from .services import PredictionService
from .data import PredictionModelRepository, PredictionRepository
from base64 import b64encode, b64decode
from PIL import Image

#Blueprint Configuration
prediction_bp = Blueprint(
    'prediction_bp',
    __name__
)

TRUE = "true"

#Initialise the prediction and prediction model repos, and prediction service
prediction_repo = PredictionRepository()
prediction_model_repo = PredictionModelRepository()
prediction_service = PredictionService(prediction_repo, prediction_model_repo)

#Ping endpoint used to test connections to the API
@prediction_bp.route('/ping', methods=["GET"])
def ping():
    return {}, 200

#this is the API method to check if a model exists
@prediction_bp.route('/model/latest', methods=["GET"])
def get_active_model():
    try:
        #get the latest model from the prediction service
        model = prediction_service.get_active_model()

        #if no model is returned, return a 404 (resource not found)
        if model is None:
            return {}, 404

        #otherwise, remove sensitive attributes from the serialized model
        serialized_model = model.serialize()
        del serialized_model["_id"]
        del serialized_model["model"]
        del serialized_model["weights"]
        return { "model": serialized_model }, 200
        
    except Exception as e:
        return { "error": str(e) }, 400

#this is the API method to create a new prediction in the database 
@prediction_bp.route('/', methods=['POST'])
def create_prediction():
    try:
        #get the image data (which is expected to be base64)
        image = request.json["image"]     
        
        #check that the file is a valid image
        #taken from StackOverflow: https://stackoverflow.com/questions/60186924/python-is-base64-data-a-valid-image
        try:
            img = Image.open(io.BytesIO(b64decode(image)))
        except Exception:
            raise Exception('File is not valid base64 image')

        if not img.format.lower() in ["png", "jpeg", "jpg", "jfif"]:
            raise Exception("File is not a valid JPEG or PNG")

        #use the service layer to make the prediction and store it in the database
        #getting the resulting id and predicted label back
        prediction_id, label = prediction_service.create_prediction(image)
        #return the created id along with a success code
        return { "id" : prediction_id, "label": label }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#create API method to set user feedback on a prediction 
@prediction_bp.route('/<id>/user-feedback', methods=['POST'])
def set_user_feedback(id):
    try:
        #get user feedback out of the http request
        user_feedback = request.json["user_feedback"]
        #use the prediction service to update the prediction with the users feedback 
        prediction_service.set_user_feedback(id, user_feedback)
        #return the success response
        return { }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#create API method to set admin feedback on a prediction 
@prediction_bp.route('/<id>/admin-feedback', methods=['POST'])
def set_admin_feedback(id):
    try:
        #get admin feedback out of the http request
        admin_feedback = request.form.get("admin_feedback") == TRUE
        #use the prediction service to update the prediction with the admins feedback 
        prediction_service.set_admin_feedback(id, admin_feedback)
        #return the success response
        return { }, 200
    except Exception as e:
        return { "error": str(e) }, 400


#create awaiting admin review API method 
@prediction_bp.route('/awaiting-admin-review', methods=['GET'])
def get_awaiting_admin_review_predictions():
    try:
        #retrieve outstanding predictions using the service layer 
        predictions = [prediction.serialize() for prediction in prediction_service.get_awaiting_admin_review_predictions()]
        #return the success response
        return { "predictions": predictions }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#create API method to post a new cat identifier model
@prediction_bp.route('/model', methods=['POST'])
def create_prediction_model():
    try:
        #retrieve the JSON data
        serialised_model = request.get_json()
        id = prediction_service.create_prediction_model(serialised_model)
        return { "id": id }, 200
    except Exception as e:
        return { "error": str(e) }, 400

### HELPER METHODS ###
def is_allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in { "png", "jpg" }
