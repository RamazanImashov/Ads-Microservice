from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
import logging

logger = logging.getLogger('config')


class UserManager(BaseUserManager):
    def _create(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create(username, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=40, verbose_name="Имя пользевателя")
    email = models.EmailField(blank=True, null=True, verbose_name="Почта")
    phone_number = models.CharField(max_length=30, blank=True,
                                    null=True, verbose_name="Номер телефона (номер должен начинаться с +)")

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} - {self.email} - {self.phone_number}"

