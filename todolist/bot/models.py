from django.db import models

from core.models import User


class TgUser(models.Model):
    tg_chat_id = models.IntegerField()
    tg_user_id = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    verification_code = models.CharField(max_length=10, null=True)
