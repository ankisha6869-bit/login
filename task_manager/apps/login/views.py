from rest_framework.views import APIView # Imports base APIView class
from rest_framework.response import Response # Imports DRF Response class
from rest_framework import status # Imports HTTP status codes
from .serializers import LoginSerializer # Imports LoginSerializer

class LoginView(APIView): # Defines an API view for login
    def post(self, request): # Handles POST requests to the login endpoint
        serializer = LoginSerializer(data=request.data) # Initialize serializer with request data
        if serializer.is_valid(): # Validate the serializer data
            data = serializer.validated_data # Get the validated data (tokens and user info)

            response = Response({ # Create a DRF Response object
                "message": "Login successful",
                "user": data["user"], # Include user details
                "access": data["access"], # Include access token
                "refresh": data["refresh"] # Include refresh token
            }, status=status.HTTP_200_OK) # Set HTTP status to 200 OK

            # Optionally set tokens in HttpOnly cookies
            # Set access token as an HttpOnly cookie
            response.set_cookie(
                key="access_token", # Cookie name
                value=data["access"], # Cookie value
                httponly=True, # Make cookie inaccessible to client-side scripts (security)
                secure=False,  # Set True in production (only send over HTTPS)
                samesite="Lax" # Protect against CSRF attacks
            )
            # Set refresh token as an HttpOnly cookie
            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                httponly=True,
                secure=False,
                samesite="Lax"
            )
            return response # Return the response with tokens and cookies

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Return validation errors if not valid

class LogoutView(APIView): # Defines an API view for logout
    def post(self, request): # Handles POST requests to the logout endpoint
        response = Response( # Create a DRF Response object
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token") # Delete the access_token cookie
        response.delete_cookie("refresh_token") # Delete the refresh_token cookie
        return response # Return the response