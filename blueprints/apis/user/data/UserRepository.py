from pymongo import MongoClient
from bson import ObjectId

from ..model import User, UserToken

#crate UserRepository class - data access layer for Users
class UserRepository:
    def __init__(self):
        pass

    #Create method to check whether a user exists in the database
    #Adapted from Tim Nelson's user authentication and login videos
    #at CodeInstitute.com
    def user_exists(self, username):
        users_col = self.__get_db_collection()
        query = { "username": username }
        existing_user = users_col.find_one(query)
        return existing_user

    #Create register method to register new user in the database
    #Adapted from Tim Nelson's user authentication and login videos
    #at CodeInstitute.com
    def register_user(self, user):
        users_col = self.__get_db_collection()
        serialised_user = user.serialize()
        del serialised_user["id"]
        users_col.insert_one(serialised_user)

    #Create get method to retrieve single user from the database based on username
    def get_user(self, username):
        users_col = self.__get_db_collection()
        query = { "username": username }
        user = users_col.find_one(query)
        return self.__deserialise_user(user)

    #Create method to update the user's current token
    def update_token(self, user):
        users_col = self.__get_db_collection()
        query = { "username": user.get_username() }
        serialised_token = user.serialize()["current_token"]
        new_values = { "$set": { "current_token":  serialised_token }}
        users_col.update_one(query, new_values)

    ### HELPER METHODS ###
    def __get_db_collection(self):
        client = MongoClient('localhost', 27017)
        return client.cat_identifier_db.users

    def __deserialise_user(self, data):
        id = data["_id"]
        username = data["username"]
        password = data["password"]
        token = self.__deserialise_user_token(data["current_token"])
        return User(username, password, id=id, current_token=token)

    def __deserialise_user_token(self, data):
        if not data == None:
            token = data["token"]
            expiry_time = data["expiry_time"]
            return UserToken(token, expiry_time)
        return None