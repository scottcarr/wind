from collections import namedtuple
import numpy as np

"""
Every data source should:
- register a stream name with create_stream
- add a generator function and a condition indicating
when that generator should fire with add_generator

the stream name can be any string

the generator function must return a dict where the keys
are stream name(s) and the values are the data
"""

all_streams = {}
all_generators = []

def compact(alist):
    """Transform a list into a representation FFTW can work on"""
    return np.asarray(alist)

def streamify(elements_dict):
    for label in elements_dict.iterkeys():
        all_streams[label].append(elements_dict[label])

def create_stream(label):
    all_streams[label] = []

def add_generator(f, cond):
    all_generators.append((f,cond))

def data_source_tick():
    for f, cond in all_generators:
        if cond():
            tmp = f.next()
            streamify(tmp)

def count_available_elements(label):
    return len(all_streams[label])

def remove_elements(label, count):
    tmp = all_streams[label][:count] # everything before count
    all_streams[label] = all_streams[label][count:] #everything after count
    return tmp

