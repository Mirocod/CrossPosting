import abc
import os

import requests

from cms.models import Article


class PromoteError(Exception):
    pass


class Promoter(abc.ABC):
    def __init__(self, article: Article):
        self.article = article

    def promote(self):
        raise NotImplementedError


class TelegramPromoter(Promoter):
    def promote(self):
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        channel_id = os.getenv('TELEGRAM_CHAT_ID')

        long_text = f'{self.article.body}\n{self.article.link}'

        send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={channel_id}&text={long_text}'

        response = requests.get(send_message_url)
        result = response.json()
        if not result['ok']:
            raise PromoteError('Похоже, нас послали доделывать приложение :-(')


class VkontaktePromoter(Promoter):
    def promote(self):
        vk_login = os.getenv('VK_LOGIN')
        vk_password = os.getenv('VK_PASSWORD')
        vk_owner_id = os.getenv('VK_OWNER_ID')

        import vk_api
        session = vk_api.VkApi(login=vk_login,
                               password=vk_password)
        session.auth()
        api = session.get_api()

        try:
            api.wall.post(owner_id=vk_owner_id,
                          message=self.article.body,
                          attachments=self.article.link)
        except vk_api.VkApiError as exc:
            raise PromoteError(exc)


class OdnoklassnikiPromoter(Promoter):
    def promote(self):
        from json import JSONEncoder
        import ok_api

        ok_access_token = os.getenv('OK_ACCESS_TOKEN')
        ok_application_key = os.getenv('OK_APPLICATION_KEY')
        ok_application_secret_key = os.getenv('OK_APPLICATION_SECRET_KEY')

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
                                    gid='70000001426867',
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
