from django.contrib import admin
from django.contrib.auth.models import Group, User
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    SolarSchedule,
)

from src.events.models import EventMessage


# Register your models here.
@admin.register(EventMessage)
class EventMessageAdmin(admin.ModelAdmin):
    """Админка для модели EventMessage"""

    list_display = ("text", "is_sent", "id_message")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text",
                    "is_sent",
                    "is_full",
                )
            },
        ),
    )


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
