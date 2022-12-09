from json import JSONDecoder
import requests
import os
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from cms.models import Article


@method_decorator(csrf_exempt, name='dispatch')
class ArticleView(View):
    def post(self, request):
        article_data = JSONDecoder().decode(request.body.decode())
        article = Article.objects.create(**article_data)
        response = {'ok': True}
        return JsonResponse(response)