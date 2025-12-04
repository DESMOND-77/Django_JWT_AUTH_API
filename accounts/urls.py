from django.urls import path

from .auth.views import (UserLoginView,UserRegistrationView,TokenRefreshView,ValidateTokenView,LogOutView)
from .profile.views import UserProfileView
from .verification.views import (VerifyEmailView,SendVerificationEmailView,CheckVerificationStatusView,PasswordResetView,ConfirmPasswordResetView)

app_name = 'accounts'
urlpatterns = [
    # Auth
    path('auth/register/',UserRegistrationView.as_view(),name='register'),
    path('auth/login/',UserLoginView.as_view(),name='login'),
    path('auth/logout/', LogOutView.as_view(), name='logout'),
    
    # token
    path('auth/token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path('auth/token/validate/', ValidateTokenView.as_view(), name='validate_token'),
    
    # Profile routes
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # verification routes
    path('auth/email-verify/', VerifyEmailView.as_view(), name='verify_email'),
    path('auth/send-verification/', SendVerificationEmailView.as_view(), name='send_verification'),
    path('auth/verification-status/', CheckVerificationStatusView.as_view(), name='check_verification'),
    
    # password reset
    path('auth/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/', ConfirmPasswordResetView.as_view(), name='confirm_password_reset'),
   ]       