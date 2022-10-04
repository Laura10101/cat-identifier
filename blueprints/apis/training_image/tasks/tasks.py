import traceback
from celery import shared_task
from datetime import datetime
from ..services import TrainingImageService
from ..model import TrainingLogEntry
from ..data import TrainingLogRepository

@shared_task(name="training_tasks.train_model")
def train_model():
    service = TrainingImageService()
    repo = TrainingLogRepository()
    try:
        #clear log before commmencing training
        repo.clear_log()
        service.train_new_model()
    except Exception as e:
        #if an exception occurs, create a log entry
        timestamp = datetime.now()
        message = traceback.format_exc()
        repo.update_log(TrainingLogEntry(timestamp, message))