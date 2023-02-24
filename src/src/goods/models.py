import base64
import os

from django.conf import settings
from django.db import models

from src.shop.models import Shop


def user_directory_path(instance, filename):
    """Функция выдает путь к загруженному файлу"""
    return f"goods/{instance.title}/{filename}"


def image_as_base64(image_file, format="png"):
    """
    :param `image_file` for the complete path of image.
    :param `format` is format for image, eg: `png` or `jpg`.
    """
    # if not os.path.isfile(image_file):
    #     return None

    encoded_string = ""
    with open(image_file, "rb") as img_f:
        encoded_string = base64.b64encode(img_f.read())
    return f'data:image/{format};base64,{encoded_string.decode("utf-8")}'


class Goods(models.Model):
    """Товары"""

    title = models.CharField(verbose_name="Название", max_length=150)
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.CharField(
        verbose_name="Описание", max_length=150, default="Пусто"
    )
    photo = models.ImageField(verbose_name="Фото товара", upload_to=user_directory_path)
    shop = models.ForeignKey(
        Shop,
        verbose_name="Магазин с Яндекс еды",
        null=True,
        on_delete=models.CASCADE,
    )

    def get_convert_base64(self, obj):
        # settings.MEDIA_ROOT = '/path/to/env/projectname/media'
        return image_as_base64(obj.photo.path)

    def __str__(self):
        return f"{self.title} {self.price}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
