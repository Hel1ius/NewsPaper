from django import forms
from django.forms.widgets import HiddenInput

from .models import Comment, Post, Newsletter


# Форма создания комментариев
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'content')


# Форма создания постов, обязательное поле author заполняется автоматически через post во Views
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('chapter', 'categories', 'header', 'content', 'billboard')


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('email', )