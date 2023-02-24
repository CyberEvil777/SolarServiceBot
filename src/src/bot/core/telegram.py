from django.conf import settings
from telegram import Bot
from telegram.ext import Dispatcher, Updater
from telegram.utils.request import Request

from src.bot.core.logging import get_logger
from src.bot.core.utils import MetaSingleton

logger = get_logger(__name__)


class SingletonUpdater(Updater, metaclass=MetaSingleton):
    pass


bot: Bot = Bot(token=settings.BOT_TOKEN, request=Request(con_pool_size=8))
updater: SingletonUpdater = SingletonUpdater(bot=bot)
dp: Dispatcher = updater.dispatcher
