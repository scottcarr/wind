import numpy as np
from audio_data import label
from generate_audio_data import SAMPLE_RATE, DURATION, SAMPLE_RATE, EXCT_FREQ
from data_sink import add_sink
from data_source import count_available_elements, remove_elements

N = int(DURATION * SAMPLE_RATE) # number of samples we need
THRESHOLD = 2000

def cond():
    return count_available_elements(label) > N

def do_fft(s):
    f = abs(np.fft.fft(s))
    freqs = np.fft.fftfreq(len(s), d=1/SAMPLE_RATE)
    #idx = np.nonzero(freqs > 0)[0]
    return freqs, f

def detect_crack():
    s = remove_elements(label, N)
    freqs, fs = do_fft(s)
    if fs[EXCT_FREQ] < THRESHOLD:
        print("[WARNING] crack detected!")
    else:
        print("[INFO] no crack detected.")

def init_crack_dection():
    add_sink(detect_crack, cond)


