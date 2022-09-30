from ..model import User
from ..data import UserRepository


class UserService:
    def __init__(self):
        self.__repository = UserRepository()

    #Create service to register a new user
    def register_user(self, username, password_hash):
        if self.__repository.user_exists(username):
            raise Exception("The username already exists")
        
        user = User(username, password_hash)
        self.__repository.register_user(user)

    #Create service to validate user's login credentials
    def login(self, username, password_hash):
        #Check that the user exists
        if not self.__repository.user_exists(username):
            return None

        user = self.__repository.get_user(username)

        #Check that the correct password was provided
        if not user.is_recognised_password(password_hash):
            return None

        #Check that the user has a valid auth token
        #If not, refresh it
        if not user.has_valid_token():
            user.refresh_token()
            self.__repository.update_token(user)

        #Return the auth token
        return user.get_token()

    #Create service to authorize a logged-in user
    def authorize(self, username, token):
        #Check that the user exists
        if not self.__repository.user_exists(username):
            return None

        #If they do, let's get the user so we can compare tokens
        user = self.__repository.get_user(username)

        #Check whether the user's token has expired:
        #Don't authenticate a user with an expired token
        if not user.has_valid_token():
            return None
        
        #Check their token to ensure it matches
        if not user.auth_token_is_valid(token):
            return None

        #Refresh the token of authenticated users so this stays alive until
        #they have been inactive for the maximum amount of time or mroe
        user.refresh_token()
        self.__repository.update_token(user)
        return user.get_token()

        
