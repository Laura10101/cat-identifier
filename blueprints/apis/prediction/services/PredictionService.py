### this class is the service layer for the predictions API ###

#import prediction repository 
from ..model import Prediction, PredictionLabel
from ..data import PredictionRepository
# import model classes
from ..model import *

# create the predictions service class
class PredictionService:
    #create class constructor
    def __init__(self):
        #create repository instance so it is accessible to all methods of this class
        self.__prediction_repository = PredictionRepository()

    #create method to create a new prediction in the database and return its ID
    def create_prediction(self, image, is_cat, colour, is_tabby, pattern, is_pointed):
        #create new prediction label instance
        label = PredictionLabel(is_cat, colour, is_tabby, pattern, is_pointed)
        #create new prediction 
        prediction = Prediction(image, label) 
        #store prediction in the database using the data access layer and return the result of it
        return self.__prediction_repository.create_one(prediction)

    #create method to set user feedback of a prediction in the database
    def set_user_feedback(self, id, user_feedback):
        self.__prediction_repository.set_user_feedback(id, user_feedback)

    #create service layer method to retrieve predictions awaiting admin review
    def get_awaiting_admin_review_predictions(self):
        return self.__prediction_repository.get_awaiting_admin_review_predictions()
    
    