from flask import Blueprint, request, current_app as app
from .services import TrainingImageService
from base64 import b64encode, b64decode
from io import BytesIO
from zipfile import ZipFile, BadZipFile
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
@training_image_bp.route('/labels', methods=['POST'])
def set_image_labels():
    #set up try/except clauses to handle happy path and exceptional paths
    try:
        service = TrainingImageService()
        label = request.json["label"]
        is_cat = label["is_cat"]
        colour = label["colour"]
        is_tabby = label["is_tabby"]
        pattern = label["pattern"]
        is_pointed = label["is_pointed"]
        for id in request.json["ids"]:
            service.set_image_label(id, is_cat, colour, is_tabby, pattern, is_pointed)
        return {}, 200
    except Exception as e:
        return { "error": str(e) }, 400

#routing for the upload images from zip service
@training_image_bp.route('/zip', methods=['POST'])
def upload_images_from_zip():
    try:
        error_txt = "A valid .zip file must be provided when bulk importing training images"
        service  = TrainingImageService()

        #check to see if a zip file part was included in the request
        if not "zip_file" in request.json:
            raise Exception(error_txt)

        #decode the zip file data into a bytes object
        b64_zip_data = request.json["zip_file"]
        zip_bytes = b64decode(b64_zip_data)

        #check to ensure that this is actually a zip file
        try:
            zip_file = ZipFile(BytesIO(zip_bytes))
        except BadZipFile:
            raise Exception(error_txt)

        #call service layer to process zip file
        processed_images, ignored_files = service.upload_images_from_zip(zip_file)
        return { "training_images": processed_images, "ignored": ignored_files }
    except Exception as e:
        return { "error": str(e) }, 400

#routing for the image search service
@training_image_bp.route('/search', methods=['GET'])
def get_image_urls_from_search():
    try:
        #create instance of the TrainingImageService
        service = TrainingImageService()
        #get query parameters
        query = request.args['query']
        count = request.args.get("count", default=1000, type=int)
        start_at = request.args.get("start_at", default=0, type=int)
        return { "image_urls": service.get_image_urls_from_search(query, count, start_at) }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#routing for the import images from urls service
@training_image_bp.route('/import', methods=['POST'])
def import_images_from_url():
    try:
        #get list of urls out of http request
        image_urls = request.json["image_urls"]
        #import images using the service layer 
        service = TrainingImageService()
        image_ids = service.import_images_from_url(image_urls)
        #return success code
        return { "training_images": image_ids }, 200
    except Exception as e:
        return { "error": str(e) }, 400

#routing for the train new model service
@training_image_bp.route('/model', methods=['POST'])
def train_new_model():
    try:
        #run the training service
        service = TrainingImageService()
        service.train_new_model()
        return {}, 200
    except Exception as e:
        return { "error": str(e) }, 400

### HELPER FUNCTIONS ###

def is_allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in { "png", "jpg", "jfif" }

def is_zip_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in { "zip" }