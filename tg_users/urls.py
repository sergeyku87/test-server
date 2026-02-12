from django.urls import re_path

from tg_users import views


app_name = "tg_users"


urlpatterns = [
    re_path("^(?P<chat_id>\d+)/$", views.CheckView.as_view(), name="index")
]
