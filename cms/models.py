from django.db import models


class Article(models.Model):
    body = models.TextField()
    link = models.CharField(max_length=100, default='https://zakonvremeni.ru/news/')
