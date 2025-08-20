from itertools import product
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    lookup_field = 'project_unique_id'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        custom_response = {
            "count": queryset.count(),
            "status": "success",
            "message": "Projects retrieved successfully",
            "data": serializer.data
        }
        return Response(custom_response, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()   #  automatically assigns request.user in serializer
            return Response({
                "status": "success",
                "message": "Project created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "message": "Project updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_deleted = True
        project.save()
        return Response({
            "status": "success",
            "message": "Project deleted successfully",
            "data": {
                "project_unique_id": project.project_unique_id,
                "project_name": project.project_name
            }
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(project)
        return Response({
            "status": "success",
            "message": "Project retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)



    def retrieve(self, request, *args, **kwargs):
        # Get the project using project_unique_id (handled automatically by lookup_field)
        project = self.get_object()
    
        serializer = self.get_serializer(project)
    
        custom_response = {
            "status": "success",
            "message": "Project retrieved successfully",
            "data": serializer.data
        }
        return Response(custom_response, status=status.HTTP_200_OK)



from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ProductViewsetUser(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    
    # Remove lookup_field since we'll handle user lookup via custom action
    # lookup_field = 'user'  # This won't work well for one-to-many relationships

    @action(detail=False, methods=['get'], url_path='user/(?P<username>[^/.]+)')
    def get_by_user(self, request, username=None):
        """
        Retrieve all projects for a specific user
        Example: /api/products-user/alice/
        """
        try:
            # Get all projects for the specified username
            projects = Project.objects.filter(
                user__username=username,
                is_deleted=False
            )
            
            # Paginate the results
            page = self.paginate_queryset(projects)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(projects, many=True)
            
            return Response({
                "status": "success",
                "message": f"Found {projects.count()} projects for user {username}",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to retrieve projects",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)