from itsdangerous import serializer
from pymongo import MongoClient
from bson import ObjectId

from ..model import TrainingLogEntry

class TrainingLogRepository:
    def __init__(self):
        pass

    #create a function to remove all log entries from the training log
    def clear_log(self):
        #get the mongo collection
        log_col = self.__get_db_collection()
        #remove all records from it
        log_col.delete_many({})

    #create a function to push a new training log entry to the log
    def update_log(self, entry):
        #get the mongo collection
        log_col = self.__get_db_collection()
        #serialize the entry
        serialised_entry = entry.serialize()
        #store it
        log_col.insert_one(serialised_entry).inserted_id
        #no need to return the insert id for log entries
        #as no functionality will be provided to retrieve a log entry by id

    #create a function to read the contents of the log
    def get_log(self):
        #get the mongo collection
        log_col = self.__get_db_collection()
        #get all entries
        entries = log_col.find()
        #deserialise the entries
        deserialised_entries = []
        for entry in entries:
            deserialised_entries.append(self.__deserialise_entry(entry))
        return deserialised_entries

    ### HELPER METHODS ###
    def __get_db_collection(self):
        client = MongoClient('localhost', 27017)
        return client.cat_identifier_db.training_log_entries

    #deserialise a log entry
    def __deserialise_entry(self, serialised_entry):
        return TrainingLogEntry(serialised_entry["timestamp"], serialised_entry["message"])
