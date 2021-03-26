from django.views.generic import ListView, FormView
from .models import Image

from .forms import CommentForm


class GalleryView(ListView, FormView):
    model = Image
    paginate_by = 5
    template_name = 'gallery/homepage.html'
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        saved = form.save(commit=False)
        saved.user = self.request.user
        saved.save()
        return super().form_valid(form)
