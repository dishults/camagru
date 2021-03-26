from django.forms.models import ModelForm

from utils import update_attrs_for_bootstrap

from .models import Comment, Like


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['comment', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_attrs_for_bootstrap(self.fields, ['comment'])


class LikeForm(ModelForm):

    class Meta:
        model = Like
        fields = ['image', 'user']
