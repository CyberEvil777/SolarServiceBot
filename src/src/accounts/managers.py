from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone: str, password: str, **extra_fields):
        if not phone:
            raise ValueError(_("The Phone number must be set"))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_authorization", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone, password, **extra_fields)

    def get_by_tg_id(self, tg_id: str):
        return self.get(telegram_id=tg_id)

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None
