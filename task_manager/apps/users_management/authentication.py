from rest_framework_simplejwt.authentication import JWTAuthentication # Base JWT authenticator
from django.contrib.auth import get_user_model # Function to get the active user model
from rest_framework.exceptions import InvalidToken, AuthenticationFailed # Exceptions for authentication errors

User = get_user_model() # Gets the currently active user model (which is UserManagement in your case)

class UsernameJWTAuthentication(JWTAuthentication): # Custom JWT authentication class
    # Overrides the method that retrieves a user from a validated token
    def get_user(self, validated_token):
        try:
            username = validated_token['username'] # Try to get 'username' from the token payload
        except KeyError: # If 'username' key is not in the token
            raise InvalidToken('Token contained no recognizable username') # Raise an error

        user = User.objects.get(username=username) # Try to get the user from the database by username
        if not user.is_active: # If the found user is not active
            raise AuthenticationFailed('User is inactive', code='user_inactive') # Raise authentication error
        return user # Return the active user object