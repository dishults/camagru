from django import forms

from utils import update_attrs_for_bootstrap

from .models import Comment, Like


class CommentForm(forms.ModelForm):

    comment = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 1}), max_length=450)

    class Meta:
        model = Comment
        fields = ['comment', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_attrs_for_bootstrap(self.fields, ['comment'])


class LikeForm(forms.ModelForm):

    class Meta:
        model = Like
        fields = ['image', 'user']
