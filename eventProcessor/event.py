import json


class Event:

    def __init__(self, sensor, value, datetime):
        self.country = sensor.country
        self.installation = sensor.installation
        self.device = sensor.ID
        self.type = sensor.type
        self.medium = sensor.transmission_medium
        self.battery = sensor.on_battery
        self.location = sensor.location
        self.timestamp = datetime
        self.value = value

    def generateJSON(self):
        return json.dumps({
            'country': self.country,
            'installation': self.installation,
            'device': self.device,
            'type': self.type.name,
            'medium': self.medium.name,
            'battery': self.battery,
            'location': self.location,
            'timestamp': self.timestamp,
            'value': self.value
        })
