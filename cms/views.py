import os
from json import JSONDecoder

import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from cms.models import Article


@method_decorator(csrf_exempt, name='dispatch')
class ArticleView(View):
    def _promote_to_telegram(self, article: Article):
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        channel_id = os.getenv('TELEGRAM_CHAT_ID')

        long_text = f'{article.body}\n{article.link}'

        send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={channel_id}&text={long_text}'

        response = requests.get(send_message_url)
        result = response.json()
        if result['ok']:
            print('Мы послали сообщение, ура!')
        else:
            print('Похоже, нас послали доделывать приложение :-(')

    def _promote_to_vk(self, article: Article):
        import vk_api
        vk_login = os.getenv('VK_LOGIN')
        vk_password = os.getenv('VK_PASSWORD')
        vk_owner_id = os.getenv('VK_OWNER_ID')

        session = vk_api.VkApi(login=vk_login,
                               password=vk_password)
        session.auth()
        api = session.get_api()

        api.wall.post(owner_id=vk_owner_id,
                      message=article.body,
                      attachments=article.link)

    def post(self, request):
        article_data = JSONDecoder().decode(request.body.decode())
        article = Article.objects.create(**article_data)
        self._promote_to_telegram(article)
        self._promote_to_vk(article)
        response = {'ok': True}
        return JsonResponse(response)
