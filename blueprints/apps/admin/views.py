from flask import Blueprint, flash, url_for, render_template, request, session, redirect
from flask import current_app as app
from json import dumps
from base64 import b64encode
from .data import *

#Blueprint Configuration
admin_bp = Blueprint(
    'admin_bp',
    __name__,
    template_folder="templates",
    static_folder="static"
)

#Create a client for each API required by the admin app
user_client = UserClient(app.config["API_BASE_URL"])

#View routes
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    #Check whether to display the login form...
    if request.method == "GET":
        return render_template("login.html")

    #Get the username and password from the request
    username = request.form.get("username")
    password = request.form.get("password")

    #Otherwise, perform the login action
    token = user_client.authenticate_user(username, password)

    #If the token is null, login failed so take the user back
    #to the login page
    if token == None:
        flash("Invalid username/password. Please try again...")
        return render_template("login.html")

    #Otherwise, set the session with the token and username
    #and redirect the user to the home page
    session["token"] = token
    session["username"] = username
    return redirect(url_for("admin_bp.home"), code=302)

@admin_bp.route("/")
def home():
    authorization_response = authorize_user()
    if not authorization_response is None:
        return authorization_response

    return render_template("home.html", title="Welcome to the admin portal")

@admin_bp.route("/training-images/upload", methods=["GET", "POST"])
def upload_images():
    #check that the user is logged in and, if they are not
    #redirect them to the login page
    authorization_response = authorize_user()
    if not authorization_response is None:
        return authorization_response

    #check whether the admin has submitted the form or not
    #if not, display the form to them
    if request.method == "GET":
        return render_template("upload-images.html", title="Upload training images")

    #otherwise:
    #check that a file part exists in the provided request
    if "file" not in request.files:
        flash("You must provide a valid Zip file to import training images from.")
        return render_template("upload-images.html", title="Upload training images")

    #check that a file has been provided and that it is a zip file
    file = request.files["file"]
    if file.filename == "" or not is_zip_file(file.filename):
        flash("You must provide a valid Zip file to import training images from.")
        return render_template("upload-images.html", title="Upload training images")

    #convert the file to base64
    b64_zip = b64encode(file.read())
    #send the data to the confirmation page to perform the action and display the result
    return render_template("confirm-upload.html", b64_zip_data=b64_zip.decode(), title="Training image upload results")

@admin_bp.route("/training-images/import", methods=["GET", "POST"])
def import_images():
    #check that the user is logged in and, if they are not
    #redirect them to the login page
    authorization_response = authorize_user()
    if not authorization_response is None:
        return authorization_response

    #if this is a GET request and no query exists
    #then direct the user to retrieve the query
    if request.method == "GET" and not "query" in request.args:
        return render_template("search-images.html", title="Search for training images")

    #for other get requests, route the user to select which
    #images to import
    elif request.method == "GET":
        return render_template("select-images.html", query=request.args["query"], title="Select training images for import")

    #otherwise, assume the user is at the import stage
    else:
        #build the list of urls to be imported
        url_list = get_ids_to_process(request.form, [])
        # get the query
        query = request.form["query"]

        return render_template("confirm-import.html", url_list=dumps(url_list), title="Import training images", query=query)

@admin_bp.route("/training-images/label", methods=["GET", "POST"])
def label_images():
    #check that the user is logged in and, if they are not
    #redirect them to the login page
    authorization_response = authorize_user()
    if not authorization_response is None:
        return authorization_response

    #if the request is a get, display the form
    if request.method == "GET":
        return render_template("label-images.html", title="Label training images")

    #check if image is a cat
    if "is_cat" in request.form:
        is_cat = request.form["is_cat"] == "on"
    else:
        is_cat = False

    # validate colour attribute of label
    if not "colour" in request.form:
        if is_cat:
            flash("Please provide a valid colour for the label")
            return render_template("label-images.html", title="Label training images")
        else:
            colour = None
    else:
        colour = request.form["colour"]
        if colour == "":
            if is_cat:
                flash("Please provide a valid colour for the label")
                return render_template("label-images.html", title="Label training images")
            else:
                colour = None
        else:
            if not is_cat:
                flash("Please leave the colour box blank for non-cat labels")
                return render_template("label-images.html", title="Label training images")

    # validate the is_tabby attribute of the label
    if "is_tabby" in request.form:
        is_tabby = request.form["is_tabby"] == "on"
        if not is_cat and is_tabby:
            flash("Please leave the 'is tabby' box unchecked for non-cat labels")
            return render_template("label-images.html", title="Label training images")
    else:
        is_tabby = False

    #validate the pattern attribute of the label
    if not "pattern" in request.form:
        if is_cat:
            flash("Please provide a valid pattern for the label")
            return render_template("label-images.html", title="Label training images")
        else:
            pattern = None
    else:
        pattern = request.form["pattern"]
        if pattern == "":
            if is_cat:
                flash("Please provide a valid pattern for the label")
                return render_template("label-images.html", title="Label training images")
            else:
                pattern = None
        else:
            if not is_cat:
                flash("Please leave the pattern box blank for non-cat labels")
                return render_template("label-images.html", title="Label training images")

    # validate the is_pointed attribute of the cat label
    if "is_pointed" in request.form:
        is_pointed = request.form["is_pointed"] == "on"
        if not is_cat and is_pointed:
            flash("Please leave the 'is pointed' box unchecked for non-cat labels")
            return render_template("label-images.html", title="Label training images")
    else:
        is_pointed = False

    #now extract the image ids to which the label should be applied
    ignore = ["is_cat", "colour", "is_tabby", "pattern", "is_pointed"]
    id_list = get_ids_to_process(request.form, ignore)

    if len(id_list) == 0:
        flash("Please select at least one training image to apply the label to")
        return render_template("label-images.html", title="Label training images")

    #build the label dictionary
    label = {
        "is_cat": is_cat,
        "colour": colour,
        "is_tabby": is_tabby,
        "pattern": pattern,
        "is_pointed": is_pointed
    }

    return render_template("confirm-labelling.html", label=dumps(label), ids=dumps(id_list), title="Label training images")

