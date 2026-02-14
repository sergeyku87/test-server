from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

from users.views import CustomLoginView, CustomCreateView


app_name = "users"

urlpatterns = [
    re_path("^login/$", CustomLoginView.as_view(), name="login"),
    re_path("^logout/$", LogoutView.as_view(), name="logout"),
    re_path("^registration/$", CustomCreateView.as_view(), name="registration"),
    #re_path("auth/?$", LoginView.as_view(), name="login"),
    #re_path("^(?P<chat_id>\d+)/$", ProbeView.as_view(), name="index"),

]
