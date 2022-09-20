from uuid import uuid4
from hashlib import sha256
from datetime import datetime, timedelta
from .UserToken import UserToken
from werkzeug.security import check_password_hash

class User:
    def __init__(self, username, password_hash, id=None, current_token=None):
        self.__id = id
        self.__username = username
        self.__password_hash = password_hash
        self.__current_token = current_token

    def get_username(self):
        return self.__username

    def is_recognised_password(self, password):
        return check_password_hash(self.__password_hash, password)

    def user_has_valid_token(self):
        if self.__current_token == None or self.__current_token.has_expired():
            return False
        return True

    def auth_token_is_valid(self, token):
        if not self.user_has_valid_token():
            return False
        return self.__current_token.matches(token)

    def refresh_token(self):
        if self.__current_token.has_expired() or self.__current_token == None:
            token = sha256(str(uuid4().hex)).hexdigest
            expiry_time = datetime.now() + timedelta(hours=1)
            self.__current_token = UserToken(token, expiry_time)

    def get_token(self):
        return self.__current_token.get_token()

    def serialize(self):
        if self.__current_token == None:
            current_token = None
        else:
            current_token = self.__current_token.serialize()
        return {
            "id": str(self.__id),
            "username": self.__username,
            "password": self.__password_hash,
            "current_token": current_token
        }