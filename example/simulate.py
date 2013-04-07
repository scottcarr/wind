from data_source import data_source_tick
from data_sink import data_sink_tick

from fast_data import init_fast
from wind_monitor import init_wind_monitor
from wind_speed_alarm import init_wind_speed_alarm
from audio_data import init_audio_data
from crack_detection import init_crack_dection

if __name__ == '__main__':
    init_fast()
    init_wind_monitor()
    init_wind_speed_alarm()
    init_audio_data()
    init_crack_dection()
    for _ in range(50000):
        data_source_tick()
        data_sink_tick()
    
