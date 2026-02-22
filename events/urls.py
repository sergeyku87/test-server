from django.urls import re_path
from django.views.generic import TemplateView

from events.views import EventView, InfoView


app_name = "events"

urlpatterns = [
    re_path(r"^$", TemplateView.as_view(template_name="base.html"), name="home"),
    re_path(r"^info/$", InfoView.as_view(), name="info"),
    re_path(r"^events/$", EventView.as_view(), name="event"),
]
