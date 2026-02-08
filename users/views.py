from django.shortcuts import render
from django.views import View


class ProbeView(View):
    def get(self, request):
        return render(request, "users/index.html", {})
