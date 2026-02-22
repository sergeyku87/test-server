from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

from users.views import CustomLoginView, CustomCreateView


app_name = "users"

urlpatterns = [
    re_path(r"^login/$", CustomLoginView.as_view(), name="login"),
    re_path(r"^logout/$", LogoutView.as_view(), name="logout"),
    re_path(r"^registration/$", CustomCreateView.as_view(), name="registration"),
]
