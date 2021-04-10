from base64 import b64decode
from io import BytesIO

from django.shortcuts import redirect, render
from django.views.generic import View
from django.core.files.images import ImageFile

from PIL import Image as PILImage

from gallery.models import Image

from .forms import ImageForm
from .models import Overlay


class EditingView(View):
    template_name = 'editing/editing.html'

    def get(self, request):
        return render(request, self.template_name, self.get_context(request))

    def post(self, request):
        # Initial variables
        image_form = ImageForm(request.POST, request.FILES)
        snapshot = request.POST.get('image_string')

        if image_form.is_valid():
            # Get headers and image if it comes from a snapshot
            try:
                headers, snapshot = snapshot.split(';base64,')
            except ValueError:
                headers, snapshot = snapshot, None

            # Get image id and overlay id
            # E.g. headers -> image:0;overlay:3;data:image/png
            try:
                # Get only image and overlay data
                image_id, overlay_id = headers.split(';')[:2]
                image_id = int(image_id.split(':')[1])
                overlay_id = int(overlay_id.split(':')[1])
            except Exception:
                pass

            # Merge image with overlay
            image = None
            try:
                if image_form.files:  # From upload
                    image = image_form.files.get('image')
                elif snapshot:  # From snapshot
                    image = BytesIO(b64decode(snapshot))
                elif image_id:  # From existing image
                    image = request.user.image_set.get(id=image_id).image

                overlay = Overlay.objects.get(id=overlay_id).image
                self.merge_image_with_overlay(
                    image, overlay, request.user)
                return self.get(request)
            except Exception:
                pass

        # Form is invalid or something went wrong
        return render(request, self.template_name,
                      self.get_context(request, image_form))

    @staticmethod
    def get_context(request, form=None):
        return {
            'images': request.user.image_set.all().order_by('-date_created'),
            'overlays': Overlay.objects.all(),
            'form': form or ImageForm(),
        }

    @staticmethod
    def merge_image_with_overlay(image, overlay, user):
        image = PILImage.open(image).convert('RGBA')
        overlay = PILImage.open(overlay).convert('RGBA')
        image.alpha_composite(overlay.resize(image.size))

        buffer = BytesIO()
        image.convert('RGB').save(buffer, format="JPEG")

        file = ImageFile(buffer)
        file = Image(image=file, user=user)
        file.image.save('snapshot.jpg', buffer)


def delete_image(request, image_id):
    # To make sure that static files will also be removed
    for image in request.user.image_set.filter(id=image_id):
        image.delete()
    return redirect('editing')
