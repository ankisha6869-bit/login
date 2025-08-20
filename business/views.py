from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from .models import Business
from .serializers import BusinessSerializer

class BusinessListCreateView(APIView):
    """
    API view to list all businesses or create a new business.
    """

    def get(self, request):
        """
        Retrieves a list of all active (not deleted) business records.
        """
        # Filter out businesses that are marked as deleted
        businesses = Business.objects.filter(businesses_is_deleted=False)
        # Serialize the queryset of businesses. `many=True` indicates it's a list of objects.
        serializer = BusinessSerializer(businesses, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": "Fetched business records successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        """
        Creates a new business record.
        """
        # Initialize the serializer with the request data.
        # No context for `request` is needed here since `UserDataValidationMixin` was removed
        # and no other serializer logic relies on request context for created/updated by fields.
        serializer = BusinessSerializer(data=request.data)
        
        # Validate the incoming data against the serializer's rules
        if serializer.is_valid():
            # If valid, save the new business object to the database.
            # The serializer's create() method will be called.
            serializer.save()
            return Response({
                "success": True,
                "status": 201,
                "message": "Business created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        # If validation fails, prepare a detailed error response.
        # It tries to get the first error field and its message for a more user-friendly error.
        error_field = list(serializer.errors.keys())[0] if serializer.errors else "unknown"
        error_message = serializer.errors[error_field][0] if serializer.errors else "Invalid input"

        return Response({
            "success": False,
            "status": 400,
            "message": "Invalid input",
            "error_field": error_field,
            "error": error_message
        }, status=status.HTTP_400_BAD_REQUEST)


class BusinessDetailView(APIView):
    """
    API view to retrieve, update, or soft-delete a single business record.
    """

    def get_object(self, pk):
        """
        Helper method to retrieve a single Business instance by its unique ID.
        Checks for `businesses_is_deleted=False` to ensure only active records are fetched.
        """
        try:
            return Business.objects.get(businesses_unique_id=pk, businesses_is_deleted=False)
        except Business.DoesNotExist:
            # If no business matches the criteria, return None
            return None

    def get(self, request, pk):
        """
        Retrieves a single business record by its unique ID.
        """
        # Attempt to get the business object
        business = self.get_object(pk)
        if not business:
            # If the business is not found (or is deleted), return a 404 Not Found response
            return Response({
                "success": False,
                "status": 404,
                "error": "Business not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Serialize the retrieved business object
        serializer = BusinessSerializer(business)
        return Response({
            "success": True,
            "status": 200,
            "message": "Fetched business successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        """
        Updates an existing business record by its unique ID.
        Supports partial updates (`partial=True`).
        """
        # Attempt to get the business object to update
        business = self.get_object(pk)
        if not business:
            return Response({
                "success": False,
                "status": 404,
                "error": "Business not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Initialize the serializer with the existing business instance and the new data.
        # `partial=True` allows for incomplete updates (e.g., only sending one field to update).
        serializer = BusinessSerializer(business, data=request.data, partial=True)
        
        # Validate the incoming data
        if serializer.is_valid():
            # If valid, save the updated business object to the database.
            # The serializer's update() method will be called.
            serializer.save()
            return Response({
                "success": True,
                "status": 200,
                "message": "Business updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        # If validation fails, prepare a detailed error response.
        error_message = list(serializer.errors.values())[0][0] if serializer.errors else "Invalid input"
        return Response({
            "success": False,
            "status": 400,
            "error": error_message
        }, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request, pk):
        """
        Soft-deletes a business record by its unique ID.
        It marks `businesses_is_deleted` to True instead of physically removing the record.
        """
        # Attempt to get the business object to delete
        business = self.get_object(pk)
        if not business:
            return Response({
                "success": False,
                "status": 404,
                "error": "Business not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Perform a soft delete by setting the `businesses_is_deleted` flag to True
        business.businesses_is_deleted = True
        business.save()

        # If there were related models that also needed soft-deletion (like CandidateSkill
        # in your example), you would add similar logic here.
        # For example:
        # RelatedModel.objects.filter(related_business=business, is_deleted=False).update(is_deleted=True)

        return Response({
            "success": True,
            "status": 200,
            "message": "Business soft-deleted successfully"
        }, status=status.HTTP_200_OK)