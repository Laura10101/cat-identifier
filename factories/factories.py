"""
Implements a series of factory methods for
creating Flask and Celery apps
"""
import os
from flask import Flask
from celery import Celery

#Flask factory to make and configure a Flask application
def make_flask():
    '''
    Creates a new Flask app

        Parameters: None

        Returns: An instance of a Flask app
    '''
    #create the flask app
    app = Flask(__name__)

    #import sensitive config data from env.py
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["BROKER_URL"] = os.environ.get("REDIS_URL")
    app.config["API_KEY"] = os.environ.get("API_KEY")
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    app.config["MONGO_DB"] = os.environ.get("MONGO_DB")
    app.config["MONGO_PREDICTIONS"] = os.environ.get("MONGO_PREDICTIONS")
    app.config["MONGO_PREDICTION_MODELS"] = os.environ.get("MONGO_PREDICTION_MODELS")
    app.config["MONGO_TRAINING_IMAGES"] = os.environ.get("MONGO_TRAINING_IMAGES")
    app.config["MONGO_TRAINING_LOG"] = os.environ.get("MONGO_TRAINING_LOG")
    app.config["MONGO_USERS"] = os.environ.get("MONGO_USERS")
    app.config["API_BASE_URL"] = os.environ.get("API_BASE_URL")

    # fix database uri for non-development (Heroku) environments
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

    return app

# celery factory to enable integration between Celery and Flask
# taken from Flask documentation: https://flask.palletsprojects.com/en/2.2.x/patterns/celery/
# modified as per Celery documentation:
# https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html
def make_celery(app):
    '''
    Factory method for a Celery instance

        Parameters:
            app (Flask app): The Flask app to use as the context for the Celery instance

        Returns:
            A Celery instance
    '''
    celery = Celery(
        "flask-celery-app",
        broker=app.config["BROKER_URL"],
        include=["..blueprints.apis.training_image.tasks"]
    )

    class ContextTask(celery.Task):
        """
        Allows a Celery task to run outside of an app context
        """
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# inspired by StackOverflow:
# https://stackoverflow.com/questions/22172915/relative-imports-require-the-package-argument
def make_celery_worker(broker_url):
    '''
    Creates a Celery worker instance without circular references

        Parameters:
            broker_url (str): The URL for the Redis instance

        Returns:
            A Celery instance, configured for the worker context
    '''
    return Celery(
        "flask-celery-app",
        broker=broker_url,
        include=["blueprints.apis.training_image.tasks"]
    )
