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
        image = request.POST.get('image_string')

        if image_form.is_valid():
            # Get headers and image if it comes from a snapshot
            try:
                headers, image = image.split(';base64,')
            except ValueError:
                headers, image = image, None

            # Get image id and overlay ids
            # E.g. headers -> image:0;overlays:0,3;data:image/png
            try:
                # Get only image and overlays data
                image_id, overlay_ids = headers.split(';')[:2]
                # Get number and convert it
                image_id = int(image_id.split(':')[1])
                # Get numbers
                overlay_ids = overlay_ids.split(':')[1]
                # Convert numbers and disregard the first one which is always 0
                overlay_ids = [int(o) for o in overlay_ids.split(',')][1:]
            except Exception:
                return render(request, self.template_name,
                              self.get_context(request, image_form))

            # From upload
            if image_form.files:
                # TODO: superpose the images
                image = image_form.save(commit=False)
                image.user = request.user
                image.save()
                return self.get(request)

            # From snapshot
            elif image:
                image = BytesIO(b64decode(image))
                image = PILImage.open(image)
                self.superpose_images(image, overlay_ids, request.user)
                return self.get(request)

            # From existing image
            elif image_id:
                original = request.user.image_set.get(id=image_id)
                original = PILImage.open(original.image).convert('RGBA')
                self.superpose_images(original, overlay_ids, request.user)
                return self.get(request)

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
    def superpose_images(original, overlay_ids, user):
        buffer = BytesIO()
        overlays = Overlay.objects.filter(id__in=overlay_ids)

        for overlay in overlays:
            overlay = PILImage.open(overlay.image).convert('RGBA')
            original.alpha_composite(overlay.resize(original.size))

        image = ImageFile(original.tobytes())
        original.convert('RGB').save(buffer, format="JPEG")
        image = Image(image=image, user=user)
        image.image.save('snapshot.jpg', buffer)


def delete_image(request, image_id):
    # To make sure that static files will also be removed
    for image in request.user.image_set.filter(id=image_id):
        image.delete()
    return redirect('editing')
