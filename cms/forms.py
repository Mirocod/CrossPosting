from django import forms
from django.contrib.auth import models as auth_models

from .models import Article


class ArticleForm(forms.ModelForm):
    link_widget = forms.TextInput(attrs={'placeholder': 'Введите ссылку новости'})
    link = forms.CharField(widget=link_widget)

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
