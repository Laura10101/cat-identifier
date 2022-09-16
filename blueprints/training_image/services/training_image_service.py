from ..model import TrainingImage, TrainingImageLabel
from ..data import TrainingImageRepository

class TrainingImageService:
    def __init__(self):
        pass

    def create_training_image(self, image_file):
        image = TrainingImage(source='Admin', label=TrainingImageLabel(), is_labelled=False)
        repo = TrainingImageRepository()
        return repo.create_one(image, image_file)

    #create service layer function to retrieve images which have not yet been labelled
    def get_unlabelled_images(self):
        #create a new image of the training image repository class and assign it to variable 'repo'
        #this allows access to the functions in the data layer
        repo = TrainingImageRepository()
        #call data layer function get_unlabelled_images and return the result 
        return repo.get_unlabelled_images()
        
    #create method to update the label of an unlabelled image 
    def set_image_label(self, id, label):
        pass