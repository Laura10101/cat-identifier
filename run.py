import os, json
from flask import Flask
import sys
sys.dont_write_bytecode = True

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

env = app.env
with open("./config/config." + env + ".json") as config_file:
    config = json.load(config_file)

app.config.update(config)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

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
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )