from django.db import models

from gallery.validators import validate_size


class Overlay(models.Model):

    image = models.ImageField(
        upload_to='static/overlays', validators=[validate_size])

    def __str__(self):
        return self.image.name

    def delete(self, *args, **kwargs):
        deleted = super().delete(*args, **kwargs)
        try:
            self.image.delete(save=False)
        except Exception:
            pass
        return deleted
