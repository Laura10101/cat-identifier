import os
import json
import sys
from factories import make_flask, make_celery

sys.dont_write_bytecode = True

#import the env file if it exists
if os.path.exists("env.py"):
    import env

app = make_flask()

#import config from json
env = app.env
with open("./config/config." + env + ".json") as config_file:
    config = json.load(config_file)

#non-sensitive config data is imported from
#json config files
app.config.update(config)

#register blueprints
with app.app_context():
    from blueprints.apis import prediction_bp, training_image_bp, user_bp, analytics_bp
    #Register APIs
    app.register_blueprint(prediction_bp, url_prefix="/api/predictions")
    app.register_blueprint(training_image_bp, url_prefix="/api/training-images")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    from blueprints.apps import admin_bp, breeders_bp
    #Register apps
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(breeders_bp, url_prefix="/breeders")

    #Initialise the db with the app
    from blueprints.apis.analytics.database import db
    db.init_app(app)

#register celery app
#inspired by from StackOverflow
#https://stackoverflow.com/questions/59632556/importing-celery-in-flask-blueprints
celery = make_celery(app)
app.celery = celery

if __name__ == "__main__":
    #Create the database as follows based on StackOverflow solution
    #https://stackoverflow.com/questions/22929839/circular-import-of-db-reference-using-flask-sqlalchemy-and-blueprints
    with app.app_context():
        db.create_all()

    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG")
    )
    