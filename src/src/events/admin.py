from django.contrib import admin
from django.contrib.auth.models import Group, User
from django_celery_beat.models import (ClockedSchedule, CrontabSchedule,
                                       IntervalSchedule, SolarSchedule)

from src.events.models import EventMessage, Feature


# Register your models here.
@admin.register(EventMessage)
class EventMessageAdmin(admin.ModelAdmin):
    """Админка для модели EventMessage"""

    list_display = ("is_sent", "id_message")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "rule_info",
                    "keyfields",
                    "rule_description",
                    "id_incident",
                    "user_info",
                    "is_sent",
                    "is_full",
                )
            },
        ),
    )


@admin.register(Feature)
class EventMessageAdmin(admin.ModelAdmin):
    """Админка для модели EventMessage"""

    list_display = ("id_incident", "text_button")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id_incident",
                    "text_button",
                    "script",
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
