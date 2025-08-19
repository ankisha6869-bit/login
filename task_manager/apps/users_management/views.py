from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import UserManagement
from .serializers import UserManagementSerializer

class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = UserManagement.objects.filter(is_deleted=False, is_active=True)
    serializer_class = UserManagementSerializer
    lookup_field = 'username' 

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            # Fallback for non-paginated response (shouldn't occur with pagination_class set)
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "message": "User list fetched successfully.",
                "user_count": len(serializer.data),
                "users": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error fetching user list: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            partial = False
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                "message": "User updated successfully.",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error updating user: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            partial = True
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                "message": "User partially updated successfully.",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error partially updating user: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.is_deleted = True
            user.is_active = False
            user.save()
            return Response({
                "message": f"User '{user.username}' has been soft deleted."
            }, status=status.HTTP_200_OK)
        except UserManagement.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error deleting user: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
