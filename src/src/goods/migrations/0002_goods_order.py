# Generated by Django 4.1.4 on 2022-12-19 07:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0001_initial"),
        ("goods", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="goods",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="order.order",
                verbose_name="Заказы",
            ),
        ),
    ]
