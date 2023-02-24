from django.contrib import admin

from src.accounts.models import User


# Register your models here.
@admin.register(User)
class OrderAdmin(admin.ModelAdmin):
    """Админка для модели Заказ"""

    list_display = ("name",)
    readonly_fields = (
        "username",
        "telegram_id",
        "date_joined",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "username",
                    "telegram_id",
                    "date_joined",
                )
            },
        ),
    )
