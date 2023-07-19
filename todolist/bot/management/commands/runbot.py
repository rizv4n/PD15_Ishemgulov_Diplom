import os
import random
import string

from django.core.management import BaseCommand
from dotenv import load_dotenv
from bot.tg.client import TgClient
from bot.models import TgUser
from goals.models.goal import Goal
from goals.models.category import GoalCategory

load_dotenv()


def verification_code(length=10):
    characters = string.digits + string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(length))


class Command(BaseCommand):
    help = 'Bot'

    def handle(self, *args, **kwargs):
        token = os.getenv("BOT_TOKEN")
        tg_client = TgClient(token)
        offset = 0

        def is_verified(telegram_id):
            if not TgUser.objects.filter(tg_user_id=telegram_id).exists():
                return 'not registered'
            elif TgUser.objects.get(tg_user_id=telegram_id).user_id is None:
                return 'not verified'
            else:
                return 'verified'

        def start(telegram_id, chat_id):
            verify = verification_code()
            verified = is_verified(telegram_id)
            if verified == 'not registered':
                new_user = TgUser(tg_chat_id=chat_id, tg_user_id=telegram_id, verification_code=verify)
                new_user.save()

                message = f'Привет) Подтверди аккаунт на сайте:)\nКод верификации: {verify}'
                tg_client.send_message(chat_id, message)

            elif verified == 'not verified':
                user = TgUser.objects.get(tg_user_id=telegram_id)
                user.verification_code = verify
                user.save()

                message = f'Код верификации: {verify}'
                tg_client.send_message(chat_id, message)

            else:
                username = TgUser.objects.get(tg_user_id=telegram_id).user_id.username
                message_1 = f'Привет, {username}'
                message_2 = '/goals - чтобы посмотреть цели\n/create - чтобы создать'
                tg_client.send_message(chat_id, message_1)
                tg_client.send_message(chat_id, message_2)

        def get_goals(telegram_id):
            if is_verified(telegram_id) != 'verified':
                message = 'Вы не верифицированы.\nИспользуйте /start'
                tg_client.send_message(chat_id, message)
            else:
                user_id = TgUser.objects.get(tg_user_id=telegram_id).user_id
                goals = Goal.objects.filter(user=user_id, status__in=[1, 2, 3])
                num = 1
                for goal in goals:
                    message = f'#{num} {goal.title}'
                    tg_client.send_message(chat_id, message)
                    num += 1

        def get_cats(user_id):
            categories = GoalCategory.objects.filter(user=user_id)
            message = 'Выберите категорию:'
            tg_client.send_message(chat_id, message)
            num = 1
            for cat in categories:
                message = f'#{num} {cat.title}'
                tg_client.send_message(chat_id, message)
                num += 1

        def get_user_input(offset):
            res = tg_client.get_updates(offset=offset)
            user_input = res.result[0].get('message').get('text')
            return user_input

        def create_goal(telegram_id, cat, title):
            user_id = TgUser.objects.get(tg_user_id=telegram_id).user_id
            category = GoalCategory.objects.get(title=cat)
            new_goal = Goal(
                title=title,
                user=user_id,
                category=category
            )
            new_goal.save()
            message = 'Операция выполнена!'
            tg_client.send_message(chat_id, message)

        def create_goal_view(telegram_id):
            if is_verified(telegram_id) != 'verified':
                message = 'Вы не верифицированы.\nИспользуйте /start'
                tg_client.send_message(chat_id, message)
            else:
                user_id = TgUser.objects.get(tg_user_id=telegram_id).user_id
                get_cats(user_id)
                cat = get_user_input(offset)

                if cat == '/cancel':
                    message = 'Операция отменена!'
                    tg_client.send_message(chat_id, message)

                elif GoalCategory.objects.filter(title=cat).exists():
                    message = 'Напишите заголовок цели:'
                    tg_client.send_message(chat_id, message)
                    title = get_user_input(offset=offset+1)

                    if title == '/cancel':
                        message = 'Операция отменена!'
                        tg_client.send_message(chat_id, message)

                    else:
                        create_goal(telegram_id, cat, title)

                else:
                    message = 'Ошибка операции (некорректно введенные данные)'
                    tg_client.send_message(chat_id, message)

        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.get('update_id') + 1
                chat_id = item.get('message').get('chat').get('id')
                tg_id = item.get('message').get('from').get('id')

                if item.get('message').get('text') == '/start':
                    start(telegram_id=tg_id, chat_id=chat_id)

                elif item.get('message').get('text') == '/goals':
                    get_goals(telegram_id=tg_id)

                elif item.get('message').get('text') == '/create':
                    create_goal_view(telegram_id=tg_id)
