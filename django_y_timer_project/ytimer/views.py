import json

from django.shortcuts import render
from django.http import HttpResponse


def default_timer_handler(request):
    from . import service

    sleep = 0
    try:
        service.handle_timer()
    except service.NoMoreTimerDue:
        sleep = 3

    return HttpResponse(json.dumps({
        'sleep': sleep
    }), content_type='application/json')