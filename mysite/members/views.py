from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect

from members.forms import LoginForm, SignupForm


class LoginView(FormView):
    template_name = 'members/login.html'
    context_object_name = 'members_login_view'
    form_class = LoginForm
    success_url = '/login'  # galery

    def form_valid(self, form):
        if self.request.user == form.user_cache:
            messages.warning(self.request, "You've already logged in.")
        else:
            login(self.request, form.user_cache)
            messages.success(self.request, "You've logged in successfully.")
        return super().form_valid(form)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You've been logged out.")
    return redirect(LoginView.success_url)


class SignupView(FormView):
    template_name = 'members/signup.html'
    context_object_name = 'members_signup_view'
    form_class = SignupForm
    success_url = '/signup'  # galery

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(LoginView.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "You've signed up successfully.")
        return super().form_valid(form)
