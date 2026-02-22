from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from events.forms import EventForm
from events.models import TimeEvent

import logging

log = logging.getLogger(__name__)


class InfoView(LoginRequiredMixin, View):
    template_name = "base.html"
    login_url = "users:login"

    def get(self, request, *args, **kwargs):
        event = TimeEvent.objects.filter(
                user=request.user
            ).last()
        return render(
            request,
            self.template_name,
            {"event": event}
        )


class EventView(LoginRequiredMixin, View):
    template_name = "events/event.html"
    login_url = "users:login"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {}
        )

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            TimeEvent.objects.create(
                user=request.user,
                event_type=form.cleaned_data["action"],
                timestamp=request.timestamp
            )
            return redirect("events:info")
        return render(
            request,
            self.template_name,
            {}
        )

