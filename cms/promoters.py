import abc
from urllib.parse import urlencode

import requests

from cms.models import Article
from crossposting_backend.settings import promoter_secrets


class PromoteError(Exception):
    pass


class Promoter(abc.ABC):
    def __init__(self, article: Article):
        self.article = article

    def promote(self):
        raise NotImplementedError


class TelegramPromoter(Promoter):
    def promote(self):
        long_text = f'{self.article.body}\n{self.article.link}'
        channel_id = promoter_secrets['TELEGRAM_CHAT_ID']
        bot_token = promoter_secrets['TELEGRAM_BOT_TOKEN']
        querystring = (('chat_id', channel_id), ('text', long_text))
        encoded_querystring = urlencode(querystring)

        send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?{encoded_querystring}'

        response = requests.get(send_message_url)
        result = response.json()
        if not result['ok']:
            raise PromoteError('Посылка сообщения в телеграм провалилась. Подробности %s' % str(result))


class VkontaktePromoter(Promoter):
    def promote(self):
        vk_owner_id = promoter_secrets['VK_OWNER_ID']
        vk_token = promoter_secrets['VK_TOKEN']
        from_group = 1

        try:
            requests.post('https://api.vk.com/method/wall.post',
                            params={
                                    'access_token': vk_token,
                                    'owner_id': vk_owner_id,
                                    'from_group': from_group,
                                    'message': self.article.body,
                                    'attachment': self.article.link,
                                    'signed': 0,
                                    'v': '5.131'
                                    })
        except Exception as exc:
            raise PromoteError(exc)


class OdnoklassnikiPromoter(Promoter):
    def promote(self):
        from json import JSONEncoder
        import ok_api

        ok_access_token = promoter_secrets['OK_ACCESS_TOKEN']
        ok_application_key = promoter_secrets['OK_APPLICATION_KEY']
        ok_application_secret_key = promoter_secrets['OK_APPLICATION_SECRET_KEY']
        ok_group_id = promoter_secrets['OK_GROUP_ID']

        session = ok_api.OkApi(access_token=ok_access_token,
                               application_key=ok_application_key,
                               application_secret_key=ok_application_secret_key)
        attachments = {
            'media': [
                {
                    'type': 'text',
                    'text': self.article.body,
                },
                {
                    'type': 'link',
                    'url': self.article.link,
                },
            ]
        }
        encoded_attachments = JSONEncoder().encode(attachments)
        try:
            session.mediatopic.post(type='GROUP_THEME',
                                    gid=ok_group_id,
                                    attachment=encoded_attachments)
        except ok_api.OkApiException as exc:
            raise PromoteError(exc)


class Marketer:
    def __init__(self, article: Article):
        self.promoters = [
            TelegramPromoter(article),
            VkontaktePromoter(article),
            OdnoklassnikiPromoter(article),
        ]

    def promote(self):
        for promoter in self.promoters:
            promoter.promote()
