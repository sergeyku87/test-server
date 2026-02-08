from django.urls import path, re_path

from users.views import ProbeView

app_name = "users"

urlpatterns = [
    re_path("^/?$", ProbeView.as_view(), name="index"),
]
