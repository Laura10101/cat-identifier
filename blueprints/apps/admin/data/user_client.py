from requests import get, post

#A client class to enable interaction with the user API
class UserClient:
    def __init__(self, base_url):
        self.__base_url = base_url + "/users/"
        self.__get_headers = {

        }

        self.__post_headers = {
            "Content-Type": "application/json"
        }

    def register_user(self, username, password_hash):
        return True

    def user_authenticates(self, username, password_hash):
        return True

    def user_is_authorised(self, token):
        return True