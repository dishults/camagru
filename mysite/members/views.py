from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import FormView

from members.forms import LoginForm, SignupForm


class LoginView(FormView):
    template_name = 'members/login.html'
    context_object_name = 'members_login_view'
    form_class = LoginForm
    success_url = '/login'

    def form_valid(self, form):
        login(self.request, form.user_cache)
        messages.success(self.request, "You've logged in successfully.")
        return super().form_valid(form)


class SignupView(FormView):
    template_name = 'members/signup.html'
    context_object_name = 'members_signup_view'
    form_class = SignupForm
    success_url = '/signup'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "You've signed up successfully.")
        return super().form_valid(form)
