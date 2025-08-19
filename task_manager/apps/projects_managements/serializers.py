from pyexpat import model
from rest_framework import serializers
from .models import Project, UserManagement
from django.db import transaction
import uuid 

class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManagement
        fields = ["username"]


def generate_custom_unique_id():
        """Generate unique ID in format RES-xxxxx (5 hex digits from UUID)"""
        return f"PRO-{str(uuid.uuid4().int)[-5:]}"  # Use last 5 digits of UUID integer



class ProjectSerializer(serializers.Serializer):
    project_unique_id = serializers.CharField(read_only = True)
    project_name = serializers.CharField(required = True, max_length = 50)
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset = UserManagement.objects.filter(is_deleted = False),
        required = True,
        allow_null = False,
        error_messages = {"Required": "Username is a required field"}
        )

    is_active = serializers.BooleanField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)

    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    def validate_project_name(self, value):
        if Project.objects.filter(project_name = value):
            raise serializers.ValidationError({"Project Name": "Project Name already Exists"})
        return value

    def validate_username(self, value):
        if UserManagement.objects.filter(username = value):
            return value
        else : 
            raise serializers.ValidationError("Username does not exists")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                project_unique_id = generate_custom_unique_id()
                project = Project.objects.create(
                    project_unique_id = project_unique_id,
                    project_name = validated_data.get('project_name'),
                    user = validated_data.get('user'),
                    )
                return project
        except Exception as e:
            raise serializers.ValidationError(f"Unable to create Object {str(e)}")
        

    def update(self, instance, validated_data):
       
        for keys, values in validated_data.items():
            setattr(instance, keys, values)
            instance.save()
        return instance