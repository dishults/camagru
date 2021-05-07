from django.contrib import messages
from django.contrib.auth import login, logout, password_validation
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.views.generic import View, FormView

from utils import get_attribute

from .forms import (
    NotifyForm, SigninForm, SignupForm, SettingsForm,
    PasswordResetCustomForm, SetPasswordCustomForm
)
from .models import Member
from .tokens import account_activation_token


class SigninView(FormView):
    template_name = 'members/signin.html'
    form_class = SigninForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(
                request, "You've already signed in")
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user == form.user_cache:
            messages.warning(self.request, "You've already signed in")
        else:
            login(self.request, form.user_cache)
            messages.success(self.request, "You've signed in successfully")
        return super().form_valid(form)


def signout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You've been signed out")
    return redirect(SigninView.success_url)


class SignupView(FormView):
    template_name = 'members/signup.html'
    form_class = SignupForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(
                request, "You've already signed up and signed in")
            return redirect(SigninView.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        Member.objects.create(user=user)
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


class SettingsView(View):
    template_name = 'members/settings.html'

    def get(self, request):
        context = {
            'settings_form': SettingsForm(),
            'notify': get_attribute(request, 'user.member.notify'),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Check password first
        password = request.POST.get('password')
        if not request.user.check_password(password):
            messages.warning(request, "Invalid password")
            return self.get(request)

        # Delete profile
        if request.POST.get('settings') == 'delete':
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, "Your profile has been deleted")
            return redirect(SigninView.success_url)

        # Update notification setting
        notify_form = NotifyForm(request.POST)
        notify = get_attribute(request, 'user.member.notify')
        if notify_form.is_valid():
            notify_setting = notify_form.cleaned_data.get('notify')
            if notify is not None and notify != notify_setting:
                notify = notify_setting
                request.user.member.notify = notify
                request.user.member.save()

        # Update all other settings
        if request.POST.get('username') == request.user.username:
            POST = request.POST.copy()
            POST['username'] = ''
            settings_form = SettingsForm(POST)
        else:
            settings_form = SettingsForm(request.POST)
        if not settings_form.is_valid():
            return render(request, self.template_name,
                          {'settings_form': settings_form, 'notify': notify})

        try:
            self.set_new_password(request, settings_form)
        except ValidationError as errors:
            settings_form.add_error('new_password', errors)
            return render(request, self.template_name,
                          {'settings_form': settings_form, 'notify': notify})

        for attribute in ('username', 'email'):
            new_value = settings_form.cleaned_data.get(attribute)
            if new_value:
                setattr(request.user, attribute, new_value)

        request.user.save()
        messages.success(
            request, "You've successfully updated your profile"
        )
        return render(request, self.template_name,
                      {'settings_form': settings_form, 'notify': notify})

    def set_new_password(self, request, form):
        new_password = form.cleaned_data.get("new_password")
        confirm_password = form.cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password == confirm_password:
            password_validation.validate_password(
                new_password, request.user
            )
            request.user.set_password(new_password)
            messages.success(
                request,
                "Your password has been updated. You are now signed out."
            )
        # Both not empty
        elif not (not new_password and not confirm_password):
            raise ValidationError(
                "The two password fields didn't match."
            )


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
