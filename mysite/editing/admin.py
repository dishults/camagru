from django.contrib import admin

from .models import Overlay

from gallery.admin import ImageAdmin


@admin.register(Overlay)
class OverlayAdmin(ImageAdmin):
    pass
