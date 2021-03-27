from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('editing', login_required(views.EditingView.as_view()), name='editing'),
]
