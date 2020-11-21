from queue import SimpleQueue, Empty
import requests
from .sensor import SensorType, TransmissionType
from .incidence import Incident
from time import time

url = 'localhost:8080'

event_timeouts = {
    Incident.EARTHQUAKE: 20,
    Incident.FIRE: 60,
    Incident.STORM: 5,
    Incident.FLOOD: 60,
    Incident.POWER_OUT: 5,
    Incident.FIBER_CUT: 5,
    Incident.NO_SIGNAL: 5,
    Incident.ZONE_INHIBITED: 5,
    Incident.FIREWORKS: 5,
    Incident.HIGH_POLLUTION: 60,
}

event_thresholds = {
    Incident.EARTHQUAKE: 5,
    Incident.FIRE: 1,
    Incident.STORM: 2,
    Incident.FLOOD: 2,
    Incident.POWER_OUT: 2,
    Incident.FIBER_CUT: 2,
    Incident.NO_SIGNAL: 2,
    Incident.ZONE_INHIBITED: 2,
    Incident.FIREWORKS: 2,
    Incident.HIGH_POLLUTION: 2,
}


class Processor:

    def __init__(self):
        self.event_queue = SimpleQueue()
        self.aggregated_events = {name: set() for name in Incident.__members__.values()}
        self.processed_events = []
        self.logged_incidents = []

    def add_event(self, event):
        self.event_queue.put(event)

    def collect_events(self):
        while True:
            try:
                e = self.event_queue.get(block=True, timeout=1)
                location = get_location(e)
                incidences = classify_event(e)
                if incidences[0] == Incident.BURGLARY:
                    self.processed_events.append((location, e))
                else:
                    for i in incidences:
                        self.aggregated_events[i].add((location, e))
            except Empty:
                self.process_events()

    def process_events(self):
        for incident_type in Incident.__members__.values():
            locations = {}
            current_time = time()
            to_remove = []
            for loc, event in self.aggregated_events[incident_type]:
                if current_time - event.timestamp > event_timeouts[incident_type]:
                    to_remove.append(event)
                if loc not in locations:
                    locations[loc] = []
                locations[loc].append(event)

            for loc, events in locations.items():
                if len(events) > event_thresholds[incident_type]:
                    self.logged_incidents.append((loc, incident_type))
                else:
                    for event in events:
                        self.processed_events.append((loc, incident_type, str(event.installation) + ":" + str(event.device)))

            for e in to_remove:
                self.aggregated_events[incident_type].discard(e)


def get_location(event):
    pass


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
