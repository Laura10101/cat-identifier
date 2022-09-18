from pymongo import MongoClient
from bson import ObjectId
import gridfs

from ..model import Prediction, PredictioneLabel

#create new class
class PredictionRepository:
    def __init__(self):
        pass

### Public Interface for the repository ###
    #create one method to store a new prediction in the database 
    def create_one(self, prediction):
        prediction_col = self.__get_db_collection()
         #validate prediction
        if not isinstance(prediction, Prediction):
            raise Exception("The prediction to store must be a valid prediction instance")

        #store prediction in the database
        #First, store the image file using gridfs and get its id
        image_store = self.__get_grid_fs()
        image_file_id = image_store.put(prediction.get_image())
        prediction.set_image(image_file_id)

        #Next, store the actual prediction in MongoDB
        serialised_prediction = prediction.serialize()
        del serialised_prediction['id'] #Remove the ID as we want this to be auto created
        return str(prediction_col.insert_one(serialised_prediction).inserted_id)

### Helper methods (private methods to encapsualte reusable logic)###
    def __get_grid_fs(self):
        client = MongoClient('localhost', 27017)
        return gridfs.GridFS(client.cat_identifier_db)

    def __get_db_collection(self):
        client = MongoClient('localhost', 27017)
        return client.cat_identifier_db.predictions

