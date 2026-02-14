from django.db import models
from django.contrib.auth.models import AbstractUser

from constants import MAX_COUNT_CHARS


class CustomUser(AbstractUser):
    chat_id = models.CharField(
        max_length=MAX_COUNT_CHARS,
        blank=True,
        null=True,
        verbose_name="Телеграмм ID",
    )
    father_name = models.CharField(
        max_length=MAX_COUNT_CHARS,
        blank=True,
        null=True,
        verbose_name="Отчество",
    )
