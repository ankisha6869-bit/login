from django.urls import path
from . import views


from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', views.ProjectViewSet)
router.register(r'products-user', views.ProductViewsetUser, basename='user')
urlpatterns = router.urls

