from django.db import models
from apps.tasks_management.models import TaskManager

# Create your models here.
class TaskProjectMapping(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    task_unique_id = models.ForeignKey(TaskManager,to_field='task_unique_id', on_delete=models.CASCADE, related_name='task_mappings')
    project_unique_id = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='project_mappings')

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unique_id
    
    class Meta:
        db_table: 'task_project_mapping'