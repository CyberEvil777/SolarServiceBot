import inspect
import runpy
import subprocess
import sys

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from src.bot.core.telegram import dp
from src.bot.modules.view_message.keyboards import get_keyboard_message
from src.events.logic import load_events, wazuh_hight_serializer
from src.events.models import EventMessage, Feature


def show_message(update: Update, context: ContextTypes) -> None:
    """Показывает или скрывает обогащенное сообщение"""
    message_id = update.callback_query.message.message_id
    messages = EventMessage.objects.filter(id_message=message_id)
    message = messages.first()
    print(wazuh_hight_serializer)
    load_events(wazuh_hight_serializer)  # ает события с файла
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


def install(package):
    subprocess.check_call([sys.executable, "-m", "pipenv", "install", package])


def use_script(update: Update, context: ContextTypes) -> None:
    update.callback_query.message.reply_markup.inline_keyboard[0][1]
    _, id_incident = (
        getattr(
            update.callback_query.message.reply_markup.inline_keyboard[0][1],
            "callback_data",
        )
    ).split("::")
    feature = Feature.objects.filter(id_incident=id_incident).first()
    while True:
        try:
            return_string = runpy.run_path(path_name=feature.script.path)
            # return_string = exec(open(feature.script.path).read())
            # return_string = importlib.import_module(feature.script.path)
            break
        except ModuleNotFoundError as error_package:
            install(error_package.name)
            print(error_package.name)
            continue
    print(update.callback_query.message.message_id)


dp.add_handler(CallbackQueryHandler(show_message, pattern="SHOW_OR_HINT"))
dp.add_handler(CallbackQueryHandler(use_script, pattern="FEATURE"))
