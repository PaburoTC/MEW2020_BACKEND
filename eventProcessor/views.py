import json
from django.shortcuts import render
from django.http import JsonResponse
from queue import SimpleQueue

# Create your views here.
class Processor():

    def init(self):
        self.eventQueue = SimpleQueue()

    def addEvent(self, event):
        self.eventQueue.put(event)

    def processEvents(self):
        while True:
            next = self.eventQueue.get(block=True)

processor = Processor()


def post_event(request):
    if request.method == 'POST':
        event = json.loads(request.body)

        processor.addEvent(event)

        return

    return JsonResponse({'status': 404})


# Shock: 10-20 fireworks 20-60 storm (60,100] earthquake
# Smoke: 70-100 fire
# Water: 40-100 flood
# Inhibition:
# Air


