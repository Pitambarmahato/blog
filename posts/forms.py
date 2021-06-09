from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'category', 'description']


class CommentForm(forms.ModelForm):
    # comment = forms.CharField(required=True)
    class Meta:
        model = Comment
        fields = ['comment']