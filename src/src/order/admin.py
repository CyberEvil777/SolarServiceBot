from django.contrib import admin
from django.utils import timezone

from src.order.models import Order


class CustomRecordsFilter(admin.SimpleListFilter):
    title = "Заказы"
    parameter_name = "old_records"
    TODAY = "Заказы на сегодня"

    def lookups(self, request, model_admin):
        return (
            (self.TODAY, self.TODAY),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == self.TODAY:
            queryset = queryset.filter(
                date_created__gte=timezone.now().date(),
            ).order_by("date_created")
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админка для модели Заказ"""

    list_display = (
        "date_created",
        "user",
    )
    readonly_fields = ("date_created", "user",)

    list_filter = (
        CustomRecordsFilter,)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "date_created",
                    "user",
                    "goods",
                )
            },
        ),
    )
