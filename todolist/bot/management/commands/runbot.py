import os

from django.core.management import BaseCommand
from dotenv import load_dotenv
from bot.tg.client import TgClient

load_dotenv()


class Command(BaseCommand):
    help = 'Bot'

    def handle(self, *args, **kwargs):
        token = os.getenv("BOT_TOKEN")
        tg_client = TgClient(token)
        offset = 0

        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.get('update_id') + 1
                chat_id = item.get('message').get('chat').get('id')
                print(item.get('message').get('from').get('id'))
                tg_client.send_message(chat_id, 'Done!')
