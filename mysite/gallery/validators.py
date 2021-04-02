from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def validate_size(image):
    minimum, maximum = 300, 1920
    width, height = get_image_dimensions(image)
    if width < minimum or width > maximum:
        raise ValidationError(
            '%(width)s is incorrect width. It should be %(minimum)s-%(maximum)s pixels',
            params={'width': width, 'minimum': minimum, 'maximum': maximum},
        )
    elif height < minimum or height > maximum:
        raise ValidationError(
            '%(height)s is incorrect height. It should be %(minimum)s-%(maximum)s pixels',
            params={'height': height, 'minimum': minimum, 'maximum': maximum},
        )
