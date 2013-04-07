from data_sink import add_sink
from data_source import count_available_elements, remove_elements

label = "ramp_detected"

def cond():
    return count_available_elements(label)

def action():
    remove_elements(label, 1) # consume a warning
    print("[WARNING] wind speed too high!")

def init_wind_speed_alarm():
    add_sink(action, cond)

