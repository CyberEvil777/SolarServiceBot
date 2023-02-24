from django.conf import settings
from telegram import (
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import ContextTypes

from src import celery_app
from src.bot.core.telegram import bot
from src.shop.models import Shop


@celery_app.task(queue="default")
def poll() -> None:
    """Создание голосования"""
    shops = list(Shop.objects.all().values_list("name", flat=True))
    questions_dict = {shop: 0 for shop in shops}
    message = bot.send_poll(
        settings.CHAT_ID,
        "Какую еду сегодня закажем?",
        shops,
        is_anonymous=False,
        allows_multiple_answers=True,
    )

    payload = {
        message.poll.id: {
            "questions": shops,
            "message_id": message.message_id,
            "chat_id": settings.CHAT_ID,
            "questions_dict": questions_dict,
            "answers": 0,
            "winner": None,
        }
    }
    bot.bot_data.update(payload)
