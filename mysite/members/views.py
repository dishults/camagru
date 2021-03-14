from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.views.generic import FormView

from members.forms import SigninForm, SignupForm, PasswordResetCustomForm, SetPasswordCustomForm

from .tokens import account_activation_token


class SigninView(FormView):
    template_name = 'members/signin.html'
    context_object_name = 'members_signin_view'
    form_class = SigninForm
    success_url = '/signin'  # galery

    def form_valid(self, form):
        if self.request.user == form.user_cache:
            messages.warning(self.request, "You've already logged in.")
        else:
            login(self.request, form.user_cache)
            messages.success(self.request, "You've logged in successfully.")
        return super().form_valid(form)


def signout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You've been logged out.")
    return redirect(SigninView.success_url)


class SignupView(FormView):
    template_name = 'members/signup.html'
    context_object_name = 'members_signup_view'
    form_class = SignupForm
    success_url = '/signup'  # galery

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(
                request, "You've already signed up and logged in.")
            return redirect(SigninView.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        EmailMessage(
            subject='Activate your account to access Camagru.',
            body=render_to_string('members/acc_active_email.html', {
                'user': user,
                'domain': get_current_site(self.request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            }),
            to=[form.cleaned_data.get('email')]
        ).send()
        messages.success(
            self.request, "You've signed up successfully. "
            + "Please confirm your email address to complete the registration")
        return super().form_valid(form)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Thank you for your email confirmation. "
            + "Now you can signin to your account.")
        return redirect('signin')
    else:
        return HttpResponse('Activation link is invalid!')


class PasswordResetCustomView(PasswordResetView):
    email_template_name = 'members/password_reset_email.html'
    form_class = PasswordResetCustomForm
    subject_template_name = 'members/password_reset_subject.txt'
    template_name = 'members/password_reset_form.html'


class PasswordResetCustomDoneView(PasswordResetDoneView):
    template_name = 'members/password_reset_done.html'


class PasswordResetCustomConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordCustomForm
    template_name = 'members/password_reset_confirm.html'


class PasswordResetCustomCompleteView(PasswordResetCompleteView):
    template_name = 'members/password_reset_complete.html'
