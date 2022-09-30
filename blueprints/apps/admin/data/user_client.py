from lib2to3.pytree import Base
from requests import get, post
from .base_client import BaseAPIClient

#A client class to enable interaction with the user API
class UserClient(BaseAPIClient):
    def __init__(self, base_url):
        BaseAPIClient.__init__(self, base_url + "/users")

    def register_user(self, username, password):
        endpoint = "/"
        data = {
            "username": username,
            "password": password
        }
        response = self._post(endpoint, data)
        
        if response.ok:
            return None
        
        return response.content["error"]

    def authenticate_user(self, username, password):
        endpoint = "/login"
        data = {
            "username": username,
            "password": password
        }
        response = self._post(endpoint, data)

        if response.ok:
            return response.content["token"]
        return None

    def authorise_user(self, username, token):
        endpoint = "/authorize"
        data = {
            "username": username,
            "token": token
        }
        response = self._post(endpoint, data)

        if response.ok:
            return response.content["token"]
        return None