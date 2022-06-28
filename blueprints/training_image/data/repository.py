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

    def __serialise_image(self, object):
        pass