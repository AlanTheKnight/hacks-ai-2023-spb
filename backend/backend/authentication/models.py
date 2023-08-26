from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from backend.authentication.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    is_active = models.BooleanField("Активный", default=True)
    is_staff = models.BooleanField("Администратор", default=False)
    is_admin = models.BooleanField("Администратор", default=False)

    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    photo_url = models.URLField("Аватар", default=None, null=True)
    username = models.CharField("Логин", max_length=100, unique=True)
    telegram_id = models.IntegerField("Telegram ID")

    date_joined = models.DateTimeField("Дата регистрации", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "telegram_id"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.get_username()
