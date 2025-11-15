from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path(
        'confirmation/',
        views.OrderConfirmationView.as_view(),
        name='confirmation'
    ),
    path(
        'success/<uuid:order_id>/',
        views.OrderSuccessView.as_view(),
        name='order_success'
    ),
]
