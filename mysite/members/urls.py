from django.urls import path

from . import views

urlpatterns = [
    path('signin', views.SigninView.as_view(), name='signin'),
    path('signout', views.signout_view, name='signout'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_reset', views.PasswordResetCustomView.as_view(),
         name='password_reset'),

    path('password_reset/done', views.PasswordResetCustomDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetCustomConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCustomCompleteView.as_view(),
         name='password_reset_complete'),
]
