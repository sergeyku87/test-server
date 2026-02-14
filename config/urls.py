from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="base.html"), name="base"),
    path("tg-user/", include("tg_users.urls")),
    path("users/", include("users.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
