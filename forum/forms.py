from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "category", "content", "image"]
        exclude = ["writer"]

    def __init__(self, *args, **kwargs):
        category = kwargs.pop("category", None)
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields["category"].initial = category
