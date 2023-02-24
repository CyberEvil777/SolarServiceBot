import os

from celery import Celery
from kombu import Queue


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.dev")

celery_app = Celery("src")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

celery_app.conf.task_queues = (
    Queue(
        "default",
    ),
)
