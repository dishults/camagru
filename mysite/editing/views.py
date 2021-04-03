from base64 import b64decode
from io import BytesIO

from django.shortcuts import redirect, render
from django.views.generic import View
from django.core.files.images import ImageFile

from gallery.models import Image

from .forms import ImageForm
from .models import Overlay


class EditingView(View):
    template_name = 'editing/editing.html'

    def get(self, request):
        return render(request, self.template_name, self.get_context(request))

    def post(self, request):
        image_form = ImageForm(request.POST, request.FILES)
        image = request.POST.get('image_string')
        if image_form.is_valid():
            # From upload
            if image_form.files:
                image = image_form.save(commit=False)
                image.user = request.user
                image.save()
            # From snapshot
            elif ';base64,' in image:
                _, image = image.split(';base64,')
                image = b64decode(image)

                buffer = BytesIO(image)
                image = ImageFile(image)

                image = Image(image=image, user=request.user)
                image.image.save('snapshot.jpg', buffer, save=True)
            else:
                return render(
                    request, self.template_name,
                    self.get_context(request, image_form)
                )
        else:
            return render(
                request, self.template_name,
                self.get_context(request, image_form)
            )
        return self.get(request)

    @staticmethod
    def get_context(request, form=None):
        return {
            'images': request.user.image_set.all().order_by('-date_created'),
            'overlays': Overlay.objects.all(),
            'form': form or ImageForm(),
        }


def delete_image(request, image_id):
    # To make sure that static files will also be removed
    for image in request.user.image_set.filter(id=image_id):
        image.delete()
    return redirect('editing')
