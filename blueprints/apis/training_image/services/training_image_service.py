from ..model import TrainingImage, TrainingImageLabel
from ..data import TrainingImageRepository

class TrainingImageService:
    def __init__(self):
        #create an instance of the training image repository that can be used by all methods of the training image service
        self.__repo = TrainingImageRepository()

    def create_training_image(self, image_file):
        image = TrainingImage(source='Admin', label=TrainingImageLabel(), is_labelled=False)
        return self.__repo.create_one(image, image_file)

    #create service layer function to retrieve images which have not yet been labelled
    def get_unlabelled_images(self):
        #this allows access to the functions in the data layer
        #call data layer function get_unlabelled_images and return the result 
        return self.__repo.get_unlabelled_images()
        
    #create method to update the label of an unlabelled image 
    def set_image_label(self, id, is_cat = False, colour = None, is_tabby = False, pattern = None, is_pointed=False):
        #create an instance of the training image label model class 
        label = TrainingImageLabel(is_cat, colour, is_tabby, pattern, is_pointed)
        #call the update label method on the training image repository 
        self.__repo.set_image_label(id, label)

    