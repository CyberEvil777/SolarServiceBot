from django.contrib import admin

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
