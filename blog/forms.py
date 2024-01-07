from django import forms
from .models import Comment, Reply, Post, Profile

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

from django import forms
from tinymce.widgets import TinyMCE
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))  # Use TinyMCE widget for the content field

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
