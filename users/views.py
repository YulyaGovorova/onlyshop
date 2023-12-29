from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetConfirmView, PasswordResetView
from django.contrib.auth.views import LoginView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.tokens import default_token_generator as token_generator
from config import settings
from config.settings import EMAIL_HOST_USER
from users.forms import UserForm, UserProfileForm, UserRecoveryForm
from users.models import User
from django.core.exceptions import ValidationError

class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass

class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('user:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией',
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)

class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('/')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:

            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user

class PasswordRecoveryView(PasswordResetView):
    template_name = 'users/restore_pass.html'
    email_template_name = 'users/reset_email.html',
    success_url = reverse_lazy('users:login')
    from_email = EMAIL_HOST_USER
    form_class = UserRecoveryForm



class PasswordResetView(PasswordResetConfirmView):
    post_reset_login = True
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy('users:login')