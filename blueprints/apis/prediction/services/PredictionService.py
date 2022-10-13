### this class is the service layer for the predictions API ###

#import prediction repository 
from ..model import CatIdentificationModel
# import model classes
from ..model import *

# create the predictions service class
class PredictionService:
    #create class constructor
    def __init__(self, prediction_repo, prediction_model_repo):
        #create repository instance so it is accessible to all methods of this class
        self.__prediction_repository = prediction_repo
        self.__prediction_model_repository = prediction_model_repo

    #create method to make a new prediction, returning its label and id
    def create_prediction(self, b64_image):
        #get the active cat identifier (prediction) model
        model = self.__prediction_model_repository.get_active_model()
        #get the prediction
        prediction = model.get_phenotype_prediction(b64_image)
        #store the prediction
        id = self.__prediction_repository.create_one(prediction)
        #return the id and label
        return id, prediction.get_label().serialize()

    #create method to set user feedback of a prediction in the database
    def set_user_feedback(self, id, user_feedback):
        self.__prediction_repository.set_user_feedback(id, user_feedback)

    #create method to set admin feedback of a prediction in the database
    def set_admin_feedback(self, id, admin_feedback):
        self.__prediction_repository.set_admin_feedback(id, admin_feedback)

    #create service layer method to retrieve predictions awaiting admin review
    def get_awaiting_admin_review_predictions(self):
        return self.__prediction_repository.get_awaiting_admin_review_predictions()
    
    #create service layer method to store new prediction model in the database
    def create_prediction_model(self, serialised_model):
        model = CatIdentificationModel(serialised_model)
        return self.__prediction_model_repository.create_model(model)

    #create service layer method to get the active model from the database
    def get_active_model(self):
        return self.__prediction_model_repository.get_active_model()

    # get summary snapshot of predictions
    def get_prediction_snapshot(self):
        return self.__prediction_repository.get_snapshot()

    # get summary snapshot of prediction models
    def get_prediction_model_snapshot(self):
        return self.__prediction_model_repository.get_snapshot()
    