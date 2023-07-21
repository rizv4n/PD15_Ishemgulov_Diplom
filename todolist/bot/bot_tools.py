import random
import string

from bot.models import TgUser
from goals.models.category import GoalCategory
from goals.models.goal import Goal


def get_verification_code(length=10):
    characters = string.digits + string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(length))


class Messages:
    choose_cat = 'Выберите категорию:'
    choose_goal_title = 'Напишите заголовок цели:'
    uncorrected_data = 'Ошибка операции (некорректно введенные данные)'

    @staticmethod
    def start_message(verify_code=None, new_user=False, verified=True, username=None):
        if new_user:
            return f'Привет) Подтверди аккаунт на сайте:)\nКод верификации: {verify_code}'
        else:
            if verified:
                return f'Привет, {username}\n' \
                       f'/goals - чтобы посмотреть цели\n' \
                       f'/create - чтобы создать\n'
            return f'Код верификации: {verify_code}'

    @staticmethod
    def errors(is_done=False, verified=True):
        if is_done:
            return 'Операция выполнена!'
        else:
            if verified:
                return 'Операция отменена!'
            return 'Вы не верифицированы.\nИспользуйте /start'


class CancelCreationException(BaseException):
    pass


class Bot:
    def __init__(self, telegram_id, chat_id, client, offset):
        self.telegram_id = telegram_id
        self.chat_id = chat_id
        self.client = client
        self.offset = offset

    def is_verified(self) -> bool:
        return TgUser.objects.get(tg_user_id=self.telegram_id).user_id is not None

    def is_registered(self) -> bool:
        return TgUser.objects.filter(tg_user_id=self.telegram_id).exists()

    def _get_user_input(self):
        res = self.client.get_updates(offset=self.offset)
        user_input = res.result[0].get('message').get('text')

        if user_input == '/cancel':
            raise CancelCreationException

        return user_input

    def _choose_categories(self, user_id):
        categories = GoalCategory.objects.filter(user=user_id, is_deleted=False)
        self.client.send_message(
            chat_id=self.chat_id,
            text=Messages.choose_cat)
        num = 0
        for cat in categories:
            num += 1
            self.client.send_message(
                chat_id=self.chat_id,
                text=f'#{num} {cat.title}')

    def _create_goal(self, category, title):
        new_goal = Goal(
            title=title,
            user=TgUser.objects.get(tg_user_id=self.telegram_id).user_id,
            category=GoalCategory.objects.get(title=category)
        )
        new_goal.save()
        self.client.send_message(
            chat_id=self.chat_id,
            text=Messages.errors(is_done=True))

    def start(self):
        verify = get_verification_code()

        if not self.is_registered():
            new_user = TgUser(
                tg_chat_id=self.chat_id,
                tg_user_id=self.telegram_id,
                verification_code=verify)
            new_user.save()

            self.client.send_message(
                chat_id=self.chat_id,
                text=Messages.start_message(
                    new_user=True,
                    verify_code=verify))

        elif not self.is_verified():
            user = TgUser.objects.get(tg_user_id=self.telegram_id)
            user.verification_code = verify
            user.save()
            self.client.send_message(
                chat_id=self.chat_id,
                text=Messages.start_message(
                    verified=False,
                    verify_code=verify))

        else:
            username = TgUser.objects.get(tg_user_id=self.telegram_id).user_id.username
            self.client.send_message(
                chat_id=self.chat_id,
                text=Messages.start_message(username=username))

    def goals(self):
        if not self.is_registered() or not self.is_verified():
            self.client.send_message(
                chat_id=self.chat_id,
                text=Messages.errors(verified=False))
        else:
            goals = Goal.objects.filter(
                user=TgUser.objects.get(tg_user_id=self.telegram_id).user_id,
                status__in=[1, 2, 3])
            num = 0
            for goal in goals:
                num += 1
                self.client.send_message(
                    chat_id=self.chat_id,
                    text=f'#{num} {goal.title}')

    def create(self):
        if not self.is_registered() or not self.is_verified():
            self.client.send_message(
                chat_id=self.chat_id,
                text=Messages.errors(verified=False)
            )

        self._choose_categories(
            user_id=TgUser.objects.get(tg_user_id=self.telegram_id).user_id
        )

        try:
            category = self._get_user_input()

            if not GoalCategory.objects.filter(title=category).exists():
                self.client.send_message(
                    chat_id=self.chat_id,
                    text=Messages.uncorrected_data
                )

            self.client.send_message(
                chat_id=self.chat_id,
                text=Messages.choose_goal_title
            )

            self.offset += 1
            title = self._get_user_input()
            self._create_goal(category=category, title=title)

        except CancelCreationException:
            self.client.send_message(
                chat_id=self.chat_id,
                text=Messages.errors()
            )
