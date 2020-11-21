from enum import Enum
from time import time
import requests
from event import Event


class Location(Enum):
    LIVING_ROOM = 'SALON',
    WINDOW = 'VENTANA',
    DOOR = 'PUERTA',
    KITCHEN = 'COCINA',
    BEDROOM = 'HABITACION',
    GARAGE = 'GARAJE',
    BASEMENT = 'SOTANO',
    BATHROOM = 'BAÑO',


class SensorType(Enum):
    SHOCK = 'SHOCK'
    SMOKE = 'SMOKE'
    WATER = 'WATER'
    INHIBITION = 'INHIBITION'
    AIR = 'AIR'


class TransmissionType(Enum):
    ADSL = 'ADSL'
    GPRS = 'GPRS'
    SMS = 'SMS'
    SIGFOX = 'SIGFOX'


url = 'localhost:8080'


class Sensor:

    def __init__(self, country, installation, ID, location):
        self.country = country
        self.installation = installation
        self.ID = ID
        self.location = location
        self.on_battery = False
        self.type = ''
        self.value = 0
        self.transmission_medium = TransmissionType.ADSL

    def send_message(self, depth=0):
        event = Event(self, self.value, time())
        data = event.generateJSON()
        response = requests.post(url + '/postEvent', data)
        if response.status_code != 200 and depth < 50:
            self.send_message(depth + 1)
        else:
            print('AAAAAAAA')


class ShockSensor(Sensor):

    def __init__(self, country, installation, ID, location):
        Sensor.__init__(self, country, installation, ID, location)
        self.type = SensorType.SHOCK


class SmokeSensor(Sensor):

    def __init__(self, country, installation, ID, location):
        Sensor.__init__(self, country, installation, ID, location)
        self.type = SensorType.SMOKE


class WaterSensor(Sensor):

    def __init__(self, country, installation, ID, location):
        Sensor.__init__(self, country, installation, ID, location)
        self.type = SensorType.WATER


class InhibitionSensor(Sensor):

    def __init__(self, country, installation, ID, location):
        Sensor.__init__(self, country, installation, ID, location)
        self.type = SensorType.INHIBITION


class AirSensor(Sensor):

    def __init__(self, country, installation, ID, location):
        Sensor.__init__(self, country, installation, ID, location)
        self.type = SensorType.AIR
