from pylab import *
import numpy as np

PUMPING_FREQ = 10.0 #Hz
EXCT_FREQ = 1000.0 #Hz
SAMPLE_RATE = 5000.0 #Hz
DURATION = 1.0 # seconds

BAD_FREQ_DELTA_F = 100 # Hz

GOOD_FILE = "good_audio_data"
BAD_FILE = "bad_audio_data"

def do_fft(s, n):
    figure(n); clf();
    f = abs(np.fft.fft(s))
    freqs = np.fft.fftfreq(len(s), d=1/SAMPLE_RATE)
    idx = np.nonzero(freqs > 0)[0]
    plot(freqs[idx], f[idx])
    
def make_good_data():
    spump = np.sin(2*np.pi*PUMPING_FREQ*t)
    sext = np.sin(2*np.pi*EXCT_FREQ*t)
    sig = sext + spump
    np.save(GOOD_FILE, sig)
    return sig

def make_bad_data():
    spump = np.sin(2*np.pi*PUMPING_FREQ*t)
    sext = 0.4 * np.sin(2*np.pi*EXCT_FREQ*t)
    sext1 = 0.3 * np.sin(2*np.pi*(EXCT_FREQ-BAD_FREQ_DELTA_F)*t)
    sext2 = 0.3 * np.sin(2*np.pi*(EXCT_FREQ+BAD_FREQ_DELTA_F)*t)
    sig = sext + sext1 + sext2 + spump
    np.save(BAD_FILE, sig)
    return sig

def make_files():
    make_bad_data()
    make_good_data()

def test_data():
    sgood = np.load(GOOD_FILE + ".npy")
    sbad = np.load(BAD_FILE + ".npy")
    do_fft(sgood, 1)
    do_fft(sbad, 2)

if __name__ == '__main__':
    ion()
    t = np.r_[0:DURATION:1/SAMPLE_RATE]
    make_files()
    test_data()

