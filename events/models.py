from django.db import models
from django.contrib.auth import get_user_model

from constants import MAX_COUNT_CHARS


class TimeEvent(models.Model):
    EVENT_TYPE = [
        ("clock_in", "Приход"),
        ("clock_out", "Уход"),
    ]

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name="events",
    )
    event_type = models.CharField(
        max_length=MAX_COUNT_CHARS,
        choices=EVENT_TYPE,
    )
    dt = models.DateTimeField(
        auto_now=True
    )
    timestamp = models.CharField(
        max_length=MAX_COUNT_CHARS,
    )

    def __str__(self):
        return f"{self.user} -> {self.event_type} -> {self.timestamp}"
