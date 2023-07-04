from django.core.validators import MinLengthValidator
from django.db import models
from goals.models import DatesModelMixin

from core.models import User
from goals.models.goal import Goal


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.PROTECT)
    text = models.CharField(verbose_name="Текст", validators=[MinLengthValidator(1)])
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")
