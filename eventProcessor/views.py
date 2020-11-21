import json
from uuid import uuid1

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import datetime

from .models import Client, SessionID, ExternalIncidents, NotableIncidents
from .processor import Processor
from django.views.decorators.csrf import csrf_exempt

processor = Processor()


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)



@csrf_exempt
def login(request):
    if request.method == 'POST':
        client_data = request.body.decode().split('&')
        username = client_data[0].split('=')[1]
        pswd = client_data[1].split('=')[1]

        client = Client.objects.get(user=username, password=pswd)

        if client is not None:

            response = HttpResponse(status=301)
            response['Location'] = 'http://localhost:63343/uc3m-mew2020-frontend/index.html'
            uuid = uuid1()
            sessionID = SessionID(uuid, client.id, datetime.datetime.now(), datetime.datetime.now())
            sessionID.save()
            set_cookie(response, "sessionID", uuid, 1)
            return response

        return JsonResponse({"error": "Huvo un error"}, status=500)

@csrf_exempt
def post_event(request):
    if request.method == 'POST':
        event = json.loads(request.body)

        processor.addEvent(event)

        return

    return JsonResponse({'status': 404})


def get_incidents(request):
    if request.method == 'POST':
        result = []
        for incident in ExternalIncidents.objects.all():
            result.append(incident.serialize())

        for incident in NotableIncidents.objects.all():
            result.append(incident.serialize())

        return JsonResponse(result)
        

# Shock: 10-20 fireworks 20-60 storm (60,100] earthquake
# Smoke: 70-100 fire
# Water: 40-100 flood
# Inhibition:
# Air
