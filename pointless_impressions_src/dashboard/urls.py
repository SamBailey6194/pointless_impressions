from django.urls import path
from . import views


app_name = 'dashboard'

# Define the URL patterns for the dashboard app
urlpatterns = [
    path('', views.DashboardLandingView.as_view(), name='landing'),
    path(
        'user-profile/<uuid:public_id>/',
        views.UserProfileDashboardView.as_view(),
        name='user_profile_dashboard',
    ),
    path(
        'admin-dashboard/<uuid:public_id>/',
        views.AdminDashboardView.as_view(),
        name='admin_dashboard',
    ),
    path(
        'admin-dashboard/<uuid:public_id>/edit-artwork/<int:artwork_id>/',
        views.EditArtworkModalView.as_view(),
        name='edit_artwork_modal'
    ),
    path(
        'admin-dashboard/<uuid:public_id>/add-artwork/',
        views.AddArtworkModalView.as_view(),
        name='add_artwork_modal'
    ),
]
