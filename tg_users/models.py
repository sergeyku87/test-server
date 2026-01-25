from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator

import re

MAX_COUNT_CHARS = 50


class TelegramUser(models.Model):
    chat_id = models.CharField(
        max_length=MAX_COUNT_CHARS,
        validators=[
            RegexValidator(
                r"^\d+$",
                message="Only digist",
                code="invalid_digists",
            ),
            MinLengthValidator(2),
        ]
    )
    first_name = models.CharField(
        max_length=MAX_COUNT_CHARS,
        validators=[MinLengthValidator(3)],
    )
    second_name = models.CharField(
        max_length=MAX_COUNT_CHARS,
        validators=[MinLengthValidator(3)]
    )
    father_name = models.CharField(
        max_length=MAX_COUNT_CHARS,
        validators=[MinLengthValidator(3)],
    )

    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.father_name}"

    def clean(self):
        ...
