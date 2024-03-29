from pymongo import MongoClient
from bson import ObjectId
from bs4 import BeautifulSoup
from html import escape
import gridfs
import requests

from ..model import TrainingImage, TrainingImageLabel

class TrainingImageRepository:
    def __init__(self, config):
        self.__config = config
    
    #### PUBLIC INTERFACE ####
    def create_one(self, image, image_file):
        if not isinstance(image, TrainingImage):
            raise Exception("The image to store must be a valid TrainingImage instance")

        training_images_col = self.__get_db_collection()

        #First, store the image file using gridfs and get its id
        image_store = self.__get_grid_fs()
        image_file_id = image_store.put(image_file)
        image.set_image(image_file_id)

        #Next, blah
        serialised_image = image.serialize()
        del serialised_image['id'] #Remove the ID as we want this to be auto created
        return str(training_images_col.insert_one(serialised_image).inserted_id)
        
    # Store the label for an image against the image in the database 
    def set_image_label(self, id, label):
        #create connection to the database using the pyMongo library
        training_images_col = self.__get_db_collection()
        #save the label 
        #convert label into JSON object so it can be saved to DB: this is called serialisation 
        #a method to do this has been created on the training image label class
        #so we call the method (serialize) and store the result in a new variable, which we have to create next:
        serialised_label = label.serialize()
        #create update query object to locate record to update
        query = { "_id": ObjectId(id) }
        #create new values object to include deserialised image data
        newvalues = { "$set": { "label": serialised_label, "is_labelled": True } }
        #perform the update
        training_images_col.update_one(query, newvalues)

    # method to retrieve a single image by its databse ID
    def get(self, id):
        #create connection to the database using the pyMongo library
        training_images_col = self.__get_db_collection()
        #create query object to get only the image that matches the given ID
        query = { "_id": ObjectId(id) }
        #execute the query (and define variable to hold it)
        serialised_image = training_images_col.find_one(query)
        #deserialise the result from JSON to python
        image = self.__deserialise_image(serialised_image)
        #return the deserialised image
        return image    

    #function to get unlabelled images from MongoDB
    def get_unlabelled_images(self, source_query=None):
        #create list/aray to store the images in
        unlabelled_images = []
        #create connection to the database using the pyMongo library
        training_images_col = self.__get_db_collection()
        #create query object to get only unlabelled images
        query = { "is_labelled": False }
        if not source_query is None:
            query["source_query"] = source_query
        #execute the query to get the results
        #create new variable to hold the raw results of the query 
        results = training_images_col.find(query)
        #translate the data from the database's format, into objects of the model class (called deserialisation)
        #iterate over the results
        for image in results:
            deserialised_image = self.__deserialise_image(image)
            unlabelled_images.append(deserialised_image)
        #return unlabelled images variable 
        return unlabelled_images

    #function to get labelled training images from MongoDB
    def get_labelled_images(self):
        #create list/aray to store the images in
        labelled_images = []
        #create connection to the database using the pyMongo library
        training_images_col = self.__get_db_collection()
        #create query object to get only labelled images
        query = { "is_labelled": True }
        #execute the query to get the results
        #create new variable to hold the raw results of the query 
        results = training_images_col.find(query)
        #translate the data from the database's format, into objects of the model class (called deserialisation)
        #iterate over the results
        for image in results:
            deserialised_image = self.__deserialise_image(image)
            labelled_images.append(deserialised_image)
        #return labelled images variable 
        return labelled_images    

    def get_image_urls_from_search(self, query, count, start_at):
        #Create the query URL from a template
        #Adapted from https://python.plainenglish.io/how-to-scrape-images-using-beautifulsoup4-in-python-e7a4ddb904b8
        base_url = "https://www.google.com"
        template_url = "/search?q={#QUERY#}&sxsrf=ALeKk03xBalIZi7BAzyIRw8R4_KrIEYONg:1620885765119&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjv44CC_sXwAhUZyjgGHSgdAQ8Q_AUoAXoECAEQAw&cshid=1620885828054361"
        query_url = base_url + template_url.replace("{#QUERY#}", escape(query))
        #List to hold the results of the search
        urls = []
        current_image = 0
        #Iterate through search pages until we have enough image urls
        while len(urls) < count:
            #Retrieve the search results page
            results_page = requests.get(query_url)
            #Parse the HTML from the search results page
            parsed_results = BeautifulSoup(results_page.content, 'html.parser')
            #Get both the image and the next button elements from the results page
            image_tags = parsed_results.find_all('img', class_='yWs4tf')
            next_link = parsed_results.find_all('a', class_='frGj1b')
            #Iterate over image elements on the current results page
            for image_tag in image_tags:
                #If we don't yet have enough images but have passed start_at,
                #then add the url for the next image on the page
                if len(urls) < count and current_image >= start_at:
                    urls.append(image_tag['src'])
                #Increment the counter for the number of results passed
                current_image += 1
            #Once all images on the page have been processed, get location of the next page
            query_url = base_url + next_link[0]['href']
        return urls

    def clear_training_images(self, query):
        training_images_col = self.__get_db_collection()
        cleaned_filter = {}
        for attribute in query:
            if attribute == "is_labelled":
                cleaned_filter[attribute] = query[attribute]
            else:
                cleaned_filter["label." + attribute] = query[attribute]

        training_images_col.delete_many(cleaned_filter)

    def get_snapshot(self):
        training_images_col = self.__get_db_collection()
        snapshot = training_images_col.aggregate([{
            "$group": {
                "_id": {
                    "is_labelled": "$is_labelled",
                    "is_cat": "$label.is_cat",
                    "colour": "$label.colour",
                    "is_tabby": "$label.is_tabby",
                    "pattern": "$label.pattern",
                    "is_pointed": "$label.is_pointed",
                    "source": "$source"
                },
                "count": { "$sum": 1 }
            }
        }])
        deserialized_snapshot = []
        for summary in snapshot:
            deserialized_snapshot.append({
                "is_unlabelled": not summary["_id"]["is_labelled"],
                "is_cat": summary["_id"]["is_cat"],
                "colour": summary["_id"]["colour"],
                "is_tabby": summary["_id"]["is_tabby"],
                "pattern": summary["_id"]["pattern"],
                "is_pointed": summary["_id"]["is_pointed"],
                "source": summary["_id"]["source"],
                "count": summary["count"]
            })
        return deserialized_snapshot

    #### HELPER FUNCTIONS ####
    def __get_mongo_db(self):
        client = MongoClient(self.__config["MONGO_URI"], 27017)
        return client[self.__config["MONGO_DB"]]

    def __get_grid_fs(self):
        db = self.__get_mongo_db()
        return gridfs.GridFS(db)

    def __get_db_collection(self):
        db = self.__get_mongo_db()
        return db[self.__config["MONGO_TRAINING_IMAGES"]]

    #deserialise function (maps from one format of data to another format of data)
    def __deserialise_image(self, data):
        image_store = self.__get_grid_fs()

        query = None
        if "source_query" in data:
            query = data["source_query"]

        return TrainingImage(
            id=data["_id"],
            image=image_store.get(ObjectId(data["image"])).read().decode(),
            source=data["source"],
            label=self.__deserialise_image_label(data["label"]), 
            is_labelled=data["is_labelled"],
            query=query
        )

    def __deserialise_image_label(self, data):
        return TrainingImageLabel(
            is_cat=data["is_cat"], 
            colour=data["colour"],
            is_tabby=data["is_tabby"],
            pattern=data["pattern"],
            is_pointed=data["is_pointed"]
        )