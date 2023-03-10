from django.db import models

# Create your models here.


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
        return self.text[:5]
