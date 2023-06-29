import inspect

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from src.bot.core.telegram import dp
from src.bot.modules.view_message.keyboards import get_keyboard_message
# from src.events.logic import load_events, wazuh_hight_serializer
from src.events.models import EventMessage
from src.events.tasks import load_script


def show_message(update: Update, context: ContextTypes) -> None:
    """Показывает или скрывает обогащенное сообщение"""
    message_id = update.callback_query.message.message_id
    messages = EventMessage.objects.filter(id_message=message_id)
    message = messages.first()
    # print(wazuh_hight_serializer)
    # load_events(wazuh_hight_serializer)  # дает события с файла
    if getattr(message, "is_full"):
        update.callback_query.message.edit_text(
            text=inspect.cleandoc(message.short_text),
            reply_markup=get_keyboard_message(message),
        )
        messages.update(is_full=False)
    else:
        update.callback_query.message.edit_text(
            text=inspect.cleandoc(message.full_text),
            reply_markup=get_keyboard_message(message),
        )
        messages.update(is_full=True)


def use_script(update: Update, context: ContextTypes) -> None:
    _, id_incident = update.callback_query.data.split("::")
    message_id = update.callback_query.message.message_id
    load_script.delay(id_incident, message_id)


dp.add_handler(CallbackQueryHandler(show_message, pattern="SHOW_OR_HINT"))
dp.add_handler(CallbackQueryHandler(use_script, pattern="FEATURE"))
