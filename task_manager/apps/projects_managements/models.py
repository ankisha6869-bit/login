from django.db import models
from apps.users_management.models import UserManagement

class Project(models.Model):
    project_unique_id = models.CharField(max_length=100, unique=True)
    project_name = models.CharField(max_length=255)
    user = models.ForeignKey(
        UserManagement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='user',  # Maps to your VARCHAR column
        to_field='username'  # References the username field
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_management'

