import os
import traceback
import json
from celery import shared_task
from datetime import datetime
from ..services import TrainingImageService
from ..model import TrainingLogEntry
from ..data import TrainingLogRepository, TrainingImageRepository, PredictionAPIClient

config = None
service = None
training_log_repo = None

def get_env_config():
    if config is None:
        globals()["config"] = {}
        #import sensitive config data from env.py
        globals()["config"]["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        globals()["config"]["BROKER_URL"] = os.environ.get("REDIS_URL")
        globals()["config"]["API_KEY"] = os.environ.get("API_KEY")
        globals()["config"]["MONGO_URI"] = os.environ.get("MONGO_URI")
        globals()["config"]["MONGO_DB"] = os.environ.get("MONGO_DB")
        globals()["config"]["MONGO_PREDICTIONS"] = os.environ.get("MONGO_PREDICTIONS")
        globals()["config"]["MONGO_PREDICTION_MODELS"] = os.environ.get("MONGO_PREDICTION_MODELS")
        globals()["config"]["MONGO_TRAINING_IMAGES"] = os.environ.get("MONGO_TRAINING_IMAGES")
        globals()["config"]["MONGO_TRAINING_LOG"] = os.environ.get("MONGO_TRAINING_LOG")
        globals()["config"]["MONGO_USERS"] = os.environ.get("MONGO_USERS")
        globals()["config"]["API_BASE_URL"] = os.environ.get("API_BASE_URL")

        # fix database uri for non-development (Heroku) environments
        uri = os.environ.get("DATABASE_URL")
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        globals()["config"]["SQLALCHEMY_DATABASE_URI"] = uri

        # now handle the json config
        with open(os.environ.get("CONFIG_FILE")) as config_file:
            json_config = json.load(config_file)
            
        for key in json_config:
            globals()["config"][key] = json_config[key]
    return config

def get_training_log_repo():
    if training_log_repo is None:
        globals()["training_log_repo"] = TrainingLogRepository(get_env_config())
    return training_log_repo

#factory method to create and configure
#a training image service instance
def get_service():
    if service is None:
        repo = TrainingImageRepository(get_env_config())
        prediction_api = PredictionAPIClient(get_env_config())
        globals()["service"] = TrainingImageService(get_env_config(), repo, get_training_log_repo(), prediction_api)
    return service

@shared_task(name="training_tasks.train_model")
def train_model():
    try:
        #clear log before commmencing training
        get_training_log_repo().clear_log()
        #log training started message
        get_training_log_repo().update_log(TrainingLogEntry(datetime.now(), "Starting training..."))
        #train the model
        get_service().train_new_model()
        #log training completed message
        get_training_log_repo().update_log(TrainingLogEntry(datetime.now(), "Completed training successfully."))
    except Exception as e:
        #if an exception occurs, create a log entry
        timestamp = datetime.now()
        message = traceback.format_exc()
        get_training_log_repo().update_log(TrainingLogEntry(timestamp, message))