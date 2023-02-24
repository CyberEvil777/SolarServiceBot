# Generated by Django 4.1.4 on 2022-12-20 07:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_order_goods"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"verbose_name": "Заказ", "verbose_name_plural": "Заказы"},
        ),
        migrations.AddField(
            model_name="order",
            name="date_created",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Дата создания заказа"
            ),
        ),
    ]
