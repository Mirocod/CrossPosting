import requests
from django.core.management import BaseCommand

from crossposting_backend.settings import promoter_secrets


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot_token = promoter_secrets['TELEGRAM_BOT_TOKEN']
        get_updates_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
        response = requests.get(get_updates_url)
        if response.ok:
            json_body = response.json()
            if json_body['ok']:
                if 'result' in json_body and len(json_body['result']) > 0:
                    print(json_body['result'][0]['channel_post']['sender_chat']['id'])
                else:
                    print('Нет обновлений')
            else:
                print(json_body['error_code'])
        else:
            print(response.status_code)
        return 0
