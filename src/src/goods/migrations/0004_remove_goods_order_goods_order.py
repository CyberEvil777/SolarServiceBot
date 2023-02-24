# Generated by Django 4.1.4 on 2022-12-20 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0002_alter_order_user"),
        ("goods", "0003_alter_goods_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="goods",
            name="order",
        ),
        migrations.AddField(
            model_name="goods",
            name="order",
            field=models.ManyToManyField(
                null=True, related_name="goods", to="order.order", verbose_name="Заказы"
            ),
        ),
    ]
