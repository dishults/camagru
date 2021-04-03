from io import BytesIO
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PILImage

from .validators import validate_size


class Image(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(
        upload_to='static/images', validators=[validate_size])

    thumbnail = models.ImageField(
        upload_to='static/thumbnails', null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.image.name

    def create_thumbnail(self):
        image = PILImage.open(self.image)
        image.thumbnail(size=(310, 230))
        image_file = BytesIO()
        image.save(image_file, image.format)
        path = self.image.name.split('/')[-1]
        self.thumbnail.save(
            path,
            # file, field_name, name, content_type, size, charset, content_type_extra=None
            InMemoryUploadedFile(
                file=image_file,
                field_name=None,
                name='',
                content_type='image/jpeg',
                size=image.size,
                charset=None,
            ),
            save=False,
        )
        super().save(force_update=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:
            self.create_thumbnail()

    def delete(self, *args, **kwargs):
        deleted = super().delete(*args, **kwargs)
        try:
            self.image.delete(save=False)
            self.thumbnail.delete(save=False)
        except Exception:
            pass
        return deleted


class Comment(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)

    comment = models.CharField(max_length=450, blank=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}: {self.comment}"


class Like(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}: {self.image}"
