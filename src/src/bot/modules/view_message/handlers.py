from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from src.bot.core.telegram import dp
from src.bot.modules.view_message.keyboards import get_keyboard_message
from src.events.models import EventMessage
from src.shop.models import Shop, WinnerShop


def poll(update: Update, context: ContextTypes) -> None:
    """Создание голосования"""
    shops = list(Shop.objects.all().values_list("name", flat=True))
    questions_dict = {shop: 0 for shop in shops}
    message = context.bot.send_poll(
        update.effective_chat.id,
        "Какую еду сегодня закажем?",
        shops,
        is_anonymous=False,
        allows_multiple_answers=True,
    )

    payload = {
        message.poll.id: {
            "questions": shops,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "questions_dict": questions_dict,
            "answers": 0,
            "winner": None,
        }
    }
    context.bot_data.update(payload)


def receive_poll_answer(update: Update, context: ContextTypes) -> None:
    """Отлов голосов"""
    answer = update.poll_answer
    answered_poll = context.bot_data[answer.poll_id]
    try:
        questions = answered_poll["questions"]
    except KeyError:
        return
    selected_options = answer.option_ids

    questions_dict = answered_poll["questions_dict"]
    for question_id in selected_options:
        questions_dict[questions[question_id]] += 1
    answered_poll["answers"] += 1
    answered_poll["questions_dict"] = questions_dict
    winner = max(questions_dict, key=questions_dict.get)
    answered_poll["winner"] = winner
    shop = Shop.objects.filter(name=winner).first()
    WinnerShop.objects.get_or_create(shop=shop)


def receive_poll(update: Update, context: ContextTypes) -> None:
    """On receiving polls, reply to it by a closed poll copying the received poll"""
    actual_poll = update.effective_message.poll
    # Only need to set the question and options, since all other parameters don't matter for
    # a closed poll
    return update.effective_message.reply_poll(
        question=actual_poll.question,
        options=[o.text for o in actual_poll.options],
        # with is_closed true, the poll/quiz is immediately closed
        is_closed=True,
        reply_markup=ReplyKeyboardRemove(),
    )


def show_message(update: Update, context: ContextTypes) -> None:
    """Показывает или скрывает обогащенное сообщение"""
    message_id = update.callback_query.message.message_id
    messages = EventMessage.objects.filter(id_message=message_id)
    message = messages.first()
    if getattr(message, "is_full"):
        update.callback_query.message.edit_text(
            text=message.short_text, reply_markup=get_keyboard_message()
        )
        messages.update(is_full=False)
    else:
        update.callback_query.message.edit_text(
            text=message.text, reply_markup=get_keyboard_message()
        )
        messages.update(is_full=True)


dp.add_handler(CallbackQueryHandler(show_message, pattern="SHOW_OR_HINT"))
