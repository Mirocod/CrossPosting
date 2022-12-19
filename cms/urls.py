from django.urls import path

from .views import ArticleView, new_article

urlpatterns = [
    path('articles/', ArticleView.as_view(), name='create-article'),
    path('articles/new/', new_article, name='new-article'),
]
