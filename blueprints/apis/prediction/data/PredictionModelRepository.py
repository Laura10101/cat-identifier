from pymongo import MongoClient
from bson import ObjectId

from blueprints.apis import prediction

from ..model import CatIdentificationModel

#create repository class for cat identification models
class PredictionModelRepository:
    def __init__(self):
        pass

    ### PUBLIC INTERFACE ###
    #create method to store a new prediction model in the database
    #this also needs to deactivate existing models
    def create_model(self, prediction_model):
        #get the prediction model mongo collection
        models_col = self.__get_db_collection()
        #update all predictions that currently exist to be inactive
        new_values = { "$set": { "is_active": False }}
        models_col.update({}, new_values)
        #serialize the new prediction model
        serialized_model = prediction_model.serialize()
        #store it and return the id
        return str(models_col.isnert_one(serialized_model).inserted_id)

    #create method to return only the active model
    def get_active_model(self):
        pass

    def get_all_models(self):
        pass

    ### HELPER METHODS ###
    def __get_db_collection(self):
        client = MongoClient('localhost', 27017)
        return client.cat_identifier_db.prediction_models

    def __deserialise_prediction_model(self, data):
        return CatIdentificationModel(data)
