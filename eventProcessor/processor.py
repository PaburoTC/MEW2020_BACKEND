from queue import SimpleQueue
import requests
from .sensor import SensorType


# Shock: [10,20) fireworks [20,60) storm [60,100] Teremoto
# Smoke: [70,100] Incendio
# Water: [40,100] Inundación
# Inhibition: [10,100] Zona Inhibida
# Air: [60,100] Alta contaminación

# self.battery: Corte Red Eléctrica
# self.medium != ADSL: Corte de Fibra de Internet
#            == SIGFOX: Zona sin Cobertura Móvil


class Processor:

    def __init__(self):
        self.eventQueue = SimpleQueue()
        self.aggregatedEvents = {member: [] for name, member in SensorType}

    def add_event(self, event):
        self.eventQueue.put(event)

    def process_events(self):
        while True:
            next = self.eventQueue.get(block=True)
            if not self.suspect_event(next):
                pass
            else:
                data = next.generateJSON()
                response = requests.post(url + '/postEvent', data)
                if response.status_code != 200:
                    print('AAAAAAAAAAAAAAA')

    def suspect_event(self, event):
        if event.type == SensorType.SHOCK:
            if
        elif event.type == SensorType.SMOKE:
        elif event.type == SensorType.WATER:
        elif event.type == SensorType.INHIBITION:
        elif event.type == SensorType.AIR:
            return false

