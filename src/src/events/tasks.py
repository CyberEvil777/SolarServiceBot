import subprocess
import time

from django.conf import settings
from telegram.error import BadRequest, Unauthorized

from src import celery_app
from src.bot.core.helpers import install
from src.bot.core.telegram import bot
from src.bot.modules.view_message.keyboards import get_keyboard_message
from src.core.mail import mail_send
from src.events.logic import load_events, wazuh_hight_serializer
from src.events.models import EventMessage, Feature


@celery_app.task()
def send_events() -> None:
    """Создание голосования"""
    load_events(wazuh_hight_serializer)
    messages = EventMessage.objects.filter(is_sent=False)
    messages_sent = 0
    for message in messages:
        try:
            message_response = bot.send_message(
                chat_id=settings.CHAT_ID,
                text=message.short_text,
                reply_markup=get_keyboard_message(message),
            )
            messages_sent += 1
            if ((message.user_info).split(","))[0]:
                mail_send(
                    IncID=message.id_incident,
                    message=message.full_text,
                    receiver_email=((message.user_info).split(","))[0],
                )
            message.id_message = message_response.message_id
            message.is_sent = True
            message.save(update_fields=["id_message", "is_sent"])
        except (Unauthorized, BadRequest):
            continue
        if messages_sent > 5:
            time.sleep(300)
            messages_sent = 0


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
