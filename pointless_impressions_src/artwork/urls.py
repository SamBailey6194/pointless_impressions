from django.urls import path
from .views import ArtworkListView


# Define the URL patterns for the artwork app
urlpatterns = [
    path('', ArtworkListView.as_view(), name='artwork'),
]
