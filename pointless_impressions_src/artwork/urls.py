from django.urls import path
from .views import ArtworkListView


# Define the URL patterns for the home app
urlpatterns = [
    path('', ArtworkListView.as_view(), name='artwork'),
]
