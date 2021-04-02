from django.views.generic import View
from django.shortcuts import redirect, render

from .models import Overlay


class EditingView(View):
    template_name = 'editing/editing.html'

    def get(self, request):
        images = request.user.image_set.all().order_by('-date_created')
        overlays = Overlay.objects.all()
        context = {
            'images': images,
            'overlays': overlays,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        return super().post(request)


def delete_image(request, image_id):
    # To make sure that static files will also be removed
    for image in request.user.image_set.filter(id=image_id):
        image.delete()
    return redirect('editing')
