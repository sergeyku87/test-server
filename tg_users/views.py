from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.views.generic import View
from django.core.exceptions import ValidationError

from tg_users.forms import TelegramUserForm
from tg_users.models import TelegramUser, TimeTracking
from utils import decrypt

import logging
import re


log = logging.getLogger(__name__)
ID = lambda n: decrypt(n)


class CheckView(View):
    def dispatch(self, request, *args, **kwargs):
        real_id = ID(kwargs.get("chat_id"))
        kwargs["chat_id"] = real_id
        self.kwargs["chat_id"] = real_id
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, chat_id, *args, **kwargs):
        if TelegramUser.objects.filter(chat_id=chat_id).exists():
            tg_user = TelegramUser.objects.get(chat_id=chat_id)
            user = get_user_model().objects.get(chat_id=chat_id)
            login(request, user)
            try:
                valid_events = dict(TimeTracking.EVENT_TYPE).keys()
                if not request.GET.get("event") in valid_events:
                    raise ValidationError("Not named param in ulr")
                TimeTracking.objects.create(
                    tg_user=tg_user,
                    event_type=request.GET.get("event"),
                    time_as=request.timestamp,
            )
            except Exception as err:
                log.error(err)
        else:
            if request.user:
                logout(request)
        return render(request, "tg_users/index.html", {})

    def post(self, request, chat_id, *args, **kwargs):
        form = TelegramUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.get_full_path())
        log.error(form.errors.as_data())
        return render(request, "tg_users/index.html", {})


# MSG_ERR = "Обязательные параметры отсутствуют или некорректны."


# def validate_params(request):
#     return (
#         request.GET.get("chat_id")
#         and request.GET.get("event")
#         and re.match(r"^\d+$", request.GET.get("chat_id"))
#         and request.GET.get("event") in ["clockin", "clockout"]
#     )


# def getting_and_saving(request):
#     """
#     Обрабатывает cобытия clock-in/clock-out для Telegram-пользователей.
#     Принимает параметры chat_id и event через GET.
#     Для POST обрабатывает форму создания TelegramUser.
#     """
#     if not validate_params(request):
#         return render(
#             request,
#             "base.html",
#             {"errors": MSG_ERR}
#         )

#     context = {}
#     if request.method == "GET":
#         try:
#             tg_user = TelegramUser.objects.get(
#                 chat_id=request.GET.get("chat_id")
#             )
#             TimeTracking.objects.create(
#                 tg_user=tg_user,
#                 event_type=request.GET.get("event"),
#                 time_as=request.timestamp,
#             )
#             context.update({"tg_user": tg_user})
#         except TelegramUser.DoesNotExist:
#             context.update({"tg_user": None})
#         except Exception as err:
#             log.error(err)

#     if request.method == "POST":
#         form = TelegramUserForm(
#             request.POST
#         )
#         if form.is_valid():
#             form.save()
#             log.info("TG User create")
#             return redirect(
#                 request.get_full_path()
#             )
#         else:
#             log.error(
#                 ";".join(
#                     [f"Field: {k}, Error: {v}" for k, v in form.errors.as_data().items()]
#                 )
#             )
#             context.update({"errors": form.errors})
#     return render(
#         request,
#         "tg_users/index.html",
#         context
#     )
