from django.db import models


class Article(models.Model):
    body = models.TextField()
    link = models.CharField(max_length=300, default='https://zakonvremeni.ru/news/')
