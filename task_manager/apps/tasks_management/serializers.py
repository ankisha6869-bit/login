from rest_framework import serializers
from apps.tasks_management.models import TaskManager
from apps.users_management.models import UserManagement
from django.db import transaction
import uuid



class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManagement
        fields = ["username"]



def generate_custom_unique_id():
        """Generate unique ID in format RES-xxxxx (5 hex digits from UUID)"""
        return f"Task-{str(uuid.uuid4().int)[-5:]}"  # Use last 5 digits of UUID integer
        


class TaskManagerSerializer(serializers.ModelSerializer):
    task_unique_id = serializers.CharField(max_length = 35, read_only = True, allow_blank = False, allow_null = False)
    task_username = serializers.SlugRelatedField(
        slug_field='username',
        queryset = UserManagement.objects.filter(is_deleted = False),
        required = True,
        allow_null = False,
        error_messages = {"Required": "Username is a required field"}
        )
    task_name = serializers.CharField(max_length = 255, allow_blank = False, allow_null = False, required = True)
    task_completion_date = serializers.DateField(required = True)
    task_status = serializers.CharField(max_length = 20, default = 'pending')
    is_active = serializers.BooleanField(default=True)
    is_deleted = serializers.BooleanField(default=False)

    class Meta:
        model = TaskManager
        fields = ['task_unique_id', 'task_username', 'task_name', 'task_completion_date', 'task_status', 'is_active', 'is_deleted']
        read_only_fields = ['task_unique_id']

        def validate_task_username(self, value):
            if not UserManagement.objects.filter(username=value).exists():
                raise serializers.ValidationError("User does not exist.")
            return value

        def validate_task_name(self, value):
            if value.strip() == "":
                raise serializers.ValidationError("Task name cannot be empty.")
            
            return value
        
        def validate_task_status(self, value):
            if value not in dict(TaskManager.STATUS_CHOICES).keys():
                raise serializers.ValidationError("Invalid task status.")
            return value


    #Make sure to handle create and update outside the class Meta
    def create(self, validated_data):
            
        try:
            with transaction.atomic():
                task_unique_id_custom = generate_custom_unique_id()
                # Check if task with the same unique ID already exists

                task_username = validated_data.get('task_username')
                task_name = validated_data.get('task_name')
                
                if TaskManager.objects.filter(task_username = task_username, task_name = task_name, is_deleted = False).exists():
                    raise serializers.ValidationError("This user already has a task with this name")

                else:
                    create_task = TaskManager.objects.create(
                    task_unique_id = task_unique_id_custom,
                    task_username = validated_data['task_username'],
                    task_name = validated_data['task_name'],
                    task_completion_date = validated_data['task_completion_date'],
                    task_status = validated_data['task_status'],
                    )
                return create_task
        except Exception as e:
            raise serializers.ValidationError(f'Error Creating task: {str(e)}')
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():

                task_username = validated_data.get('task_username')
                task_name = validated_data.get('task_name')
                
                if TaskManager.objects.filter(task_username = task_username, task_name = task_name, is_deleted = False).exists():
                    raise serializers.ValidationError("This user already has a task with this name")


                for keys, value in validated_data.items():
                    setattr(instance, keys, value)
                    instance.save()
                return instance
        except Exception as e:
            raise serializers.ValidationError(f"Error Updating Task: {str(e)}")
        