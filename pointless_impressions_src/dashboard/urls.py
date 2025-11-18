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
        'user-profile/change-password/',
        views.ChangePasswordView.as_view(),
        name='change_password'
    ),
    path(
        'user-profile/edit-user-info/',
        views.EditUserInfoView.as_view(),
        name='edit_user_info'
    ),
    path(
        'user-profile/change-profile-pic/',
        views.ChangeProfilePictureView.as_view(),
        name='change_profile_pic'
    ),
    path(
        'user-profile/edit-order/<int:order_id>/',
        views.CombinedOrderView.as_view(),
        name='edit_order'
    ),
    path(
        'user-profile/edit-address/<int:address_id>/',
        views.EditAddressView.as_view(),
        name='edit_address'
    ),
    path(
        'user-profile/add-address/',
        views.EditAddressView.as_view(),
        name='add_address'
    ),
    path(
        'artist-dashboard/<uuid:public_id>/',
        views.ArtistDashboardView.as_view(),
        name='artist_dashboard'
    ),
    path(
        'artist-dashboard/edit-artwork/<int:artwork_id>/',
        views.EditArtworkModalView.as_view(),
        name='edit_artwork_modal'
    ),
    path(
        'artist-dashboard/add-artwork/',
        views.AddArtworkModalView.as_view(),
        name='add_artwork_modal'
    ),
    path('admin-dashboard/<uuid:public_id>/',
         views.AdminDashboardView.as_view(),
         name='admin_dashboard'),
    path(
        'admin-dashboard/<uuid:public_id>/order-processing/',
        views.OrderProcessingView.as_view(),
        name='order_processing'
    ),
    path(
        (
            'admin-dashboard/<uuid:public_id>/'
            'order-processing/<uuid:order_id>/modal/'
        ),
        views.OrderProcessingModalView.as_view(),
        name='order_processing_modal'
    ),
    path(
        'admin-dashboard/<uuid:public_id>/manage-artists/',
        views.ManageArtistsView.as_view(),
        name='manage_artists'
    ),
    path(
        'admin-dashboard/<uuid:public_id>/artwork-approval/<int:artwork_id>/',
        views.ArtworkApprovalView.as_view(),
        name='approve_artwork'
    ),
]
