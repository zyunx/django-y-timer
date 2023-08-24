import json

from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict

from .models import Task


def tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        return HttpResponse(json.dumps([{
            'id': t.id,
            'title': t.title,
            'timeout_in_seconds': t.timeout_in_seconds,
            'status': t.status,
            'timeout_timer_id': str(t.timeout_timer_id),
            'poll_status_timer_id': str(t.poll_status_timer_id),
        } for t in tasks], indent=2), content_type='application/json')
    elif request.method == 'POST':
        task = Task.objects.create(title=request.POST['title'], timeout_in_seconds=int(request.POST['timeout_in_seconds']))
        task.run()
        return HttpResponse()
    