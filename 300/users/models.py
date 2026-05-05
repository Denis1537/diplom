from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_blocked = models.BooleanField("заблокирован", default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

