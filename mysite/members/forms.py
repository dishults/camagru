from django.contrib.auth.models import User
from django import forms


class ContactForm(forms.ModelForm):
    checkbox = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control mb-2'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control mb-2'
                }
            ),
        }
