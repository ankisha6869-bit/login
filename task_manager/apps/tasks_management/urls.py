from django.urls import path
from rest_framework import routers
from apps.tasks_management.views import TaskManagerView, TaskManagerViewUserFilter,TaskUserFilterView

router = routers.SimpleRouter()
router.register(r'tasks', TaskManagerView)
router.register(r'task-user', TaskManagerViewUserFilter, basename='user')


urlpatterns = router.urls


urlpatterns += [
    path('task-user-filter/', TaskUserFilterView.as_view(), name='task-user-filter'),
]