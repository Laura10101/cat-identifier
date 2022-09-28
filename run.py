import os, json
from flask import Flask
import sys
sys.dont_write_bytecode = True


app = Flask(__name__)

env = app.env
with open("./config/config." + env + ".json") as config_file:
    config = json.load(config_file)

app.config.from_object(config)

with app.app_context():
    #Register APIs
    from blueprints.apis import prediction_bp, training_image_bp, user_bp
    app.register_blueprint(prediction_bp, url_prefix="/api/predictions")
    app.register_blueprint(training_image_bp, url_prefix="/api/training-images")
    app.register_blueprint(user_bp, url_prefix="/api/users")

    #Register apps
    from blueprints.apps import admin_bp, breeders_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(breeders_bp, url_prefix="/")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True
    )