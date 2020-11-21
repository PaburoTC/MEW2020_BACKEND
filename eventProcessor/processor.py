from queue import Queue, Empty
from .models import NotableIncidents, ExternalIncidents, Installation
from .sensor import SensorType, TransmissionType
from .incidence import Incident
from time import time

url = 'localhost:8080'

event_timeouts = {
    Incident.EARTHQUAKE.name: 20,
    Incident.FIRE.name: 60,
    Incident.STORM.name: 5,
    Incident.FLOOD.name: 60,
    Incident.POWER_OUT.name: 5,
    Incident.FIBER_CUT.name: 5,
    Incident.NO_SIGNAL.name: 5,
    Incident.ZONE_INHIBITED.name: 5,
    Incident.FIREWORKS.name: 5,
    Incident.HIGH_POLLUTION.name: 60,
}

event_thresholds = {
    Incident.EARTHQUAKE.name: 5,
    Incident.FIRE.name: 1,
    Incident.STORM.name: 2,
    Incident.FLOOD.name: 2,
    Incident.POWER_OUT.name: 2,
    Incident.FIBER_CUT.name: 2,
    Incident.NO_SIGNAL.name: 2,
    Incident.ZONE_INHIBITED.name: 2,
    Incident.FIREWORKS.name: 2,
    Incident.HIGH_POLLUTION.name: 2,
}


class Processor:

    def __init__(self):
        self.event_queue = Queue(1000000)
        self.aggregated_events = {name: set() for name in Incident.__members__.values()}

    def add_event(self, event):
        self.event_queue.put(event)

    def collect_events(self):
        last_time_processed = time()
        while True:
            try:
                e = self.event_queue.get(block=True, timeout=1)
                location = get_location(e)
                incidences = classify_event(e)
                for i in incidences:
                    self.aggregated_events[i].add((location, e))
            except Empty:
                pass

            if time() - last_time_processed >= 1:
                self.process_events()
                last_time_processed = time()

    def process_events(self):
        for incident_type in Incident.__members__.keys():
            locations = {}
            current_time = time()
            to_remove = []
            for loc, event in self.aggregated_events[incident_type]:
                if current_time - event.timestamp > event_timeouts[incident_type]:
                    to_remove.append(event)
                if loc not in locations:
                    locations[loc] = []
                locations[loc[1]].append(event)

            for loc, events in locations.items():
                if len(events) > event_thresholds[incident_type]:
                    ExternalIncidents(postal_code=loc, timestamp=events[0].timestamp, type=incident_type).save()
                else:
                    for event in events:
                        NotableIncidents(installation=event.installation, timestamp=event.timestamp, type=incident_type).save()
            for e in to_remove:
                self.aggregated_events[incident_type].discard(e)


def get_location(event):
    loc = Installation.objects.get(installation=event.installation, device=event.device)
    return loc.direction, loc.postal_code


def classify_event(event):
    incidences = []
    if event.type == SensorType.SHOCK:
        if event.value in range(10, 20):
            incidences.append(Incident.FIREWORKS)
        elif event.value in range(20, 60):
            incidences.append(Incident.STORM)
        elif event.value in range(60, 101):
            incidences.append(Incident.EARTHQUAKE)
    elif event.type == SensorType.SMOKE and event.value in range(70, 101):
        incidences.append(Incident.FIRE)
    elif event.type == SensorType.WATER and event.value in range(40, 101):
        incidences.append(Incident.FLOOD)
    elif event.type == SensorType.INHIBITION and event.value in range(10, 101):
        incidences.append(Incident.ZONE_INHIBITED)
    elif event.type == SensorType.AIR and event.value in range(60, 101):
        incidences.append(Incident.HIGH_POLLUTION)

    if event.battery:
        incidences.append(Incident.POWER_OUT)

    if event.medium != TransmissionType.ADSL:
        incidences.append(Incident.FIBER_CUT)
    elif event.medium == TransmissionType.SIGFOX:
        incidences.append(Incident.NO_SIGNAL)

    return incidences
