# Generated by Django 4.1.4 on 2022-12-19 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_remove_article_title_article_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='link',
            field=models.CharField(default='https://zakonvremeni.ru/news/', max_length=200),
        ),
    ]