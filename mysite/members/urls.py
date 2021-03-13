from django.urls import path

from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
