from django import forms
from django.forms.models import ModelForm

from utils import update_attrs_for_bootstrap
from gallery.models import Image


class ImageForm(ModelForm):

    # For upload
    image = forms.ImageField(required=False)
    # For snapshot
    image_string = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Image
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_attrs_for_bootstrap(self.fields, ['image'])
