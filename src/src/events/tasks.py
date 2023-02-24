from django.conf import settings

from src import celery_app
from src.bot.core.telegram import bot
from src.bot.modules.view_message.keyboards import get_keyboard_message
from src.events.models import EventMessage


@celery_app.task()
def send_events() -> None:
    """Создание голосования"""
    messages = EventMessage.objects.filter(is_sent=False)
    for message in messages:
        message_response = bot.send_message(
            chat_id=settings.CHAT_ID,
            text=message.text,
            reply_markup=get_keyboard_message(),
        )
        message.id_message = message_response.message_id
        message.is_sent = True
        message.save(update_fields=["id_message", "is_sent"])
