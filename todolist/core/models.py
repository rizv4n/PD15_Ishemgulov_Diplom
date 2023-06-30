from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    updated = models.DateTimeField(auto_now=True)

