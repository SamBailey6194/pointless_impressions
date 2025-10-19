from django.urls import path
from .views import HomeView

# Define the URL patterns for the home app
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
