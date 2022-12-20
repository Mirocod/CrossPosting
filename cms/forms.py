from django import forms
from django.contrib.auth import models as auth_models

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('body', 'link',)


class UserForm(forms.ModelForm):
    class Meta:
        model = auth_models.User
        fields = ('username', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }
