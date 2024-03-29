import gc
import numpy as np
import pickle
from base64 import b64encode
from sklearn.model_selection import train_test_split
from keras.callbacks import LambdaCallback
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras import optimizers
from keras.models import Sequential

class CatIdentificationModel:
    def __init__(self, config):
        self.__config = config
        #Initialise a null model
        self.__model = None
        #Initialise a null set of test results
        self.__test_results = None
        #Time training started/ended
        self.__training_started = None
        self.__training_ended = None
        #Define the hyperparameters to use during training
        param_config = self.__config["training_parameters"]
        #Number of epochs
        self.__epochs = param_config["epochs"]
        #Batch sizes
        self.__test_batch_size = param_config["test_batch_size"]
        self.__train_batch_size = param_config["train_batch_size"]
        #Learning rate
        self.__learning_rate = param_config["learning_rate"]
        #Decay
        self.__decay = param_config["decay"]
        #Loss function
        self.__loss_function = param_config["loss_function"]
        #Metrics
        self.__metrics = param_config["metrics"]
        #Dropout rate
        self.__dropout = param_config["dropout_rate"]
        #Base file path
        self.base_path = ""

    #create public method to train neural network
    def train_model(self, training_images, log_training_status=None):
        # collect garbage before data preprocessing starts
        self.__collect_garbage()
        #this chains the other private methods together 
        #convert test data into numpy arrays so the ML model can use it 
        x_data, y_data = self.__convert_to_numpy(training_images)
        #Check to see if either the input or output data is empty
        if len(x_data) == 0 or len(y_data) == 0:
            return None #If so, return nothing
        else:
            #perform train, test, split
            x_train, x_test, y_train, y_test = self.__train_test_split(x_data, y_data)
            # unsplit data is no longer required
            del x_data
            del y_data
            self.__collect_garbage()
            #standardise the data 
            train_iterator, test_iterator = self.__get_data_iterators(x_train, x_test, y_train, y_test)
            # the iterator holds references to the train and test sets now
            # so collecting garbage here won't free up much memory
            #get model
            self.__model = self.__define_model(x_train[0].shape, y_train[0].shape[0])
            #calculate the training and test batch sizes
            #if the batch size is larger than the number of samples
            #then set the number of batches to 1, otherwise
            #do the calculation
            if self.__train_batch_size > train_iterator.n:
                training_batches = 1
            else:
                training_batches = train_iterator.n // self.__train_batch_size
            
            if self.__test_batch_size > test_iterator.n:
                test_batches = 1
            else:
                test_batches = test_iterator.n // self.__test_batch_size
            #create callback to report training status
            callbacks = []
            if not log_training_status is None:
                callbacks.append(LambdaCallback(
                    on_batch_end=lambda batch,logs: log_training_status(batch,logs,self.__config)
                ))
            # collect garbage before training starts for good measure
            self.__collect_garbage()
            #train the model
            self.__model.fit_generator(
                generator=train_iterator,
                steps_per_epoch=training_batches,
                epochs=self.__epochs,
                callbacks=callbacks
            )
            #test model 
            test_iterator.reset()
            self.__test_results = self.__model.evaluate_generator(
                test_iterator, steps=test_batches, verbose=1
            )
            # collect garbage after training for good measure
            self.__collect_garbage()
            #return test results and model file 
            serialized_model = self.__serialize()
            # finally collect garbage after serialization
            # which may add lots of additional objects to memory
            self.__collect_garbage()
            return serialized_model

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

    #create private method to return keras image data iterators for train and test data  
    #the image data iterators will standardise the image data as required
    def __get_data_iterators(self, x_train, x_test, y_train, y_test):
        #Create image data generator to normalize images between 0 and 1
        data_generator = ImageDataGenerator(rescale=1.0/255.0)
        #Create our train and test iterators
        train_iterator = data_generator.flow(x_train, y_train, batch_size=self.__train_batch_size)
        test_iterator = data_generator.flow(x_test, y_test, batch_size=self.__test_batch_size)
        return train_iterator, test_iterator

    #create private method to perform train/test/split 
    def __train_test_split(self, training_images, training_labels):
        #perform the split
        x_train, x_test, y_train, y_test = train_test_split(training_images, training_labels, test_size=0.33, random_state=42)
        #return the data as numpy arrays
        return np.array(x_train), np.array(x_test), np.array(y_train), np.array(y_test)

    #create private method to define the neural network 
    def __define_model(self, input_shape, output_shape):
        #create a sequential model
        model = Sequential()
        #create the input layer for the model
        #the input layer is a convolutional layer
        #the input shape is 100 x 100 x 3 (width x height x channels)
        model.add(Conv2D(
            32, #Number of filters
            (3,3), #Size of the stride
            padding='same',
            input_shape=input_shape
        ))
        model.add(Activation('relu'))

        #next, create the hidden layers
        #hidden layer 1 is another convolutional layer
        #the filters and stride match the input layer
        model.add(Conv2D(
            32, #Number of filters
            (3,3) #Shape of the stride
        ))
        model.add(Activation('relu'))
        #add a MaxPooling layer - this is standard when
        #working with convolutional neural networks
        model.add(MaxPooling2D(pool_size=(2,2)))
        #Randomly deactivate neurons during training to prevent overfitting
        model.add(Dropout(self.__dropout))

        #hidden layer 2 is also a convolutional layer
        #this time, the number of filters has been doubled
        model.add(Conv2D(
            64, #Number of filters
            (3,3) #Size of strides
        ))
        model.add(Activation('relu'))

        #hidden layer 3 is the final hidden layer (also convolutional)
        model.add(Conv2D(
            64, #Number of filters
            (3,3) #Size of strides
        ))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(self.__dropout))

        #create a prediction layer
        #this is used to extract the most interesting features from
        #the 3-dimensional data for the purposes of predicting
        #our 2-dimensional output array
        #flatten layer converts 3-d to 2-d layer
        model.add(Flatten())
        #create a dense layer with 512 neurons/units to make predictions
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dropout(self.__dropout))

        #create the output layer to predict each label in our target
        model.add(Dense(
            output_shape, #One unit per label
            activation='sigmoid' #Preferred activation function for
                                 #multi-label image classification
        ))

        #compile the model
        model.compile(
            optimizers.RMSprop(learning_rate=self.__learning_rate, decay=self.__decay),
            loss=self.__loss_function,
            metrics=self.__metrics
        )

        #return the compiled model
        return model

    #create a method to convert the model configuration including
    #architecture, weights, and hyperparameters to JSON data
    def __serialize(self):
        weights = self.__model.get_weights()
        return {
            "model": b64encode(pickle.dumps(self.__model.get_config(), protocol=0)).decode(),
            "weights": b64encode(pickle.dumps(weights, protocol=0)).decode(),
            "loss": self.__test_results[0],
            "accuracy": self.__test_results[1],
            "training_started": self.__training_started,
            "training_ended": self.__training_ended
        }
        
    # collect garbage, including printing results
    def __collect_garbage(self):
        print("Before: " + str(gc.get_count()))
        gc.collect()
        print("After: " + str(gc.get_count()))

    