from flask import Blueprint, current_app as app


#Blueprint Configuration
training_image_bp = Blueprint(
    'training_image_bp',
    __name__
)


@training_image_bp.route('/', methods=['POST'])
def post_training_image():
    return "Post request received"