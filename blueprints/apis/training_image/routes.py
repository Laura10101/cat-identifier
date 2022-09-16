from flask import Blueprint, request, current_app as app
from .services import TrainingImageService
from base64 import b64encode
from werkzeug.utils import secure_filename
import os


#Blueprint Configuration
training_image_bp = Blueprint(
    'training_image_bp',
    __name__
)

UPLOAD_PATH = "/tmp/uploads/"
TRUE = "true"

@training_image_bp.route('/', methods=['POST'])
def post_training_image():
    try:
        service  = TrainingImageService()
        image = request.files["image"]

        if image.filename == "" or not image or not is_allowed_extension(image.filename):
            raise Exception("A valid .png or .jpg image must be provided when posting a training image")

        image_id = service.create_training_image(image_file=b64encode(image.read()))
        return { "id" : image_id }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#GET UNLABELLED TRAINING IMAGES
@training_image_bp.route('/unlabelled', methods=['GET'])
def get_unlabelled_training_images():
    try:
        service = TrainingImageService()
        images = [image.serialize() for image in service.get_unlabelled_images()]
        return { "images": images }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#routing for the set image label service
@training_image_bp.route('/<id>/label', methods=['POST'])
def set_image_label(id):
    #set up try/except clauses to handle happy path and exceptional paths
    try: 
        service = TrainingImageService() 
        is_cat = request.form.get("is_cat") == TRUE
        colour = request.form.get("colour")
        is_tabby = request.form.get("is_tabby") == TRUE
        pattern = request.form.get("pattern")
        is_pointed = request.form.get("is_pointed") == TRUE
        service.set_image_label(id, is_cat, colour, is_tabby, pattern, is_pointed)
        return {}, 200
    except Exception as e:
        return { "error": str(e) }, 400

### HELPER FUNCTIONS ###

def is_allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in { "png", "jpg" }