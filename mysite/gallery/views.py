from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string

from utils import get_attribute, Paginator
from views import FormView

from .models import Image, Like
from .forms import CommentForm


class GalleryView(FormView):
    model = Image
    paginate_by = 5
    template_name = 'gallery/homepage.html'
    form_class = CommentForm
    success_url = '/'

    def get(self, request, form=None):
        number = int(request.GET.get('page', 1))
        if not hasattr(self, 'paginated'):
            queryset = self.model.objects.all()
            self.paginated = Paginator(queryset, self.paginate_by)
        context = {
            'form': form or self.form_class(),
            'page_obj': self.paginated.page(number),
        }
        return render(request, self.template_name, context)

    def form_valid(self, form):
        image = form.cleaned_data.get('image')
        user = self.request.user
        button = self.request.POST.get('button')
        if button == 'like':
            _, created = Like.objects.get_or_create(
                image=image, user=user)
            if not created:
                try:
                    Like.objects.get(
                        image=image, user=user).delete()
                except ObjectDoesNotExist:
                    pass
        elif button == 'comment' and form.cleaned_data['comment']:
            saved = form.save(commit=False)
            saved.user = user
            saved.save()
            if get_attribute(image, 'user.email') and image.user != user\
                    and get_attribute(image, 'user.member.notify'):
                EmailMessage(
                    subject='New picture comment',
                    body=render_to_string('gallery/notify.html', {
                        'image': image,
                        'from_user': user,
                        'domain': get_current_site(self.request).domain,
                    }),
                    to=[image.user.email]
                ).send()
        self.success_url += f'/#{image.id}'
        return super().form_valid(form)
