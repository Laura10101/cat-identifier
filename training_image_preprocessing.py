#Based on the following articles:
#https://machinelearningmastery.com/how-to-normalize-center-and-standardize-images-with-the-imagedatagenerator-in-keras/
#https://vijayabhaskar96.medium.com/multi-label-image-classification-tutorial-with-keras-imagedatagenerator-cd541f8eaf24
#https://www.geeksforgeeks.org/how-to-normalize-center-and-standardize-image-pixels-in-keras/


from blueprints.apis.training_image.data import TrainingImageRepository
from blueprints.apis.training_image.model.cat_identification_model import CatIdentificationModel

#Fetch labelled training images
repo = TrainingImageRepository()
training_images = repo.get_labelled_images()

len(training_images)

#Fetch the trained model
model = CatIdentificationModel()
test_results = model.train_model(training_images)