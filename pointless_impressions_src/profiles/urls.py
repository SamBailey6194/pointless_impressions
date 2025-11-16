from django.urls import path
from . import views

# Define the URL patterns for the home app
urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
]
