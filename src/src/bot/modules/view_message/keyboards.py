from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.events.models import EventMessage, Feature


def get_keyboard_message(obj: EventMessage) -> InlineKeyboardMarkup:
    """
    Клавиатура обогащения
    """
    features_query = Feature.objects.filter(id_incident=obj.id_incident)
    list_buttons = [
        InlineKeyboardButton(text="Обогатить", callback_data="SHOW_OR_HINT"),
    ]
    for feature in features_query:
        list_buttons.append(
            InlineKeyboardButton(
                text=f"{feature.text_button}",
                callback_data=f"FEATURE::{feature.id_incident}",
            ),
        )
    return InlineKeyboardMarkup(inline_keyboard=[list_buttons])
