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
        del serialized_model["_id"]
        #store it and return the id
        return str(models_col.isnert_one(serialized_model).inserted_id)

    #create method to return only the active model
    def get_active_model(self):
        #create the query object
        query = { "is_active": True }
        #return the first model (there should only be one)
        models = self.__get_models(query)
        return models[0]

    def get_all_models(self):
        return self.__get_models({})

    ### HELPER METHODS ###
    def __get_db_collection(self):
        client = MongoClient('localhost', 27017)
        return client.cat_identifier_db.prediction_models

    #Create a helper method to get models based on a query
    def __get_models(self, query):
        #Get the prediction models collection
        models_col = self.__get_db_collection()
        #Execute the query to get results
        results = models_col.find(query)
        #Deserialize the results
        deserialised_models = []
        for model in results:
            deserialised_model = self.__deserialise_prediction_model(model)
            deserialised_models.append(deserialised_model)

        #return the deserialised result
        return deserialised_models


    def __deserialise_prediction_model(self, data):
        return CatIdentificationModel(data)
