from enum import Enum


class Incident(Enum):
    EARTHQUAKE = "Terremoto"
    FIRE = "Incendio"
    STORM = "Tormenta"
    FLOOD = "Inundación"
    POWER_OUT = "Corte Red Eléctrica"
    FIBER_CUT = "Corte de Fibra de Internet"
    NO_SIGNAL = "Zona sin Cobertura Móvil"
    ZONE_INHIBITED = "Zona Inhibida"
    FIREWORKS = "Fuegos Artificiales"
    HIGH_POLLUTION = "Alta Contaminación"
