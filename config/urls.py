from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    #path('admin/', admin.site.urls),
    path("", include("events.urls")),
    path("tg-user/", include("tg_users.urls")),
    path("users/", include("users.urls")),
]
