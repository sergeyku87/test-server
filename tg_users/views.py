from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse

from tg_users.forms import TelegramUserForm
from tg_users.models import TelegramUser, TimeTracking

import logging
import re

log = logging.getLogger(__name__)

MSG_ERR = "Обязательные параметры отсутствуют или некорректны."


def validate_params(request):
    return (
        request.GET.get("chat_id")
        and request.GET.get("event")
        and re.match(r"^\d+$", request.GET.get("chat_id"))
        and request.GET.get("event") in ["clockin", "clockout"]
    )


def getting_and_saving(request):
    """
    Обрабатывает cобытия clock-in/clock-out для Telegram-пользователей.
    Принимает параметры chat_id и event через GET.
    Для POST обрабатывает форму создания TelegramUser.
    """
    if not validate_params(request):
        return render(
            request,
            "base.html",
            {"errors": MSG_ERR}
        )

    context = {}
    if request.method == "GET":
        try:
            tg_user = TelegramUser.objects.get(
                chat_id=request.GET.get("chat_id")
            )
            TimeTracking.objects.create(
                tg_user=tg_user,
                event_type=request.GET.get("event"),
                time_as=request.timestamp,
            )
            context.update({"tg_user": tg_user})
        except TelegramUser.DoesNotExist:
            context.update({"tg_user": None})
        except Exception as err:
            log.error(err)

    if request.method == "POST":
        form = TelegramUserForm(
            request.POST
        )
        if form.is_valid():
            form.save()
            log.info("TG User create")
            return redirect(
                request.get_full_path()
            )
        else:
            log.error(
                ";".join(
                    [f"Field: {k}, Error: {v}" for k, v in form.errors.as_data().items()]
                )
            )
            context.update({"errors": form.errors})
    return render(
        request,
        "tg_users/index.html",
        context
    )
