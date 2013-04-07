from data_source import remove_elements, count_available_elements, create_stream,\
        add_generator
import numpy as np

N = 100 # need 100 data points for a calculation
THRESHOLD = 12

label = "ramp_detected"
WINDVAR = "WindVxi"

def cond():
    if count_available_elements(WINDVAR) >= N:
        x = remove_elements(WINDVAR, N)
        #print x
        a = np.average(x)
        #print "[INFO] Average windspeed: {0}".format(a)
        if a > THRESHOLD:
            return True
        else:
            print "[INFO] wind speed normal."
    return False

def speed_detection():
    while 1:
        yield {label: True} 

def init_wind_monitor():
    create_stream(label)
    add_generator(speed_detection(), cond)

