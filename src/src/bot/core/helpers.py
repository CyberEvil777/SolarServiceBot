from django.db import transaction
from telegram import User as TelegramUser

from src.accounts.models import User


@transaction.atomic
def get_or_create_user(telegram_user: TelegramUser) -> None:
    """Функция проверяет существует ли пользователь. Если не существует, то создает"""
    try:
        user = User.objects.get_by_tg_id(telegram_user.id)
    except User.DoesNotExist:
        if telegram_user.last_name is None:
            user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                name=f"{telegram_user.first_name}",
            )
        else:
            user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                name=f"{telegram_user.first_name} {telegram_user.last_name}",
            )
        user.save()
    return user
