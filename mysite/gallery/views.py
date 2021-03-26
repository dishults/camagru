from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.views.generic import ListView, FormView

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Image, Like
from .forms import CommentForm


class GalleryView(ListView, FormView):
    model = Image
    paginate_by = 5
    template_name = 'gallery/homepage.html'
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        image = form.cleaned_data.get('image')
        button = self.request.POST.get('button')
        if button == 'like':
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
            if image and image.user != self.request.user and image.user.email:
                EmailMessage(
                    subject='New picture comment',
                    body=render_to_string('gallery/notify.html', {
                        'image': image,
                        'from_user': self.request.user,
                        'domain': get_current_site(self.request).domain,
                    }),
                    to=[image.user.email]
                ).send()
        return super().form_valid(form)
