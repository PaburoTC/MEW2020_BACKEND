from enum import Enum, auto


class Incident(Enum):
    earthquake = auto()
    fire = auto()
    storm = auto()
    flood = auto()
    power_out = auto()
    fiber_cut = auto()
    no_signal = auto()
    zone_inhibited = auto()
    fireworks = auto()
    high_pollution = auto()
    burglary = auto()
