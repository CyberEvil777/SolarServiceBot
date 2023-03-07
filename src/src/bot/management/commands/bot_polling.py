from django.core.management import BaseCommand
from telegram import Update
from telegram.ext import CallbackContext

from src.bot.core.logging import get_logger
from src.bot.core.packages import PackagesLoader
from src.bot.core.telegram import updater

logger = get_logger(__name__)


def err_handler(update: "Update", context: "CallbackContext"):
    update.message.reply_text("Комманда не распознана")


class Command(BaseCommand):
    """Команда для запуска пулинга телеграм бота."""

    help = "Запуск пулинга телеграм бота"  # noqa

    @staticmethod
    def load_modules():
        """Функция подгрузки пакета, в массив добавляем наименование пакета."""
        PackagesLoader().load_packages(
            f"src.bot.modules.{item}"
            for item in [
                "view_message",
            ]
        )

    def handle(self, *args, **options):
        """Запуск пулинга телеграм бота."""

        self.load_modules()

        updater.start_polling()
        logger.info("Bot polling started")
        # Global Exception Handler. Регистрируется последним из всех Handler'ов
        # Перехватывает все сообщения которые не обрабатываются другими Хэндлерами
        # dp.add_handler(MessageHandler(Filters.regex(r".*"), err_handler))

        updater.idle()
