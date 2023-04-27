from django.db import models

# Create your models here.


def user_directory_path(instance, filename):
    """Функция выдает путь к загруженному файлу в разделе Мой Профиль"""
    return f"{instance.__class__.__name__}/{instance.id_incident}/{filename}"


class EventMessage(models.Model):
    """Инцидент с elasticsearch Wazuh"""

    text = models.TextField(
        verbose_name="Текст инцидента",
        help_text="Текст сообщения, которое приходит если произошел инцидент",
    )
    id_message = models.CharField(
        verbose_name="id сообщения", max_length=50, blank=True, null=True
    )
    is_full = models.BooleanField(default=False)
    is_sent = models.BooleanField(verbose_name="Отправлено", default=False)

    rule_info = models.CharField(
        verbose_name="Наименование инцидента", max_length=255, null=True, blank=True
    )
    keyfields = models.CharField(
        verbose_name="Ключь с ElasticSearch", max_length=255, null=True, blank=True
    )
    rule_description = models.CharField(
        verbose_name="Описание", max_length=255, null=True, blank=True
    )
    id_incident = models.CharField(
        verbose_name="ID инцидента", max_length=255, null=True, blank=True
    )
    user_info = models.CharField(
        verbose_name=" Информация о пользователе", max_length=255, null=True, blank=True
    )

    @property
    def short_text(self):
        msg = (
            f" #{self.id_incident.replace('-','_')} \n"
            f"☢️ {self.rule_info}\n\n"
            f"Описание Инцидента:\n"
            f"{self.rule_description}\n\n"
            f"KeyFields:\n"
            f"{self.keyfields}\n\n"
            f"ID инцидента: {self.id_incident}\n"
        )
        return msg

    @property
    def full_text(self):
        msg = (
            f" #{self.id_incident.replace('-','_')} \n"
            f"☢️ {self.rule_info}\n\n"
            f"Описание Инцидента:\n"
            f"{self.rule_description}\n\n"
            f"KeyFields:\n"
            f"{self.keyfields}\n\n"
            f"ID инцидента: {self.id_incident}\n\n"
            f"Информация о пользователе\n"
            f"{self.user_info or 'Отсутствует'}\n"
        )
        return msg


class Feature(models.Model):
    id_incident = models.CharField(
        verbose_name="ID инцидента", max_length=255, null=True, blank=True
    )

    text_button = models.CharField(
        verbose_name="Текст, который будет отображаться в названии кнопки",
        max_length=255,
        null=True,
        blank=True,
    )

    script = models.FileField(
        upload_to=user_directory_path,
        verbose_name="Скрипт",
        help_text="Запускается при нажатии на кнопку",
        blank=True,
    )
