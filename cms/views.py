from json import JSONDecoder, JSONEncoder
import requests
import os
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from cms.models import Article


@method_decorator(csrf_exempt, name='dispatch')
class ArticleView(View):
    def _promote_to_channel(self, article: Article):
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        channel_id = os.getenv('TELEGRAM_CHAT_ID')

        long_text = f'{article.title}\n{article.body}'

        send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={channel_id}&text={long_text}'

        response = requests.get(send_message_url)
        result = response.json()
        if result['ok']:
            print('Мы послали сообщение, ура!')
        else:
            print('Похоже, нас послали доделывать приложение :-(')

    def _promote_to_joomla(self, article: Article):
        joomla_token = os.getenv('JOOMLA_TOKEN')
        headers = {
            'X-Joomla-Token': joomla_token,
            'Content-Type': 'application/json'
        }
        article_json = {
            "alias": article.title,
            "articletext": article.body,
            "catid": "8",
            "language": "*",
            "metadesc": "",
            "metakey": "",
            "title": article.title,
            "state": 1
        }
        response = requests.post('http://zv.mirokod.ru/api/index.php/v1/content/articles',
                                 headers=headers,
                                 data=JSONEncoder().encode(article_json))
        result = response.json()
        print(result)

    def post(self, request):
        article_data = JSONDecoder().decode(request.body.decode())
        article = Article.objects.create(**article_data)
        self._promote_to_channel(article)
        self._promote_to_joomla(article)
        response = {'ok': True}
        return JsonResponse(response)