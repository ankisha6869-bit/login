from django.urls import path
from .views import BusinessListCreateView, BusinessDetailView

urlpatterns = [
    # URL for listing all businesses and creating a new business
    # GET request to /api/businesses/ -> BusinessListCreateView.get() (list)
    # POST request to /api/businesses/ -> BusinessListCreateView.post() (create)
    path('businesses/', BusinessListCreateView.as_view(), name='business-list-create'),

    # URL for retrieving, updating, or soft-deleting a single business by its unique ID
    # GET request to /api/businesses/{unique_id}/ -> BusinessDetailView.get() (retrieve)
    # PUT request to /api/businesses/{unique_id}/ -> BusinessDetailView.put() (update)
    # DELETE request to /api/businesses/{unique_id}/ -> BusinessDetailView.delete() (soft-delete)
    # The 'pk' in the path will capture the businesses_unique_id from the URL.
    path('businesses/<str:pk>/', BusinessDetailView.as_view(), name='business-detail'),
]