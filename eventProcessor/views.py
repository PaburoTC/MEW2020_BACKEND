import json
from django.shortcuts import render
from django.http import JsonResponse
from .processor import Processor

# Create your views here.


processor = Processor()


def post_event(request):
    if request.method == 'POST':
        event = json.loads(request.body)

        processor.add_event(event)

        return

    return JsonResponse({'status': 404})


