from django.contrib import admin

from src.shop.models import Shop, WinnerShop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """Админка для модели Заказ"""

    list_display = ("name",)

    fieldsets = (
        (
            None,
            {"fields": ("name",)},
        ),
    )


@admin.register(WinnerShop)
class WinnerShopAdmin(admin.ModelAdmin):
    """Админка для модели Заказ"""

    fieldsets = (
        (
            None,
            {"fields": ("shop",)},
        ),
    )
