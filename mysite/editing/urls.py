from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('editing', login_required(views.EditingView.as_view()), name='editing'),
    path('delete/<int:image_id>', login_required(views.delete_image),
         name='delete_image'),
]
