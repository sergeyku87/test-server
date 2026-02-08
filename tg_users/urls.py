from django.urls import re_path

from tg_users.views import getting_and_saving


app_name = "tg_users"


urlpatterns = [
    re_path("^$", getting_and_saving, name="getting_and_saving")
]
