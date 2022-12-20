from django.urls import path

from .views import ArticleView, new_article, AuthenticationView

urlpatterns = [
    path('articles/', ArticleView.as_view(), name='create-article'),
    path('articles/new/', new_article, name='new-article'),
    path(
        '',
        AuthenticationView.as_view(),
        name='authenticate'
    )
]
