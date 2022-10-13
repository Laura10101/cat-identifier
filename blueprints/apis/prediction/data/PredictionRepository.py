from pymongo import MongoClient
from bson import ObjectId
import gridfs

from ..model import Prediction, PredictionLabel

#create new class
class PredictionRepository:
    def __init__(self, config):
        self.__config = config

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


    def get_snapshot(self):
        prediction_col = self.__get_db_collection()
        snapshot = prediction_col.aggregate([{
            "$group": {
                "_id": {
                    "is_labelled": True,
                    "is_cat": "$label.is_cat",
                    "colour": "$label.colour",
                    "is_tabby": "$label.is_tabby",
                    "pattern": "$label.pattern",
                    "is_pointed": "$label.is_pointed",
                    "user_has_reviewed": "$user_has_reviewed",
                    "user_feedback": "$user_feedback",
                    "admin_has_reviewed": "$admin_has_reviewed",
                    "admin_feedback": "$admin_feedback"
                },
                "count": { "$sum": 1 }
            }
        }])

        deserialized_snapshot = []
        for summary in snapshot:
            user_review_status = self.__get_review_status(
                summary["user_has_reviewed"],
                summary["user_feedback"]
            )

            admin_review_status = self.__get_review_status(
                summary["admin_has_reviewed"],
                summary["admin_feedback"]
            )
            deserialized_snapshot.append({
                "is_labelled": summary["is_labelled"],
                "is_cat": summary["is_cat"],
                "colour": summary["colour"],
                "is_tabby": summary["is_tabby"],
                "pattern": summary["pattern"],
                "is_pointed": summary["is_pointed"],
                "user_review_status": user_review_status,
                "admin_review_status": admin_review_status
            })
        return deserialized_snapshot

### Helper methods (private methods to encapsualte reusable logic)###
    def __get_mongo_db(self):
        client = MongoClient(self.__config["MONGO_URI"], 27017)
        return client[self.__config["MONGO_DB"]]

    def __get_grid_fs(self):
        db = self.__get_mongo_db()
        return gridfs.GridFS(db)

    def __get_db_collection(self):
        db = self.__get_mongo_db()
        return db[self.__config["MONGO_PREDICTIONS"]]

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

    def __get_review_status(self, is_reviewed, feedback):
        if not is_reviewed:
            return "Not Reviewed"
        elif feedback:
            return "Accepted"
        else:
            return "Rejected"

