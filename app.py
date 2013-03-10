# TODO: read multiple files to simulate 2 sensors

import numpy as np
from collections import namedtuple

Datum = namedtuple("Datum" \
        ,["Time" \
        , "WindVxi"\
        , "WindVyi"	\
        , "WindVzi" \
        , "HorWndDir" \
        , "VerWndDir" \
        , "BldPitch2" \
        , "IPDefl1" \
        , "IPDefl2" \
        , "TwstDefl1" \
        , "TwstDefl2" \
        , "TwstDefl3"	
        , "RootMxb2"	
        , "RootMyb2" \
        , "RootMzb2" \
        , "LSShftFys" \
        , "LSShftFzs" \
        , "LSSTipMys" \
        , "LSSTipMzs" \
        , "YawBrTDxp" \
        , "YawBrTDyp" \
        , "YawBrMxn" \
        , "YawBrMyn" \
        , "YawBrMzn"
         ]
)

def read_input():
    # read the input file one line at a time as though we were sampling
    # a real set of sensors
    f = open("Test13.out")
    i = 0
    for line in f.readlines():
        # there are 8 lines of header
        if i < 8:
            i += 1
        else:
            yield line

def unpack_line(lines):
    # split up the line and put it in a struct
    for line in lines:
        yield Datum(*map(float, (line.split())))

def windowed_average(data):
    # say we want to have at least N samples and then take the average
    # we now need to pool N samples into an array
    sig = []
    N = 100
    for d in data:
        sig.append(d.WindVxi)
        if len(sig) == N:
            ans = sum(sig)/N
            sig = []
            yield ans 

def classify(sig):
    # run a classifier on the each average from the previous step
    for s in sig:
        if s > 11.5: # a completely made up classifier
            yield "OK. Average {0}.".format(s)
        else:
            yield "DANGER! Average {0}.".format(s)


if __name__ == '__main__':
    theapp = classify(windowed_average(unpack_line(read_input())))
    while 1:
        try:
            print theapp.next()
        except StopIteration:
            print "done." # out of data
            break

