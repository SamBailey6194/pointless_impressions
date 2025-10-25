from django.urls import path
from .views import ArtworkListView

app_name = 'artwork'

# Define the URL patterns for the artwork app
urlpatterns = [
    path('', ArtworkListView.as_view(), name='list'),
]
