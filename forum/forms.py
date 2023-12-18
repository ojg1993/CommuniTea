from django import forms
from django.forms import TextInput

from .models import Post, Comment


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "category", "content", "image"]
        exclude = ["writer"]

    def __init__(self, *args, **kwargs):
        category = kwargs.pop("category", None)
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields["category"].initial = category


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"style": "width: 365px; height: 100px;"}),
        }
        labels = {"content": ""}
