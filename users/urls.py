from django.urls import path, re_path
from django.contrib.auth.views import LoginView


app_name = "users"

urlpatterns = [
    #re_path("auth/?$", LoginView.as_view(), name="login"),
    #re_path("^(?P<chat_id>\d+)/$", ProbeView.as_view(), name="index"),

]
