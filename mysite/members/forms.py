from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-2'}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class SignupForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-2'}))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control mb-2'}))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-2'}))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
