import subprocess

from django.conf import settings

from src import celery_app
from src.bot.core.helpers import install
from src.bot.core.telegram import bot
from src.bot.modules.view_message.keyboards import get_keyboard_message
from src.events.models import EventMessage, Feature


@celery_app.task()
def send_events() -> None:
    """Создание голосования"""
    # load_events(wazuh_hight_serializer)
    messages = EventMessage.objects.filter(is_sent=False)
    for message in messages:
        message_response = bot.send_message(
            chat_id=settings.CHAT_ID,
            text=message.short_text,
            reply_markup=get_keyboard_message(message),
        )
        message.id_message = message_response.message_id
        message.is_sent = True
        message.save(update_fields=["id_message", "is_sent"])


@celery_app.task()
def load_script(id_incident, message_id) -> None:
    feature = Feature.objects.filter(id_incident=id_incident).first()
    event = EventMessage.objects.filter(id_message=message_id).first()
    while True:
        try:
            with open("output.txt", "w") as output:
                subprocess.call(["python", feature.script.path], stdout=output)
            with open("output.txt", "r") as output:
                output = output.read()
                msg = (
                    f" #{event.id_incident.replace('-','_')} \n"
                    f"☢️ {event.rule_info}\n\n"
                    f"{output}"
                )
                bot.send_message(
                    chat_id=settings.CHAT_ID,
                    text=msg,
                )
            break
        except ModuleNotFoundError as error_package:
            install(error_package.name)
            continue
