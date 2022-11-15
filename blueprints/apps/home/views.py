from flask import Blueprint, flash, url_for, redirect, render_template, request, current_app as app
from requests import get

# blueprint Configuration
home_bp = Blueprint(
    'home_bp',
    __name__,
    template_folder="templates",
    static_folder="static"
)

@home_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")
