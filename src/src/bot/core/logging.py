import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from os.path import dirname

from django.conf import settings

FORMATTER = logging.Formatter(
    fmt=(
        "[%(asctime)s] %(levelname)s | %(threadName)s | %(name)s | "
        "%(funcName)s:%(lineno)d | %(message)s"
    ),
)
LOG_FILE = "bot.log"


def get_logs_dir() -> str:
    logs_dir = os.path.join(dirname(settings.SOURCES_ROOT), "logs")
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    return logs_dir


def get_console_handler() -> logging.StreamHandler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler() -> TimedRotatingFileHandler:
    log_file = os.path.join(get_logs_dir(), LOG_FILE)
    file_handler = TimedRotatingFileHandler(log_file, when="midnight")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name: str, level: int = logging.DEBUG):
    logger = logging.getLogger(logger_name)

    logger.setLevel(level)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())

    logger.propagate = False

    return logger
