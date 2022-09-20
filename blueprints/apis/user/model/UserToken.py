from datetime import datetime

class UserToken:
    def __init__(self, token, expiry_time):
        self.__token = token
        self.__expiry_time = expiry_time

    def get_token(self):
        return self.__token

    def has_expired(self):
        return datetime.now() >= self.__expiry_time

    def matches(self, token):
        if self.has_expired():
            return self.__token == token
        else:
            return False

    def serialize(self):
        return {
            "token": self.__token,
            "expiry_time": self.__expiry_time
        }