from django.shortcuts import render

import logging

log = logging.getLogger(__name__)


def index(request):
    context = {"body": {"ass": "big", "cunt": "small"}}
    return render(request, "base.html", context)
