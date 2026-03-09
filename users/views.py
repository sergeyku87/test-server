from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.views.generic import View

from users.forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
)

import logging

log = logging.getLogger(__name__)


class CustomLoginView(View):
    template_name = "users/login.html"

    def _set_no_cache_headers(self, response):
        """Устанавливает заголовки, запрещающие кэширование"""
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def get(self, request, *args, **kwargs):
        response = render(
            request,
            self.template_name,
            {"form": CustomAuthenticationForm()}
        )
        return self._set_no_cache_headers(response)

    def post(self, request, *args, **kwargs):
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and user.is_active:
                login(request, user)
                return redirect("events:events-list")

        return render(
            request,
            self.template_name,
            {"form": form}
        )


class CustomCreateView(View):
    template_name = "users/registration.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"form": CustomUserCreationForm()}
        )

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            log.info("; ".join([f"{k}: {v}" for k,v in form.cleaned_data.items()]))
            user = form.save()
            login(request, user)
            return redirect("/")
        return render(
            request,
            self.template_name,
            {"form": form}
        )
