from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    """Команда для создания периодческих задач."""

    help = "Создание периодических задач"

    def handle(self, *args, **options):
        """Консольный вывод."""
        self.stdout.write("Начато создание периодических задач:\n")
        start = timezone.now()
        self._setup_tasks()
        self.stdout.write(
            "Периодические задачи созданы. Время: "
            f"{(timezone.now() - start).seconds / 60:.2f} мин"
        )

    @staticmethod
    def _setup_tasks():
        """Периодические задачи."""
        every_five_min_cron, _ = CrontabSchedule.objects.get_or_create(
            minute="*/1",
            timezone=settings.TIME_ZONE,
        )

        every_day_at_8am_hours_cron, _ = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="1",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone=settings.TIME_ZONE,
        )

        every_day_at_7am_hours_cron, _ = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone=settings.TIME_ZONE,
        )

        _ = PeriodicTask.objects.get_or_create(
            crontab=every_five_min_cron,
            name="Создание рассылки",
            task="src.events.tasks.send_events",
            # queue="default",
        )
