from pymongo import MongoClient
import gridfs

from blueprints.training_image.model import training_image_label
from ..model import TrainingImage, TrainingImageLabel

class TrainingImageRepository:
    def __init__(self):
        pass
    
    #### PUBLIC INTERFACE ####
    def create_one(self, image, image_file):
        if not isinstance(image, TrainingImage):
            raise Exception("The image to store must be a valid TrainingImage instance")

        training_images_col = self.__get_db_collection()

        #First, store the image file using gridfs and get its id
        image_store = self.__get_grid_fs()
        image_file_id = image_store.put(image_file, content_type=image_file.content_type)
        image.set_image(image_file_id)

        #Next, blah
        serialised_image = image.serialize()
        del serialised_image['id'] #Remove the ID as we want this to be auto created
        return str(training_images_col.insert_one(serialised_image).inserted_id)
        
    # Store the label for an image against the image in the database 
    def set_image_label(self, id, label):
        #create connection to the database using the pyMongo library
        training_images_col = self.__get_db_collection()
        #save the label 
        #convert label into JSON object so it can be saved to DB: this is called serialisation 
        #a method to do this has been created on the training image label class
        #so we call the method (serialize) and store the result in a new variable, which we have to create next:
        serialised_label = label.serialize()
        #create update query object to locate record to update
        query = { "_id": id }
        #create new values object to include deserialised image data
        newvalues = { "$set": { "label": serialised_label } }
        #perform the update
        training_images_col.update_one(query, newvalues)

    # method to retrieve a single image by its databse ID
    def get(self, id):
        #create connection to the database using the pyMongo library
        training_images_col = self.__get_db_collection()
        #create query object to get only the image that matches the given ID
        query = { "_id": id }
        #execute the query (and define variable to hold it)
        serialised_image = training_images_col.find_one(query)
        #deserialise the result from JSON to python
        image = self.__deserialise_image(serialised_image)
        #return the deserialised image
        return image    

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
            deserialised_image = self.__deserialise_image(image)
            unlabelled_images.append(deserialised_image)
        #return unlabelled images variable 
        return unlabelled_images

    def list(self):
        pass

    #### HELPER FUNCTIONS ####
    def __get_grid_fs(self):
        client = MongoClient('localhost', 27017)
        return gridfs.GridFS(client.cat_identifier_db)

    def __get_db_collection(self):
        client = MongoClient('localhost', 27017)
        return client.cat_identifier_db.training_images

    #deserialise function (maps from one format of data to another format of data)
    def __deserialise_image(self, data):
        image_store = self.__get_grid_fs()
        return TrainingImage(
            id=data["_id"],
            image=image_store.get(data["image"]).read(),
            source=data["source"],
            label=self.__deserialise_image_label(data["label"]), 
            is_labelled=data["is_labelled"]
        )

    def __deserialise_image_label(self, data):
        return TrainingImageLabel(
            is_cat=data["is_cat"], 
            colour=data["colour"],
            is_tabby=data["is_tabby"],
            pattern=data["pattern"],
            is_pointed=data["is_pointed"]
        )