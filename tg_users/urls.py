from django.urls import re_path

from tg_users.views import index


app_name = "tg_users"


urlpatterns = [
    re_path("^$", index, name="index")
]
