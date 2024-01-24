from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.core.mail import send_mail
import random
from django.shortcuts import redirect, render

from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.tokens import default_token_generator as token_generator

from config.settings import EMAIL_HOST_USER
from users.forms import UserProfileForm, UserRecoveryForm, UserRegisterForm
from users.models import User
from django.core.exceptions import ValidationError

from users.utils import send_email_for_verify

class ExtraLoginView(LoginView):
    form_class = AuthenticationForm
# class LoginView(BaseLoginView):
#     template_name = 'users/login.html'
#     form_class = AuthenticationForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email')


    # def form_valid(self, form):
    #     new_user = form.save()
    #     send_mail(
    #         subject='поздравляем с регистрацией',
    #         message='вы зарегистрированы',
    #         form_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[new_user.email]
    #     )
    #     return super().form_valid(form)


    def post(self, request, **kwargs):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # email = form.cleaned_data.get('email')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('users:confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('/')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
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


# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('user_email')
#         try:
#             user = User.objects.get(email=email)
#             new_password = ''.join([str(random.randint(0, 9)) for _ in range(8)])
#             send_mail(
#                 subject='New password',
#                 message=f'Your new password {new_password}',
#                 from_email=EMAIL_HOST_USER,
#                 recipient_list=[user.email]
#             )
#             user.set_password(new_password)
#             user.save()
#             return redirect(reverse('users:login'))
#         except Exception:
#             message = 'We can not find user with this email'
#             contex = {
#                 'message': message
#             }
#             return render(request, 'users/forgot_password.html', contex)
#     else:
#         return render(request, 'users/forgot_password.html')