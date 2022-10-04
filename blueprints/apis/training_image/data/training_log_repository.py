from pymongo import MongoClient
from bson import ObjectId

from ..model import TrainingLogEntry

class TrainingImageRepository:
    def __init__(self):
        pass

    def clear_log(self):
        pass

    def update_log(self, message):
        pass

    def get_log(self):
        pass

    ### HELPER METHODS ###
    def __get_db_collection(self):
        client = MongoClient('localhost', 27017)
        return client.cat_identifier_db.training_log_entries