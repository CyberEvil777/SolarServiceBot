from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone

from src.accounts.managers import CustomUserManager


class User(AbstractBaseUser):
    """Модель описывающая таблицу телеграм пользователя."""

    email = None

    username = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Логин"
    )
    name = models.CharField(
        verbose_name="Имя Фамилия", blank=False, null=True, max_length=100
    )
    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name="Уникальный id в Телеграм",
        null=True,
    )

    date_joined = models.DateTimeField(
        verbose_name="Дата регистрации", default=timezone.now
    )

    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_authorization = models.BooleanField(
        default=False,
    )

    is_moderator = models.BooleanField(
        verbose_name="Модератор",
        help_text="Может обогощать сообщения",
        default=False,
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"
