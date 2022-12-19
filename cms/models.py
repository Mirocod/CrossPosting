from django.db import models


class Article(models.Model):
    body = models.TextField(null=False)
    link = models.CharField(max_length=200, default='https://zakonvremeni.ru/news/')
