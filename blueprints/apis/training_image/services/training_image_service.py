from concurrent.futures import process
from uuid import uuid4
from blueprints.apis.training_image.data.PredictionAPIClient import PredictionAPIClient
from ..model import TrainingImage, TrainingImageLabel, CatIdentificationModel
from ..data import TrainingImageRepository, TrainingLogRepository
from os import listdir
from os.path import isfile, isdir, join
from shutil import rmtree
from base64 import b64encode
from requests import get

class TrainingImageService:
    def __init__(self):
        #create an instance of the training image repository that can be used by all methods of the training image service
        self.__repo = TrainingImageRepository()
        self.__log_repo = TrainingLogRepository()

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

    #create method to search google images for a list of images matching the given query term
    def get_image_urls_from_search(self, query, count=1000, start_at = 0):
        #Use the training image repository to retrieve the given number of image urls for the given query
        return self.__repo.get_image_urls_from_search(query, count, start_at)

    #create method to upload training images from a zip file 
    def upload_images_from_zip(self, zip_file):
        #create variable to hold the destination file path for extraction
        extraction_file_path = ".\\" + str(uuid4()) + "\\"
        #run unzip method on the object, method is called extractall
        zip_file.extractall(extraction_file_path)

        #perform depth first tree walk on the file structure: see helper methods 
        processed, ignored = self.process_extracted_files(extraction_file_path, {}, [])
    
        #delete the extracted files
        rmtree(extraction_file_path)

        return processed, ignored

    #import training images from a list of urls
    def import_images_from_url(self, image_urls):
        #create dictionary to hold ids of the created images
        image_ids = {}
        #loop over each of the image urls in turn 
        for url in image_urls:
            #for each image url, need to retrieve the image data from that url 
            image = b64encode(get(url).content)
            #use existing create method to create a training image in the database from the image url
            id = self.create_training_image(image)
            #update dictionary with the id and url of the created training image 
            image_ids[url] = id
        return image_ids

    #train a new model
    def train_new_model(self):
        #get training images using the training images repo
        training_images = self.__repo.get_labelled_images()
        #create the CatIdentificationModel instance
        model = CatIdentificationModel()
        serialized_model = model.train_model(training_images, log_training_status=handle_training_batch_end)

        #If serialized model is null, this is because there was insufficient
        #data to train the model
        if serialized_model == None:
            raise Exception("Insufficient training data exists to train the cat identification model")

        #Update the predictions API with the new model
        pred_api_client = PredictionAPIClient()
        posted = pred_api_client.post_trained_model(serialized_model)
        
        if not posted:
            raise Exception("Failed to update predictions API with trained model")

    #retrieve log entries from the database
    def read_log(self):
        #read the log entries
        entries = self.__log_repo.get_log()
        #sort them by timestamp
        entries.sort(key=lambda x: x.get_timestamp())
        return entries

        
    ### HELPER METHODS ###
    #recursive depth first tree walk algorithm to process extracted files from zip file
    def process_extracted_files(self, directory, processed_images, ignored_files):
        #get children of current directory
        children = listdir(directory)
        #for each file/node check that it is a valid image file 
        for child in children:
            path_to_child = join(directory, child)
            rel_path_to_child = path_to_child.replace(directory, ".\\")
            #check if folder
            if isdir(path_to_child):
                #if folder, recurse in order to process children of this folder
                self.process_extracted_files(path_to_child, processed_images, ignored_files)
            elif isfile(path_to_child):
                if self.is_allowed_extension(child):
                    id = self.process_image_file(path_to_child)
                    processed_images[rel_path_to_child] = id
                else:
                    ignored_files.append(rel_path_to_child)
        return processed_images, ignored_files
                
    #method to process image files found in zip file 
    def process_image_file(self, file_path):
        #open the file for reading 
        with open(file_path, "rb") as image_file:
            #read the data out of the file as base64 
            image_data = b64encode(image_file.read())
        #pass that over to existing service for creating new training images
        return self.create_training_image(image_data)

    #check to make sure that file name is a png or jpeg
    def is_allowed_extension(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in { "png", "jpg", "jfif" }


#callback function to handle training batch end events
def handle_training_batch_end(batch, logs):
    #create a new training log entry
    #get a training log repo
    repo = TrainingLogRepository()
    #store the training log entry in the log
