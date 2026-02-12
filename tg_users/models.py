from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth import get_user_model
from django.db import transaction

import logging

from constants import MAX_COUNT_CHARS, MIN_COUNT_CHARS
from utils import translit_ru, gen_seq

log = logging.getLogger(__name__)


class TelegramUser(models.Model):
    chat_id = models.CharField(
        max_length=MAX_COUNT_CHARS,
        unique=True,
        validators=[
            RegexValidator(
                r"^\d+$",
                message="Only digist",
                code="invalid_digists",
            ),
        ]
    )
    first_name = models.CharField(
        max_length=MAX_COUNT_CHARS,
        validators=[MinLengthValidator(MIN_COUNT_CHARS)],
    )
    second_name = models.CharField(
        max_length=MAX_COUNT_CHARS,
        validators=[MinLengthValidator(MIN_COUNT_CHARS)]
    )
    father_name = models.CharField(
        max_length=MAX_COUNT_CHARS,
        validators=[MinLengthValidator(MIN_COUNT_CHARS)],
    )

    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.father_name}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if get_user_model().objects.filter(chat_id=self.chat_id).exists():
                return
            try:
                username = f"{translit_ru(self.first_name)}_{translit_ru(self.second_name)}"
                get_user_model().objects.create(
                    username=username,
                    first_name=self.first_name,
                    last_name=self.second_name,
                    father_name=self.father_name,
                    password=gen_seq(),
                    chat_id=self.chat_id
                )
            except Exception as e:
                log.exception(f"Error create chat_id={self.chat_id}: {e}")
                raise


class TimeTracking(models.Model):
    EVENT_TYPE = [
        ("clockin", "Приход"),
        ("clockout", "Уход"),
    ]
    tg_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="tracking",
    )
    timestamp = models.DateTimeField(
        auto_now=True
    )
    event_type = models.CharField(
        max_length=MAX_COUNT_CHARS,
        choices=EVENT_TYPE,
    )
    time_as = models.CharField(
        max_length=MAX_COUNT_CHARS
    )


# def post_save_create(sender, created, instance, **kwargs):
#     if created:
#         try:
#             get_user_model().objects.create(
#                 username=f"{translit_ru(instance.first_name)}_{translit_ru(instance.second_name)}",
#                 first_name=instance.first_name,
#                 last_name=instance.second_name,
#                 father_name=instance.father_name,
#                 password=gen_seq(),
#                 chat_id=instance.chat_id
#             )
#         except:
#             instance.delete()
#             raise





