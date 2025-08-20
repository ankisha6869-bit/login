from django.db import models

class UserManagement(models.Model):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    dob = models.DateField()

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users_management'


from django.db import models
from apps.users_management.models import UserManagement

class Project(models.Model):
    project_unique_id = models.CharField(max_length=100, unique=True)
    project_name = models.CharField(max_length=255)
    username = models.ForeignKey(UserManagement,to_field='username',db_column='username', on_delete=models.CASCADE,null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'project_management'


from django.db import models
from apps.users_management.models import UserManagement

class TaskManager(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('terminated', 'Terminated'),
    ]

    # Primary key 'id' is added automatically by Django, no need to declare explicitly
    task_unique_id = models.CharField(max_length=100, unique=True)
    task_username = models.ForeignKey(UserManagement,to_field='username', on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    task_completion_date = models.CharField(max_length = 100, null = True, blank=True)
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task_name} ({self.task_unique_id})"

    class Meta:
        db_table : "task_management"

from django.db import models
from apps.tasks_management.models import TaskManager

# Create your models here.
class TaskProjectMapping(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    task_unique_id = models.ForeignKey(TaskManager,to_field='task_unique_id',db_column='task_unique_id', on_delete=models.CASCADE, related_name='task_mappings')
    project_unique_id = models.ForeignKey('Project',to_field='project_unique_id',db_column='project_unique_id', on_delete=models.CASCADE, related_name='project_mappings')

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unique_id
    
    class Meta:
        db_table: 'task_project_mapping'