from .training_image_label import TrainingImageLabel
from base64 import b64encode, b64decode
import io
from PIL import Image
import numpy as np


class TrainingImage:
    def __init__(self, id = None, image = None, source = "Admin", label = None, is_labelled = False):
        self.__valid_sources = ['Google', 'Admin', 'User']
        self._id = id
        self._image = image

        if source not in self.__valid_sources:
            raise Exception("Training image source not recognised: ", source)
        self._source = source

        if not label == None:
            if not isinstance(label, TrainingImageLabel):
                raise Exception("Label is not a valid training image label: ", label)
        self._label = label

        self._is_labelled = is_labelled

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image

    #create method to return pre-processed image (chains other methods together)
    def get_preprocessed_image(self):
        #get resized image data
        image_data = self.__get_resized_image()
        #convert image data to numerical data 
        image_data = self.__get_numerical_image(image_data)
        #return standardised image
        return image_data

    #create method to standardise image size
    #this code was taken from stack overflow, see link below
    #https://stackoverflow.com/questions/61574724/how-to-resize-base64-encoded-image-in-python
    def __get_resized_image(self):
        #get the image data for this training image
        base64_str = self.get_image()
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

    def get_source(self):
        return self._source

    def set_source(self, source):
        if source not in self.__valid_sources:
            raise Exception("Training image source not recognised: ", source)
        self._source = source

    def get_label(self):
        return self._label

    def set_label(self, label):
        if not label == None:
            if not isinstance(label, TrainingImageLabel):
                raise Exception("Label is not a valid training image label: ", label)
        self._label = label

    def get_is_labelled(self):
        return self._is_labelled

    def set_is_labelled(self, is_labelled):
        self._is_labelled = is_labelled
    
    def serialize(self):
        return {
            "id": str(self.get_id()),
            "image": self.get_image(),
            "source": self.get_source(),
            "label": self.get_label().serialize(),
            "is_labelled": self.get_is_labelled()
        }