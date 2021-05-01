from django.urls import path
from django.views.generic import RedirectView

from utils import login_required

from . import views

urlpatterns = [
    # Has to be without a trailing slash so that static thumbs and overlays load properly
    path('editing', login_required(views.EditingView.as_view()), name='editing'),
    path('editing/', RedirectView.as_view(pattern_name='editing', permanent=True)),
    path('delete/<int:image_id>/', login_required(views.delete_image),
         name='delete_image'),
]
