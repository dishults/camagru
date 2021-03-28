from django.views.generic import View
from django.shortcuts import render
from django.core.paginator import Paginator

from gallery.models import Image
from .models import Overlay


class EditingView(View):
    template_name = 'editing/editing.html'

    def get(self, request):
        images = Image.objects.filter(
            user=request.user).order_by('-date_created')
        overlays = Overlay.objects.all()
        context = {
            'images': images,
            'overlays': overlays,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        return super().post(request)
