from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_message() -> InlineKeyboardMarkup:
    """
    Клавиатура обогащения
    """

    list_buttons = [
        InlineKeyboardButton(text="Обогатить", callback_data="SHOW_OR_HINT"),
    ]

    return InlineKeyboardMarkup(inline_keyboard=[list_buttons])
