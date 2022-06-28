import os
from flask import Flask


app = Flask(__name__)

with app.app_context():
    from blueprints import training_image_bp
    app.register_blueprint(training_image_bp, url_prefix="/training_images")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True
    )