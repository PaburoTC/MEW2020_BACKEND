from sensor import ShockSensor, Location
from random import choice, randint
from time import sleep

installations = {
    90354: [1000, 1001, 1002, 1003, 1004, 1005],
    60000: [5000, 5001, 5002, 5003, 5004, 5005]
}


class SensorPool:
    def __init__(self):
        self.sensors = [ShockSensor('ES', choice(list(installations.values()))[i % 6], randint(1, 5), choice(list(Location.__members__.keys()))) for i in range(50)]

    def run(self):
        while True:
            sleep(randint(1, 10))
            for s in self.sensors:
                if randint(1, 20) == 1:
                    s.send_message()


SensorPool().run()
