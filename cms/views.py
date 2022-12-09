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
    def _send_to_channel(self, article: Article):
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

    def post(self, request):
        article_data = JSONDecoder().decode(request.body.decode())
        article = Article.objects.create(**article_data)
        self._send_to_channel(article)
        response = {'ok': True}
        return JsonResponse(response)