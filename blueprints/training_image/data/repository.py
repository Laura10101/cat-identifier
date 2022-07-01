from pymongo import MongoClient

from blueprints.training_image.model import training_image_label
from ..model import TrainingImage, TrainingImageLabel

class TrainingImageRepository:
    def __init__(self):
        pass

    def create_one(self, image):
        if not isinstance(image, TrainingImage):
            raise Exception("The image to store must be a valid TrainingImage instance")
        serialised_image = self.__serialise_image(image)
        training_images_col = self.__get_db_collection()
        return training_images_col.insert_one(serialised_image).inserted_id

        
    def update(self, image):
        pass

    def get(self, id):
        pass

    #function to get unlabelled images from MongoDB
    def get_unlabelled_images(self):
        #create list/aray to store the images in
        unlabelled_images = []
        #create connection to the database using the pyMongo library
        training_images_col = self.__get_db_collection()
        #create query object to get only unlabelled images
        query = { "is_labelled": False }
        #execute the query to get the results
        #create new variable to hold the raw results of the query 
        results = training_images_col.find(query)
        #translate the data from the database's format, into objects of the model class (called deserialisation)
        #iterate over the results
        for image in results:
            pass
        #return unlabelled images variable 
        return unlabelled_images

    def list(self):
        pass

    def __get_db_collection(self):
        client = MongoClient('localhost', 27017)
        return client.cat_identifier_db.training_images

    def __serialise_image(self, image):
        return {
            "image": image.get_image(),
            "source": image.get_source(),
            "label": self.__serialise_image_label(image.get_label()),
            "is_labelled": image.get_is_labelled()
        }

    def __serialise_image_label(self, label):
        return {
            "is_cat": label.get_is_cat(),
            "colour": label.get_colour(),
            "is_tabby": label.get_is_tabby(),
            "pattern": label.get_pattern(),
            "is_pointed": label.get_is_pointed()
        }

    #deserialise function (maps from one format of data to another format of data)
    def __deserialise_image(self, data):
        pass

    def __deserialise_image_label(self, data):
        return TrainingImageLabel(
            is_cat=data["is_cat"], 
            colour=data["colour"],
            is_tabby=data["is_tabby"]
            pattern=data["pattern"],
            is_pointed=data["is_pointed"]
        )