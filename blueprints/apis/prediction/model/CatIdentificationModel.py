from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from base64 import b64encode, b64decode
import io
from PIL import Image
import numpy as np

from blueprints.apis.prediction.model.PredictionLabel import PredictionLabel
from .Prediction import Prediction

#Represents a machine learning model for predicting
#cat phenotypes from an image of the cat
class CatIdentificationModel:
    def __init__(self, serialized_model):
        #deserialize the model
        self.__serialized_model = serialized_model
        #create the sequential model from the serialized model
        self.__model = Sequential.from_config(serialized_model["model"])
        #update the weights
        self.__model.set_weights(serialized_model["weights"])
        #update ID if it exists at this stage
        if "_id" in serialized_model:
            self.__id = serialized_model["_id"]
        else:
            self.__id = None

        self.__training_started = serialized_model["training_started"]
        self.__training_ended = serialized_model["training_ended"]

        #default is_active to true because if the is_active property
        #doesn't yet exist then we assume that it hasn't yet been
        #saved to the database in which case it is likely to be the latest
        #model to be posted to the API and therefore the new active one
        #in the event of a race condition, whichever is saved to the database
        #last will become the active model
        if "is_active" in serialized_model:
            self.__is_active = serialized_model["is_active"]
        else:
            self.__is_active = True

    #The model is read only
    def get_id(self):
        return self.__id

    def get_training_started(self):
        return self.__training_started

    def get_training_ended(self):
        return self.__training_ended

    def is_active(self):
        return self.__is_active

    def get_phenotype_prediction(self, b64_image):
        #make the prediction using the ML model
        prediction = self.__make_prediction(b64_image)

        #interpret the prediction output to produce the
        #prediction label
        label = PredictionLabel.from_prediction_output(prediction)

        #create and return the prediction object
        return Prediction(b64_image, label)

    def serialize(self):
        #Ensure these attributes are set as when posting models
        #for the first time, these won't yet exist in the serialized model
        #data so they need to be set with defaults
        self.__serialized_model["_id"] = self.get_id()
        self.__serialized_model["is_active"] = self.is_active()
        return self.__serialized_model

    def __make_prediction(self, b64_image):
        #first, preprocess the image so it is a consistent size
        #and represented as a numpy array
        preprocessed_image = self.__get_preprocessed_image(b64_image)
        #create the iterator to normalise the image and feed
        #into the model
        iterator = self.__get_data_iterator([preprocessed_image])
        #make the prediction
        pred = self.__model.predict_generator(iterator, verbose=1)
        #return the prediction
        return pred

    #create method to return pre-processed image (chains other methods together)
    def __get_preprocessed_image(self, b64_image):
        #get resized image data
        image_data = self.__get_resized_image(b64_image)
        #convert image data to numerical data 
        image_data = self.__get_numerical_image(image_data)
        #return standardised image
        return image_data

    #create method to standardise image size
    #this code was taken from stack overflow, see link below
    #https://stackoverflow.com/questions/61574724/how-to-resize-base64-encoded-image-in-python
    def __get_resized_image(self, base64_str):
        #create a buffer to hold image data
        buffer = io.BytesIO()
        #decode base64 image back into binary
        imgdata = b64decode(base64_str)
        #create a buffer containing binary image data and use this to open an image
        img = Image.open(io.BytesIO(imgdata))
        #resize the image
        new_img = img.resize((100, 100))  # x, y
        #save the resized image back into the buffer created earlier
        new_img.save(buffer, format="JPEG")
        #encode the information in the buffer back into base64
        img_b64 = b64encode(buffer.getvalue())
        return img_b64

    #create method to convert image data into numerical data 
    #code adapted from stckovderflow answer, link below
    #https://stackoverflow.com/questions/57318892/convert-base64-encoded-image-to-a-numpy-array
    def __get_numerical_image(self, image_data):
        #decode the base64 image data back to binary
        base64_decoded = b64decode(image_data)
        #open the binary data as an image using PILLOW
        image = Image.open(io.BytesIO(base64_decoded))
        #converts the open image to a numpy array and returns it
        return np.array(image)

    #create private method to return keras image data iterator for the prediction
    #the image data iterator will standardise the image data as required
    def __get_data_iterator(self, x_pred):
        #Create image data generator to normalize images between 0 and 1
        data_generator = ImageDataGenerator(rescale=1.0/255.0)
        #Create the iterator
        iterator = data_generator.flow(
            x=x_pred,
            batch_size=1
        )
        return iterator