from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.urls import path

from django.views.generic import TemplateView
from users.apps import UsersConfig


app_name = UsersConfig.name




urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),


]