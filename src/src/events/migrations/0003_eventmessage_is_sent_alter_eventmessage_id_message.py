# Generated by Django 4.1.7 on 2023-02-24 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0002_rename_event_eventmessage"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventmessage",
            name="is_sent",
            field=models.BooleanField(default=False, verbose_name="Отправлено"),
        ),
        migrations.AlterField(
            model_name="eventmessage",
            name="id_message",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="id сообщения"
            ),
        ),
    ]
