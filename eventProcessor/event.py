import json


class Event:

    def __init__(self, sensor, value, datetime):
        self.country = sensor.client.country
        self.installation = sensor.client.ID
        self.device = sensor.ID
        self.type = sensor.type
        self.medium = sensor.transmission_medium
        self.battery = sensor.on_battery
        self.location = sensor.location
        self.timestamp = datetime
        self.value = value

    def generateJSON(self):
        return json.dumps(self)
