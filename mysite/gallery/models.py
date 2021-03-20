from django.db import models
from django.contrib.auth.models import User

from .validators import validate_size


class Image(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='images', validators=[validate_size])

    notify = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


class Comment(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)

    comment = models.CharField(max_length=450, blank=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
