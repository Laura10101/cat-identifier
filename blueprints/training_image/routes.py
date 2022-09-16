from flask import Blueprint, request, current_app as app
from .services import TrainingImageService
from werkzeug.utils import secure_filename
import os


#Blueprint Configuration
training_image_bp = Blueprint(
    'training_image_bp',
    __name__
)

UPLOAD_PATH = "/tmp/uploads/"

@training_image_bp.route('/', methods=['POST'])
def post_training_image():
    try:
        service  = TrainingImageService()
        image = request.files["image"]

        if image.filename == "" or not image or not is_allowed_extension(image.filename):
            raise Exception("A valid .png or .jpg image must be provided when posting a training image")

        image_id = service.create_training_image(image_file=image)
        return { "id" : image_id }, 200
    except Exception as e:
        return { "error": str(e) }, 400

### GET UNLABELLED TRAINING IMAGES ###
@training_image_bp.route('/', methods=['GET'])
def get_unlabelled_training_images():
    try:
        service = TrainingImageService()
        images = [image.serialize() for image in service.get_unlabelled_images()]
        return { "images": images }, 200
    except Exception as e:
        return { "error": str(e) }, 400

### HELPER FUNCTIONS ###

def is_allowed_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in { "png", "jpg" }