@admin_bp.route("/training-images/clean")
def clean_training_images():
    return 200

@admin_bp.route("/training/start")
def start_training():
    #check that the user is logged in and, if they are not
    #redirect them to the login page
    authorization_response = authorize_user()
    if not authorization_response is None:
        return authorization_response

    return render_template("start-training.html", title="Start model training")

@admin_bp.route("/training/status")
def check_training_status():
    #check that the user is logged in and, if they are not
    #redirect them to the login page
    authorization_response = authorize_user()
    if not authorization_response is None:
        return authorization_response

    return render_template("check-training-status.html", title="Check training status")

@admin_bp.route("/users/add", methods=["GET", "POST"])
def add_admin_users():
    authorization_response = authorize_user()
    if not authorization_response is None:
        return authorization_response

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_reentry = request.form.get("password_reentry")

        if not password == password_reentry:
            flash("Passwords do not match. Please try again")

        else:
            result = user_client.register_user(username, password)

            if result is None:
                flash("User has been successfully added")
            else:
                flash("Error occurred while adding user: " + result)

    return render_template("add-user.html", title="Add user")

@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():
    #check that the user is logged in and, if they are not
    #redirect them to the login page
    authorization_response = authorize_user()
    if not authorization_response is None:
        return authorization_response

    return render_template("dashboard.html", title="Admin dashboards")

@admin_bp.route("/dashboard/clear", methods=["GET", "POST"])
def clear_dashboard():
    if request.method == "GET":
        return render_template("clear-dashboard.html", title="Clear analytics data")
    elif request.method == "POST":
        if "clear-training-image-analytics" in request.form:
            clear_training_image_analytics = request.form["clear-training-image-analytics"] == "on"
        else:
            clear_training_image_analytics = False

        if "clear-prediction-analytics" in request.form:
            clear_prediction_analytics = request.form["clear-prediction-analytics"] == "on"
        else:
            clear_prediction_analytics = False

        if "clear-model-analytics" in request.form:
            clear_model_analytics = request.form["clear-model-analytics"] == "on"
        else:
            clear_model_analytics = False

        return render_template(
            "confirm-clear-dashboard.html",
            title="Clear analytics data",
            clear_training_image_analytics=clear_training_image_analytics,
            clear_prediction_analytics=clear_prediction_analytics,
            clear_model_analytics=clear_model_analytics
        )

@admin_bp.route("/logout", methods=["GET"])
def logout():
    flash("You were successfully logged out")
    session.pop("username")
    session.pop("token")
    return redirect(url_for("admin_bp.login"), code=302)

#Helper functions
def authorize_user():
    #If the session variables for username or token haven't been set yet
    #then no user is logged in
    if not "username" in session.keys() or not "token" in session.keys():
        return redirect(url_for("admin_bp.login"), code=302)

    #Check the user's authorization status based on token and username
    refreshed_token = user_client.authorise_user(session["username"], session["token"])

    #If no refreshed token is returned, authorization failed
    #so clear the session cookies and redirect to the login page
    if refreshed_token is None:
        session.pop("username")
        session.pop("token")
        return redirect(url_for("admin_bp.login"), code=302)

    #Otherwise, update the session token and return None
    session["token"] = refreshed_token
    return None

#Function to check whether a file is a zip file
def is_zip_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in { "zip" }

#Function to get the identifiers to process from a training images
#grid form request
def get_ids_to_process(form_data, ignore):
    #build the list of urls to be imported
    #create empty dictionary to hold all identifiers on the form
    #and their indices
    all_ids = {}
    #create a list to hold the included indices
    indices = []
    #iterate over all form elements
    for name in form_data:
        #check whether to ignore this name or not
        if not name in ignore:
            #check if this is an id input or an included input
            if "id_" in name:
                #if an id, get the index from the name
                #which follows the underscore
                index = int(name.split("_")[1])
                #add the url to the dictionary
                all_ids[index] = request.form[name]
            elif "include_" in name:
                #if the checkbox was ticked
                #this index should be included in the list of urls
                #to be imported
                if request.form[name].lower() == "on":
                    index = int(name.split("_")[1])
                    indices.append(index)

    #once all form elements have been processed,
    #build the list of urls to be imported
    id_list = []
    for index in indices:
        id_list.append(all_ids[index])

    return id_list