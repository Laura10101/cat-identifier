from pymongo import MongoClient
from bson import ObjectId
import gridfs

from ..model import Prediction, PredictionLabel

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
        image_file_id = image_store.put(prediction.get_image(), encoding="utf-8")
        prediction.set_image(image_file_id)

        #Next, store the actual prediction in MongoDB
        serialised_prediction = prediction.serialize()
        del serialised_prediction['id'] #Remove the ID as we want this to be auto created
        return str(prediction_col.insert_one(serialised_prediction).inserted_id)

    #create a function to update a prediction with the user's feedback
    def set_user_feedback(self, id, user_feedback):
        #get database connection 
        prediction_col = self.__get_db_collection()
        #create new values object which also updates user has reviewed to true
        newvalues = { "$set": { "user_feedback": user_feedback, "user_has_reviewed": True } }
        #create query object
        query = { "_id": ObjectId(id) }
        #perform the update on the database
        prediction_col.update_one(query, newvalues)

    #create a function to update a prediction with the user's feedback
    def set_admin_feedback(self, id, admin_feedback):
        #get database connection 
        prediction_col = self.__get_db_collection()
        #create new values object which also updates user has reviewed to true
        newvalues = { "$set": { "admin_feedback": admin_feedback, "admin_has_reviewed": True } }
        #create query object
        query = { "_id": ObjectId(id) }
        #perform the update on the database
        prediction_col.update_one(query, newvalues)

    #create data access method for getting unreviewed predictions 
    def get_awaiting_admin_review_predictions(self):
        #get database connection 
        prediction_col = self.__get_db_collection()
        #create query object to query user has reviewed = false OR user feedback = false AND admin has reviewed = False
        query = { 
            "$and": [
                { "$or": [
                    { "user_has_reviewed": False },
                    { "user_feedback": False }
                ] },
                { "admin_has_reviewed": False }
            ]
         }
        #execute the query
        results = prediction_col.find(query)
        #deserialise the results by calling deserialisation method and iterating over the results 
        deserialised_predictions = []
        for result in results:
            deserialised_prediction = self.__deserialise_prediction(result)
            deserialised_predictions.append(deserialised_prediction)
        #return the results 
        return deserialised_predictions

### Helper methods (private methods to encapsualte reusable logic)###
    def __get_grid_fs(self):
        client = MongoClient('localhost', 27017)
        return gridfs.GridFS(client.cat_identifier_db)

    def __get_db_collection(self):
        client = MongoClient('localhost', 27017)
        return client.cat_identifier_db.predictions

    def __deserialise_prediction(self, data):
        image_store = self.__get_grid_fs()
        return Prediction(
            image_store.get(ObjectId(data["image"])).read(),
            self.__deserialise_prediction_label(data["label"]),
            id=data["_id"],
            user_has_reviewed=data["user_has_reviewed"],
            user_feedback=data["user_feedback"],
            admin_has_reviewed=data["admin_has_reviewed"],
            admin_feedback=data["admin_feedback"]
        )

    def __deserialise_prediction_label(self, data):
        return PredictionLabel(
            is_cat=data["is_cat"], 
            colour=data["colour"],
            is_tabby=data["is_tabby"],
            pattern=data["pattern"],
            is_pointed=data["is_pointed"]
        )

