from django.urls import path
from . import views


app_name = 'profiles'

# Define the URL patterns for the profiles app
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path(
        'verify-email/',
        views.VerifyEmailView.as_view(),
        name='verify_email'
        ),
    path(
        'artist-application/',
        views.ArtistApplicationView.as_view(),
        name='artist_application'
        ),
]
