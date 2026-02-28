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
        'resend-verification-code/',
        views.ResendVerificationCodeView.as_view(),
        name='resend_verification_code'
    ),
]
