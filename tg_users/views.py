from django.shortcuts import render
from django.utils import timezone

import logging

log = logging.getLogger(__name__)


def index(request):
    context = {"chat_id": None, "is_auth": False}
    if request.method == "GET" and request.GET.get("chat_id"):
        context["chat_id"] = request.GET.get("chat_id")
        context["is_auth"] = True
    if request.method == "POST":
        log.debug(request.POST)
    return render(request, "base.html", context)
