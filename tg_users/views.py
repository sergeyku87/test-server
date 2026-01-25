from django.shortcuts import render

import logging

log = logging.getLogger(__name__)


def index(request):
    return render(request, "base.html", {})
