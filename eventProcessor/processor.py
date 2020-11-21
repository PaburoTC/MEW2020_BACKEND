from queue import SimpleQueue
import requests
from .sensor import SensorType, TransmissionType
from .incidence import Incident

class Processor:

    def __init__(self):
        self.eventQueue = SimpleQueue()
        self.aggregatedEvents = {member: [] for name, member in SensorType}

    def add_event(self, event):
        self.eventQueue.put(event)

    def process_events(self):
        while True:
            next = self.eventQueue.get(block=True)
            incidences = self.suspect_event(next) # Para hacer output ig
            if not incidences:
                pass
            else:
                data = next.generateJSON()
                response = requests.post(url + '/postEvent', data)
                if response.status_code != 200:
                    print('AAAAAAAAAAAAAAA')

    def suspect_event(self, event):
        incidences = []
        if event.type == SensorType.SHOCK:
            if event.value in range(10, 20):
                incidences.append(Incident.fireworks)
            elif event.value in range(20, 60):
                incidences.append(Incident.storm)
            elif event.value in range(60, 101):
                incidences.append(Incident.earthquake)
        elif event.type == SensorType.SMOKE and event.value in range(70, 101):
            incidences.append(Incident.fire)
        elif event.type == SensorType.WATER and event.value in range(40, 101):
            incidences.append(Incident.flood)
        elif event.type == SensorType.INHIBITION and event.value in range(10,101):
            incidences.append(Incident.zone_inhibited)
        elif event.type == SensorType.AIR and event.value in range(60, 101):
            incidences.append(Incident.high_pollution)
        
        if event.battery:
            incidences.append(Incident.power_out)
        if event.medium != TransmissionType.ADSL:
            incidences.append(Incident.fiber_cut)
        elif event.medium == TransmissionType.SIGFOX:
            incidences.append(Incident.no_signal)
        
        return incidences 

