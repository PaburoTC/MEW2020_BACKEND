from enum import Enum
from time import time
import requests
from .event import Event


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


url = ''


class Sensor:

    def __init__(self, installation, ID, location):
        self.installation = installation
        self.ID = ID
        self.location = location
        self.on_battery = False
        self.type = ''
        self.value = 0
        self.transmission_medium = TransmissionType.ADSL

    def send_message(self):
        event = Event(self, self.value, time())
        data = event.generateJSON()
        response = requests.post(url + '/postEvent', data)
        if response.status_code != 200:
            print('AAAAAAAAAAAAAAA')


class ShockSensor(Sensor):

    def __init__(self, installation, ID, location):
        Sensor.__init__(self, installation, ID, location)
        self.type = SensorType.SHOCK


class SmokeSensor(Sensor):

    def __init__(self, installation, ID, location):
        Sensor.__init__(self, installation, ID, location)
        self.type = SensorType.SMOKE


class WaterSensor(Sensor):

    def __init__(self, installation, ID, location):
        Sensor.__init__(self, installation, ID, location)
        self.type = SensorType.WATER


class InhibitionSensor(Sensor):

    def __init__(self, installation, ID, location):
        Sensor.__init__(self, installation, ID, location)
        self.type = SensorType.INHIBITION


class AirSensor(Sensor):

    def __init__(self, installation, ID, location):
        Sensor.__init__(self, installation, ID, location)
        self.type = SensorType.AIR
