from django.urls import re_path
from django.views.generic import TemplateView

from events.views import EventView, EventsListView


app_name = "events"

urlpatterns = [
    re_path(r"^events/$", EventsListView.as_view(), name="events-list"),
    re_path(r"^events/create/$", EventView.as_view(), name="event-create"),
]
