from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def validate_size(image):
    width, height = get_image_dimensions(image)
    if width > 1920 or width < 300:
        raise ValidationError(
            '%(width)s is incorrect width. It should be 300-1920 pixels',
            code='invalid',
            params={'width': width},
        )
    elif height > 1920 or height < 300:
        raise ValidationError(
            '%(height)s is incorrect height. It should be 300-1920 pixels',
            code='invalid',
            params={'height': height},
        )
