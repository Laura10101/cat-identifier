import traceback
from flask import Blueprint, request, current_app as app
from base64 import b64encode, b64decode
from io import BytesIO
from zipfile import ZipFile, BadZipFile
from .data import TrainingImageRepository, TrainingLogRepository, PredictionAPIClient
from .services import TrainingImageService

#Blueprint Configuration
training_image_bp = Blueprint(
    'training_image_bp',
    __name__
)

service = None

#factory method to create and configure
#a training image service instance
def get_service():
    if service is None:
        repo = TrainingImageRepository(app.config)
        log_repo = TrainingLogRepository(app.config)
        prediction_api = PredictionAPIClient(app.config)
        globals()["service"] = TrainingImageService(app.config, repo, log_repo, prediction_api)
    return service

#Ping endpoint used to test connections to the API
@training_image_bp.route('/ping', methods=["GET"])
def ping():
    return {}, 200

@training_image_bp.route('/', methods=['POST'])
def post_training_image():
    try:
        image = request.files["image"]

        if image.filename == "" or not image or not is_allowed_extension(image.filename):
            raise Exception("A valid .png or .jpg image must be provided when posting a training image")

        image_id = get_service().create_training_image(image_file=b64encode(image.read()))
        return { "id" : image_id }, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": str(e) }, 400

#GET UNLABELLED TRAINING IMAGES
@training_image_bp.route('/unlabelled', methods=['GET'])
def get_unlabelled_training_images():
    try:
        if "query" in request.args:
            source_query = request.args["query"]
        else:
            source_query = None

        images = [image.serialize() for image in get_service().get_unlabelled_images(source_query=source_query)]
        return { "images": images }, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": str(e) }, 400

#routing for the set image label service
@training_image_bp.route('/labels', methods=['POST'])
def set_image_labels():
    #set up try/except clauses to handle happy path and exceptional paths
    try:
        label = request.json["label"]
        is_cat = label["is_cat"]
        colour = label["colour"]
        is_tabby = label["is_tabby"]
        pattern = label["pattern"]
        is_pointed = label["is_pointed"]
        for id in request.json["ids"]:
            get_service().set_image_label(id, is_cat, colour, is_tabby, pattern, is_pointed)
        return {}, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": str(e) }, 400

#routing for the upload images from zip service
@training_image_bp.route('/zip', methods=['POST'])
def upload_images_from_zip():
    try:
        error_txt = "A valid .zip file must be provided when bulk importing training images"

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
            app.logger.error(traceback.print_exc())
            raise Exception(error_txt)

        #call service layer to process zip file
        processed_images, ignored_files = get_service().upload_images_from_zip(zip_file)
        return { "training_images": processed_images, "ignored": ignored_files }
    except Exception as e:
        return { "error": str(e) }, 400

#routing for the image search service
@training_image_bp.route('/search', methods=['GET'])
def get_image_urls_from_search():
    try:
        #get query parameters
        query = request.args['query']
        count = request.args.get("count", default=1000, type=int)
        start_at = request.args.get("start_at", default=0, type=int)
        return { "image_urls": get_service().get_image_urls_from_search(query, count, start_at) }, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": str(e) }, 400

#routing for the import images from urls service
@training_image_bp.route('/import', methods=['POST'])
def import_images_from_url():
    try:
        #get list of urls out of http request
        if "image_urls" not in request.json:
            raise Exception("A list of images must be provided as part of an import.")
        image_urls = request.json["image_urls"]
        # get the query that generated the url list
        if "query" not in request.json:
            raise Exception("An import must include the query from which the images were selected.")
        query = request.json["query"]
        #import images using the service layer 
        image_ids = get_service().import_images_from_url(image_urls, query)
        #return success code
        return { "training_images": image_ids }, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": str(e) }, 400

# routing for the get training image snapshot service
@training_image_bp.route('/snapshot', methods=['GET'])
def get_training_images_snapshot():
    try:
        snapshot = get_service().get_training_images_snapshot()
        return { "snapshot": snapshot }, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": str(e) }, 500

#routing for the train new model service
@training_image_bp.route('/model', methods=['POST'])
def train_new_model():
    try:
        #run the training service
        app.celery.send_task("training_tasks.train_model",args=[])
        return {}, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": str(e) }, 400

#routing for the read log service
@training_image_bp.route("/model/log", methods=["GET"])
def read_log():
    try:
        #retrieve the log entries
        entries = get_service().read_log()
        #serialise to a list
        serialised_entries = []
        for entry in entries:
            serialised_entries.append(entry.as_str())
        return { "entries": serialised_entries }, 200
    except Exception as e:
        app.logger.error(traceback.print_exc())
        return { "error": str(e) }, 400

### HELPER FUNCTIONS ###

def is_allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in { "png", "jpg", "jfif" }

def is_zip_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in { "zip" }