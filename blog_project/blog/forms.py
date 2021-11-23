from django import forms
from django.db.models import fields

from .models import Category, Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'intro', 'body', 'category', 'priority', 'image')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)