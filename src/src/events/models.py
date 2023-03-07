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
    # id_elasticsearch = models.CharField

    @property
    def short_text(self):
        return self.text[:5]
