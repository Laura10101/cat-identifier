from sklearn.model_selection import train_test_split
import numpy as np

class CatIdentificationModel:
    def __init__(self):
        pass

    #create public method to train neural network
    def train_model(self, training_images):
        #this chains the other private methods together 
        #convert test data into numpy arrays so the ML model can use it 
        x_data, y_data = self.__convert_to_numpy(training_images)
        #standardise the data 
        x_data, y_data = self.__standardise_data(x_data, y_data)
        #perform train, test, split
        x_train, y_train, x_test, y_test = self.__train_test_split(x_data, y_data)
        #get model
        self.__model = self.__define_model()
        #run training loop to do the training 
        #test model 
        test_result = self.__test_model(x_test, y_test)
        #return test results and model file 
        return test_result

    #create private method to test neural network 
    def __test_model(self, training_images, training_labels):
        pass

    #create private method to convert training image objects to numpy array 
    def __convert_to_numpy(self, training_images):
        #create two arrays, one to hold numeric image data and one to hold numeric labels
        x_data = [] #numeric image data
        y_data = [] #numeric labels data 
        #iterate over each training image
        for training_image in training_images:
            #for each training image, get the image and the label as numeric data 
            numeric_image = training_image.get_preprocessed_image()
            numeric_label = training_image.get_label().get_numeric_label()
            #add the numeric image and numeric label to the relevant arrays
            if training_image.get_label().is_sufficient_for_training():
                x_data.append(numeric_image)
                y_data.append(numeric_label)
        #return both arrays
        return x_data, y_data

    #create private method to standardise data
    def __standardise_data(self, training_images, training_labels):
        pass

    #create private method to perform train/test/split 
    def __train_test_split(self, training_images, training_labels):
        return train_test_split(training_images, training_labels, test_size=0.33, random_state=42)

    #create provate method to define the neural network 
    def __define_model(self):
        pass