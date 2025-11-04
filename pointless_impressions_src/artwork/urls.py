from django.urls import path
from . import views

app_name = 'artwork'

# Define the URL patterns for the artwork app
urlpatterns = [
    path('', views.ArtworkListView.as_view(), name='list'),
    path('<slug:slug>/', views.ArtworkDetailView.as_view(), name='detail'),
    path('api/artworks/', views.ArtworkAPIView.as_view(), name='api_artworks'),
    # ⚠️  DEVELOPMENT ONLY - Test data setup endpoint
    path(
        'api/setup-test-data/',
        views.setup_test_data,
        name='setup_test_data'
    ),
]
