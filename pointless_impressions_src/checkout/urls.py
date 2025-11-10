from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path(
        '',
        views.CheckoutView.as_view(),
        name='checkout'
    ),
    path(
        'api/cart/add/',
        views.AddToCartView.as_view(),
        name='api_add_to_cart'
    ),
    path(
        'api/cart/remove/',
        views.RemoveFromCartView.as_view(),
        name='api_remove_from_cart'
    ),
    path(
        'api/cart/update/',
        views.UpdateCartQuantityView.as_view(),
        name='api_update_cart'
    ),
    path(
        'api/cart/sync/',
        views.SyncCartView.as_view(),
        name='api_sync_cart'
    ),
    path(
        'api/cart/fetch/',
        views.CartFetchView.as_view(),
        name='api_cart_fetch'
    ),
]
