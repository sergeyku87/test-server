from django.shortcuts import render, redirect
from django.db.models import Count, Max, Min, Q
from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncDate
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from events.forms import EventForm
from events.models import TimeEvent

import logging

log = logging.getLogger(__name__)


class EventsListView(LoginRequiredMixin, ListView):
    template_name = "events/events-list.html"
    context_object_name = "events"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return TimeEvent.objects.annotate(
                date=TruncDate('dt')
            ).values(
                'user__username',
                'date',
            ).annotate(
                clock_in_time=Min(
                    'dt',
                    filter=Q(event_type='clock_in')
                ),
                clock_out_time=Max(
                    'dt',
                    filter=Q(event_type='clock_out')
                )
            ).annotate(
                work_duration=ExpressionWrapper(
                    F('clock_out_time') - F('clock_in_time'),
                    output_field=DurationField()
                )
            ).order_by('date', 'user__username')
        return TimeEvent.objects.filter(
            user=self.request.user
        ).annotate(
            date=TruncDate("dt")
        ).order_by("date")

    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # if self.request.user.is_superuser:
        #     for value in data.get("events"):
        #         if value.get("event_type") == "clock_in":
        #             value["event_type"] = "Приход"
        #         elif value.get("event_type") == "clock_out":
        #             value["event_type"] = "Уход"
        return data


class EventView(LoginRequiredMixin, View):
    template_name = "events/event-create.html"
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
            return redirect("events:events-list")
        return render(
            request,
            self.template_name,
            {}
        )

