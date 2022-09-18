# import the prediction label class
from .PredictionLabel import PredictionLabel
# create prediction class to represent predictions made by the AI and the feedback provided on those predictions by breeders/cat owners and admins 
class Prediction:
    # create the constructor for the prediction class
    # as a minimum, every instance of the prediction class must have both an image and a label, all other attributes are optional. 
    def __init__(self, image, label, id = None, user_has_reviewed = False, user_feedback = False, admin_has_reviewed = False, admin_feedback = False):
        self.__id = id
        self.__image = image
        if not isinstance(label, PredictionLabel):
            raise Exception("Label is not a valid prediction label: ", label)
        self.__label = label
        self.__user_has_reviewed = user_has_reviewed
        self.__user_feedback = user_feedback
        self.__admin_has_reviewed = admin_has_reviewed
        self.__admin_feedback = admin_feedback

    #create getters and setters for all class attributes
    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id 

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_label(self):
        return self.__label

    def set_label(self, label):
        if not isinstance(label, PredictionLabel):
            raise Exception("Label is not a valid prediction label: ", label)
        self.__label = label

    def get_user_has_reviewed(self):
        return self.__user_has_reviewed

    def set_user_has_reviewed(self, user_has_reviewed):
        self.__user_has_reviewed = user_has_reviewed

    def get_user_feedback(self):
        return self.__user_feedback

    def set_user_feedback(self, user_feedback):
        self.__user_feedback = user_feedback

    def get_admin_has_reviewed(self):
        return self.__admin_has_reviewed

    def set_admin_has_reviewed(self, admin_has_reviewed):
        self.__admin_has_reviewed = admin_has_reviewed

    def get_admin_feedback(self):
        return self.__admin_feedback

    def set_admin_feedback(self, admin_feedback):
        self.__admin_feedback = admin_feedback

    def serialize(self):
        return {
            "id": self.get_id(),
            "image": self.get_image(),
            "label": self.get_image.serialize(),
            "user_has_reviewed": self.get_user_has_reviewed(),
            "user_feedback": self.get_user_feedback(),
            "admin_has_reviewed": self.get_admin_has_reviewed(),
            "admin_feedback": self.get_admin_feedback()
        }