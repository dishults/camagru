from django.http import FileResponse, Http404
from django.views.generic import ListView
from .models import Image


class GalleryView(ListView):
    model = Image
    paginate_by = 5
    template_name = 'gallery/homepage.html'


def show_image(requiest, image):
    try:
        return FileResponse(open(f'images/{image}', 'rb'))
    except FileNotFoundError:
        raise Http404("Image does not exist")
