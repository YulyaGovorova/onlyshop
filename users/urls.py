from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.urls import path

from django.views.generic import TemplateView
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, EmailVerify, PasswordRecoveryView, ExtraLoginView

app_name = UsersConfig.name




urlpatterns = [
    path('recovery/', PasswordRecoveryView.as_view(template_name='users/restore_pass.html'), name='recovery'),
    path('login/', ExtraLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm_email/', TemplateView.as_view(template_name='users/confirm_email.html'),
         name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'),
         name='invalid_verify'),
    path('reset/<uidb64>/<token>/', PasswordResetView.as_view(), name='reset'),

]