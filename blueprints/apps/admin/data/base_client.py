from requests import get, post
#Create a base API client providing common functionality
#for interacting with REST APIs
class BaseAPIClient:
    def __init__(self, base_url):
        self.__base_url = base_url
        self.__get_headers = {}
        self.__post_headers = {
            "Content-Type": "application/json"
        }

    #create a method to send an http post request and return the response
    #the http request will use the standard post headers
    def _post(self, endpoint, data):
        url = self.__base_url + endpoint
        return post(url, data, headers=self.__post_headers)

    #create a method to send an http get request and return the result
    #the http request will use the standard get headers
    def _get(self, endpoint, data=None, querystring=None):
        url = self.__base_url + endpoint

        if not querystring is None:
            url = url + querystring

        return get(url, data, headers=self.__get_headers)