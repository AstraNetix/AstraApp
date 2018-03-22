from django.contrib.auth import get_user_model
from passlib.context import CryptContext
from api.exceptions.user_exceptions import AuthenticationError

User = get_user_model()

class Authentication:
    def authenticate(self, request, username=None, password=None):
        """
        Attempt to authenticate a user, given a email and
        password. Return the user or return None.
        """
        try:
            return User.authenticate(email=username, password=password)
        except AuthenticationError:
            return None