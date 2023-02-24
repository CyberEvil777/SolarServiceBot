from django.db import models
from django.utils import timezone

from src.accounts.models import User
from src.goods.models import Goods


class Order(models.Model):
    """Класс для хранение заказов"""

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    goods = models.ManyToManyField(Goods, verbose_name="Заказы", related_name="order")
    date_created = models.DateTimeField(
        verbose_name="Дата создания заказа", default=timezone.now
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
