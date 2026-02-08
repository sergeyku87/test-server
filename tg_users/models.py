from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator

import re

from constants import MAX_COUNT_CHARS, MIN_COUNT_CHARS


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

    def clean(self):
        ...


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
