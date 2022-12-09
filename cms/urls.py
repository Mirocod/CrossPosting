from .views import ArticleView
from django.urls import path

urlpatterns = [
    path('articles/', ArticleView.as_view())
]
