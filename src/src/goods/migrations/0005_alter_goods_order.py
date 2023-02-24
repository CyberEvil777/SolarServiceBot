# Generated by Django 4.1.4 on 2022-12-20 07:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0002_alter_order_user"),
        ("goods", "0004_remove_goods_order_goods_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goods",
            name="order",
            field=models.ManyToManyField(
                related_name="goods", to="order.order", verbose_name="Заказы"
            ),
        ),
    ]