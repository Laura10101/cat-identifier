from flask import Blueprint, request, current_app as app
from .services import PredictionService
from base64 import b64encode

#Blueprint Configuration
prediction_bp = Blueprint(
    'prediction_bp',
    __name__
)

TRUE = "true"

#this is the API method to create a new prediction in the database 
@prediction_bp.route('/', methods=['POST'])
def create_prediction():
    try:
        #create an instance of the prediction service
        service  = PredictionService()
        #get the image as base64
        image = request.files["image"]
        
        #validate that the file that has been provided is an image file 
        if image.filename == "" or not image or not is_allowed_extension(image.filename):
            raise Exception("A valid .png or .jpg image must be provided when posting a training image")

        #use the service layer to make the prediction and store it in the database
        #getting the resulting id and predicted label back
        prediction_id, label = service.create_prediction(b64encode(image.read()))
        #return the created id along with a success code
        return { "id" : prediction_id, "phenotype": label }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#create API method to set user feedback on a prediction 
@prediction_bp.route('/<id>/user-feedback', methods=['POST'])
def set_user_feedback(id):
    try:
        #get predictions service
        service  = PredictionService()
        #get user feedback out of the http request
        user_feedback = request.form.get("user_feedback") == TRUE
        #use the prediction service to update the prediction with the users feedback 
        service.set_user_feedback(id, user_feedback)
        #return the success response
        return { }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#create API method to set admin feedback on a prediction 
@prediction_bp.route('/<id>/admin-feedback', methods=['POST'])
def set_admin_feedback(id):
    try:
        #get predictions service
        service  = PredictionService()
        #get admin feedback out of the http request
        admin_feedback = request.form.get("admin_feedback") == TRUE
        #use the prediction service to update the prediction with the admins feedback 
        service.set_admin_feedback(id, admin_feedback)
        #return the success response
        return { }, 200
    except Exception as e:
        return { "error": str(e) }, 400


#create awaiting admin review API method 
@prediction_bp.route('/awaiting-admin-review', methods=['GET'])
def get_awaiting_admin_review_predictions():
    try:
        service = PredictionService()
        #retrieve outstanding predictions using the service layer 
        predictions = [prediction.serialize() for prediction in service.get_awaiting_admin_review_predictions()]
        #return the success response
        return { "predictions": predictions }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#create API method to post a new cat identifier model
@prediction_bp.route('/model', methods=['POST'])
def create_prediction_model():
    try:
        service = PredictionService()
        #retrieve the JSON data
        serialised_model = request.get_json()
        id = service.create_prediction_model(serialised_model)
        return { "id": id }, 200
    except Exception as e:
        return { "error": str(e) }, 400

### HELPER METHODS ###
def is_allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in { "png", "jpg" }
