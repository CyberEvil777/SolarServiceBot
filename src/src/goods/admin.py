from django.contrib import admin
from django.contrib.auth.models import Group, User
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    SolarSchedule,
)

from src.goods.models import Goods


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    """Админка для модели еды"""

    list_display = (
        "title",
        "price",
        "shop",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "price",
                    "photo",
                    "shop",
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
