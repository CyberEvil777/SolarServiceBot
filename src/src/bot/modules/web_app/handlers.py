import json

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler)

from src.bot.core.helpers import get_or_create_user
from src.bot.core.telegram import dp
from src.events.models import EventMessage
from src.goods.models import Goods
from src.order.models import Order


def start(update: Update, context: CallbackContext) -> None:
    user = get_or_create_user(update.effective_user)
    #     [
    #     KeyboardButton(
    #         "WEB_FORM",
    #         web_app=WebAppInfo(url="https://tourmaline-cupcake-966f19.netlify.app/form"),
    #     )
    # ],
    menu = [
        [
            KeyboardButton(
                "Заказать еду",
                web_app=WebAppInfo(
                    url="https://tourmaline-cupcake-966f19.netlify.app/"
                ),
            )
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {user.name}",
        reply_markup=reply_markup,
    )


def open_web_app(update: Update, context: CallbackContext) -> None:
    """Отлавливаем запросы с web app приложения"""
    user = get_or_create_user(update.effective_user)
    data = json.loads(update.effective_message.web_app_data.data)
    id_products = [product.get("id") for product in data.get("products")]

    goods = Goods.objects.filter(pk__in=id_products)
    order = Order(user=user)
    order.save()
    order.goods.add(*goods)
    goods_from_site = list(goods.values_list("title", flat=True))
    sucsess_msg = f"Вы успешно заказали: {', '.join(goods_from_site)}"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=sucsess_msg,
        disable_web_page_preview=True,
    )


def check_id(update: Update, context: CallbackContext) -> None:
    update.effective_chat.send_message("helllo")
    print(update.effective_chat.id)


dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("check", check_id))
dp.add_handler(MessageHandler(Filters.status_update.web_app_data, open_web_app))
# dp.add_handler(MessageHandler(CustomFilters.button(ABOUT_BOT), about_bot_handler))
