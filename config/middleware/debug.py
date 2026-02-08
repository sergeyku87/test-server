from django.utils import timezone as tz

import logging

log = logging.getLogger("django.request.ip")


class DebugIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        addr = request.META.get("REMOTE_ADDR", "unknow")
        response = self.get_response(request)
        log.debug(
            f'REMOTE_ADDR: {addr}; CODE: {response.status_code}'
            )
        return response


class TimeStampMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.timestamp = tz.localtime(tz.now()).strftime("%d.%m.%Y %H:%M")
        return self.get_response(request)
