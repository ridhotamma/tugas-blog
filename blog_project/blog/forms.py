from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']