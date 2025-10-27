from django.urls import path
from .views import ArtworkListView, ArtworkDetailView, ArtworkAPIView

app_name = 'artwork'

# Define the URL patterns for the artwork app
urlpatterns = [
    path('', ArtworkListView.as_view(), name='list'),
    path('<slug:slug>/', ArtworkDetailView.as_view(), name='detail'),
    path('api/artworks/', ArtworkAPIView.as_view(), name='api_artworks'),
]
