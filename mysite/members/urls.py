from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('accounts/login/', views.SigninView.as_view(), name='login'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('settings/', login_required(views.SettingsView.as_view()), name='settings'),

    path('password_reset/', views.PasswordResetCustomView.as_view(),
         name='password_reset'),
    path('password_reset/done/', views.PasswordResetCustomDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetCustomConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCustomCompleteView.as_view(),
         name='password_reset_complete'),
]
