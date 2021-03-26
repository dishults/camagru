from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, FormView
from .models import Image, Like

from .forms import CommentForm


class GalleryView(ListView, FormView):
    model = Image
    paginate_by = 5
    template_name = 'gallery/homepage.html'
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        button = self.request.POST.get('button')
        if button == 'like':
            image = form.cleaned_data.get('image')
            _, created = Like.objects.get_or_create(
                image=image, user=self.request.user)
            if not created:
                try:
                    Like.objects.get(
                        image=image, user=self.request.user).delete()
                except ObjectDoesNotExist:
                    pass
        elif button == 'comment' and form.cleaned_data['comment']:
            saved = form.save(commit=False)
            saved.user = self.request.user
            saved.save()
        return super().form_valid(form)
