from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm as Auth, PasswordResetForm
from django.core.exceptions import ValidationError

from catalog.forms import StyleFormMixin
from users.models import User
from users.utils import send_email_for_verify


class AuthenticationForm(Auth):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )


            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                if not self.user_cache.email_verify:
                    send_email_for_verify(self.request, self.user_cache)
                    raise ValidationError(
                        'Email not verify, check your email',
                        code='invalid_login',
                    )
                else:
                    self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserRecoveryForm(StyleFormMixin, PasswordResetForm):
    email = forms.EmailField(max_length=100)