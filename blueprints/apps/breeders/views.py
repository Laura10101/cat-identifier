from flask import Blueprint, render_template, request, current_app as app

#Blueprint Configuration
breeders_bp = Blueprint(
    'breeders_bp',
    __name__,
    template_folder="templates",
    static_folder="static"
)

@breeders_bp.route("/", methods=["GET"])
def upload_image():
    return render_template("upload-cat-image.html")

@breeders_bp.route("/results", methods=["POST"])
def get_results():
    return render_template("results.html")

@breeders_bp.route("/thankyou", methods=["POST"])
def thankyou():
    return render_template("thankyou.html")