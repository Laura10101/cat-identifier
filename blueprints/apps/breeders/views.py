from flask import Blueprint, flash, url_for, redirect, render_template, request, current_app as app
from base64 import b64encode
from requests import get

#Blueprint Configuration
breeders_bp = Blueprint(
    'breeders_bp',
    __name__,
    template_folder="templates",
    static_folder="static"
)

@breeders_bp.route("/", methods=["GET"])
def upload_image():
    if model_exists():
        return render_template("upload-cat-image.html")
    else:
        return render_template("model-not-ready.html")

@breeders_bp.route("/results", methods=["POST"])
def get_results():
    #Get the image file as b64 from the http request
    image = request.files["image"]
    
    #validate that the file that has been provided is an image file
    extension = get_extension(image.filename)
    if extension in ["jpg", "jpeg", "jfif"]:
        encoding = "image/jpeg"

    elif extension in ["png"]:
        encoding = "image/png"

    else:
        flash("A valid .png or .jpg image must be provided when posting a training image")
        return redirect(url_for("breeders_bp.upload_image"), code=302)

    b64_image = b64encode(image.read()).decode()
    b64_image_src = "data:" + encoding + "; base64," + b64_image
        
    return render_template("results.html", b64_image=b64_image, b64_image_src=b64_image_src)

@breeders_bp.route("/thankyou", methods=["POST"])
def thankyou():
    id = request.form["prediction_id"]
    feedback = request.form["feedback"]
    return render_template("thankyou.html", id=id, feedback=str(feedback).lower())

### HELPER METHODS ###
def get_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    else:
        return ""

def model_exists():
    endpoint = app.config["API_BASE_URL"] + "/predictions/model/latest"
    response = get(endpoint)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception(response.json()["error"])
