from django.db import models

# Create your models here.


class Shop(models.Model):
    """Магазин еды"""

    name = models.CharField(verbose_name="Магазин", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин Яндекс еды"
        verbose_name_plural = "Магазины Яндекс еды"


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class WinnerShop(SingletonModel):
    shop = models.OneToOneField(
        Shop,
        verbose_name="Магазин с Яндекс еды",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"Сегодня кушаем в {self.shop}"

    class Meta:
        verbose_name = "Победитель голосования"
        verbose_name_plural = "Победитель голосования"
