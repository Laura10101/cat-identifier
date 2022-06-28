import pymongo
from ..model import TrainingImage, TrainingImageLabel

class TrainingImageRepository:
    def __init__(self):
        pass

    def create(self, image):
        if not isinstance(image, TrainingImage):
            raise Exception("The image to store must be a valid TrainingImage instance")
        
    def update(self, image):
        pass

    def get(self, id):
        pass

    def list(self):
        pass

    def __serialise_image(self, image):
        return {
            "image": image.get_image(),
            "source": image.get_source(),
            "label": self.__serialise_image_label(self, image.get_label()),
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