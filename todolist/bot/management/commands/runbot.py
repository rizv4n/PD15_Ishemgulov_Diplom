import os

from django.core.management import BaseCommand
from dotenv import load_dotenv
from bot.tg.client import TgClient
from bot.bot_tools import Bot

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

                bot = Bot(
                    telegram_id=item.get('message').get('from').get('id'),
                    chat_id=item.get('message').get('chat').get('id'),
                    offset=offset,
                    client=tg_client)

                if item.get('message').get('text') == '/start':
                    bot.start()

                elif item.get('message').get('text') == '/goals':
                    bot.goals()

                elif item.get('message').get('text') == '/create':
                    bot.create()
