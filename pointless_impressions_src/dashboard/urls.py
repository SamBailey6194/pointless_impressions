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
        'user-profile/<uuid:order_id>/order/update/',
        views.UpdateOrderView.as_view(),
        name='order_update',
    ),
    path(
        'user-profile/<uuid:order_id>/order/delete/',
        views.DeleteOrderView.as_view(),
        name='order_delete',
    ),
    path(
        'admin-dashboard/<uuid:public_id>/',
        views.AdminDashboardView.as_view(),
        name='admin_dashboard',
    ),
    path(
        'admin-dashboard/<uuid:public_id>/edit-artwork/<slug:artwork_slug>/',
        views.EditArtworkModalView.as_view(),
        name='edit_artwork_modal'
    ),
    path(
        'admin-dashboard/<uuid:public_id>/delete-artwork/<slug:artwork_slug>/',
        views.DeleteArtworkModalView.as_view(),
        name='delete_artwork_modal'
    ),
    path(
        'admin-dashboard/<uuid:public_id>/add-artwork/',
        views.AddArtworkModalView.as_view(),
        name='add_artwork_modal'
    ),
    path(
        'admin-dashboard/<uuid:public_id>/edit-order/<uuid:order_id>/',
        views.EditOrderModalView.as_view(),
        name='edit_order_modal'
    ),
    path(
        'admin-dashboard/<uuid:public_id>/delete-order/<uuid:order_id>/',
        views.DeleteOrderModalView.as_view(),
        name='delete_order_modal'
    ),
    path(
        'guest-order/<uuid:order_id>/',
        views.GuestOrderView.as_view(),
        name='guest_order',
    ),
]
