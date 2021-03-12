from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import FormView

from members.forms import ContactForm
from django.views.generic.edit import FormView


class LoginView(FormView):
    template_name = 'members/login.html'
    context_object_name = 'members_login_view'
    form_class = ContactForm
    success_url = '/members/login'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if form.cleaned_data.get('checkbox'):
            form.save()
        return super().form_valid(form)
