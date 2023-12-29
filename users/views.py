from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.exceptions import ValidationError
from config.settings import EMAIL_HOST_USER
from users.models import User
from users.forms import UserRegisterForm, UserProfileForm, UserRecoveryForm, AuthenticationForm
from users.utils import send_email_for_verify

class ExtraLoginView(LoginView):
    form_class = AuthenticationForm
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email')

    def post(self, request, **kwargs):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('users:confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


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


@staticmethod


def get_user(uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError,
            User.DoesNotExist, ValidationError):
        user = None
    return user
