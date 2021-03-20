from django.views.generic import ListView
from .models import Image


class GalleryView(ListView):
    model = Image
    paginate_by = 5
    template_name = 'gallery/homepage.html'
