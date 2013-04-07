import numpy as np
from data_source import create_stream, add_generator
from generate_audio_data import GOOD_FILE, BAD_FILE

label = "audio"

DATA_FILE = GOOD_FILE
#DATA_FILE = BAD_FILE

def audio_read():
    data = np.load(DATA_FILE + ".npy")
    while 1:
        for i in range(data.shape[0]):
            yield {label: data[i]}

def init_audio_data():
    create_stream(label)
    cond = lambda: True # this generator should always fire
    add_generator(audio_read(), cond)
