from enum import Enum, auto


class Incident(Enum):
    earthquake = "Terremoto"
    fire = "Incendio"
    storm = "Tormenta"
    flood = "Inundación"
    power_out = "Corte Red Eléctrica"
    fiber_cut = "Corte de Fibra de Internet"
    no_signal = "Zona sin Cobertura Móvil"
    zone_inhibited = "Zona Inhibida"
    fireworks = "Fuegos Artificiales"
    high_pollution = "Alta Contaminación"
    burglary = "Robo"
