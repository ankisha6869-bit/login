from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the URLs from your app (e.g., named 'businesses_app')
    path('api/', include('business.urls')), # Replace 'your_app_name' with the actual name of your Django app
]