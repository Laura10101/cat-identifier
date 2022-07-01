from flask import Blueprint, request, current_app as app
from .services import TrainingImageService


#Blueprint Configuration
training_image_bp = Blueprint(
    'training_image_bp',
    __name__
)


@training_image_bp.route('/', methods=['POST'])
def post_training_image():
    try:
        service  = TrainingImageService()
        image = request.files["image"]
        id = service.create_training_image(image=image)
        return { "id" : id }, 200
    except Exception as e:
        return { "error": str(e) }, 400

