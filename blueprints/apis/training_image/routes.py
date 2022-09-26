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

#routing for the upload images from zip service
@training_image_bp.route('/zip', methods=['POST'])
def upload_images_from_zip():
    try:
        temp_file_path = "C:\\temp"
        #save zip file to hard drive from http request
        service  = TrainingImageService()
        zip_file = request.files["zip_file"]

        if zip_file.filename == "" or not zip_file or not is_zip_file(zip_file.filename):
            raise Exception("A valid .zip file must be provided when bulk importing training images")
        
        file_path = os.path.join(temp_file_path, secure_filename(zip_file.filename))
        zip_file.save(file_path)
        #call service layer to process zip file
        processed_images, ignored_files = service.upload_images_from_zip(file_path)
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