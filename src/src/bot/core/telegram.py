from django.conf import settings
from telegram import Bot
from telegram.ext import Dispatcher, Updater
from telegram.utils.request import Request

from src.bot.core.logging import get_logger
from src.bot.core.utils import MetaSingleton

logger = get_logger(__name__)


class SingletonUpdater(Updater, metaclass=MetaSingleton):
    pass


REQUEST_KWARGS = {
    "proxy_url": "socks5://185.61.38.128:1080/",
    # Optional, if you need authentication:
    "urllib3_proxy_kwargs": {
        "assert_hostname": "False",
        "cert_reqs": "CERT_NONE"
        # 'username': 'user',
        # 'password': 'password'
    },
}
bot: Bot = Bot(
    token=settings.BOT_TOKEN,
    request=Request(
        con_pool_size=8,
        proxy_url="socks5://185.61.38.128:1080/",
        urllib3_proxy_kwargs={
            "assert_hostname": "False",
            "cert_reqs": "CERT_NONE"
            # 'username': 'user',
            # 'password': 'password'
        },
    ),
)
updater: SingletonUpdater = SingletonUpdater(bot=bot, request_kwargs=REQUEST_KWARGS)
dp: Dispatcher = updater.dispatcher
