import jwt # Imports PyJWT library for JWT creation/decoding
import datetime # Imports datetime for setting token expiration times
from django.conf import settings # Imports Django settings (SECRET_KEY)
from rest_framework import serializers # Imports DRF serializers
from django.contrib.auth.hashers import check_password # Imports function to verify hashed passwords
from apps.users_management.models import UserManagement # Imports UserManagement model

class LoginSerializer(serializers.Serializer): # Defines a serializer for login input
    username = serializers.CharField() # Expects a username field
    password = serializers.CharField(write_only=True) # Expects a password field (write_only means it's not included in output)

    # Custom validation method for the entire data payload
    def validate(self, data):
        username = data.get("username") # Get username from input data
        password = data.get("password") # Get password from input data

        # Find user
        try:
            user = UserManagement.objects.get( # Try to retrieve user by username
                username=username,
                is_active=True, # User must be active
                is_deleted=False # User must not be soft-deleted
            )
        except UserManagement.DoesNotExist: # If user not found or criteria not met
            raise serializers.ValidationError("Invalid username or password") # Raise validation error

        # Check password
        if not check_password(password, user.password): # Verify provided password against hashed password
            raise serializers.ValidationError("Invalid username or password") # Raise error if password doesn't match

        # Generate tokens manually
        payload = { # Payload for the access token
            "user_id": user.id,   # DRF expects this, not "id" (common JWT claim)
            "username": user.username, # Include username
            "email": user.email, # Include email
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15), # Expiration time (15 minutes from now)
            "iat": datetime.datetime.utcnow(), # Issued at time
        }
        # Encode the access token using payload, SECRET_KEY, and HS256 algorithm
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        refresh_payload = { # Payload for the refresh token
            "user_id": user.id,   # again user_id
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7), # Expiration time (7 days from now)
            "iat": datetime.datetime.utcnow(),
        }
        # Encode the refresh token
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

        return { # Return a dictionary containing tokens and user data
            "access": access_token,
            "refresh": refresh_token,
            "user": { # Detailed user information for the response
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number,
            },
        }