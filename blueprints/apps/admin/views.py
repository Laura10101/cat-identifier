from flask import Blueprint, render_template, request, current_app as app

#Blueprint Configuration
admin_bp = Blueprint(
    'admin_bp',
    __name__,
    template_folder="templates"
)

#View routes
@admin_bp.route("/login", methods=["GET"])
def display_login_form():
    return render_template("login.html")