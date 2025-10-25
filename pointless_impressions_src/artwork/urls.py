from django.urls import path
from .views import ArtworkListView, ArtworkDetailView

app_name = 'artwork'

# Define the URL patterns for the artwork app
urlpatterns = [
    path('', ArtworkListView.as_view(), name='list'),
    path('<int:pk>/', ArtworkDetailView.as_view(), name='detail'),
]
