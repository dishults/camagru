from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm,
    PasswordResetForm, SetPasswordForm, UsernameField
)
from django.forms.models import ModelForm


def update_attrs_for_bootstrap(fields, names):
    for name in names:
        fields[name].widget.attrs.update({'class': 'form-control'})


class SigninForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_attrs_for_bootstrap(self.fields, ['username', 'password'])


class SignupForm(UserCreationForm):

    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'autocomplete': 'email'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_attrs_for_bootstrap(
            self.fields, ['username', 'email', 'password1', 'password2'])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SettingsForm(ModelForm):
    username = UsernameField(required=False)

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_attrs_for_bootstrap(
            self.fields, ['username', 'email', 'password'])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PasswordResetCustomForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_attrs_for_bootstrap(self.fields, ['email'])


class SetPasswordCustomForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_attrs_for_bootstrap(
            self.fields, ['new_password1', 'new_password2'])
