from django.shortcuts import render, redirect
from django.views import View

from users.forms import ProbeUserForm

class ProbeView(View):
    def get(self, request, chat_id, *args, **kwargs):
        if not request.user.is_authenticated:
            form = ProbeUserForm()
            return render(request, "users/index.html", {"form": form})
        return render(request, "users/index.html", {})

    def post(self, request, chat_id, *args, **kwarg):
        form = ProbeUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:index", chat_id=chat_id)
        return render(request, "users/index.html", {"form": form})
