from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path(
        '',
        views.CheckoutView.as_view(),
        name='checkout'
    ),
    path(
        'cart-dropdown/',
        views.CartDropdownView.as_view(),
        name='cart_dropdown'
    ),
]
