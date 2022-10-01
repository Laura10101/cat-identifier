from flask import Blueprint, flash, url_for, render_template, request, session, redirect
from flask import current_app as app
from .data import *

#Blueprint Configuration
admin_bp = Blueprint(
    'admin_bp',
    __name__,
    template_folder="templates",
    static_folder="static"
)

#Create a client for each API required by the admin app
user_client = UserClient(app.config["api_base_url"])

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

    return render_template("home.html")

@admin_bp.route("/training-images/upload")
def upload_images():
    pass

@admin_bp.route("/training-images/import")
def import_images():
    pass

@admin_bp.route("/training-images/label")
def label_images():
    return "Hello World"

@admin_bp.route("/training/start")
def start_training():
    pass

@admin_bp.route("/training/status")
def check_training_status():
    pass

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

    return render_template("add-user.html", user_step=8)


@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():
    pass

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