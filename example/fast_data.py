from data_source import create_stream, add_generator

labels = ["Time","WindVxi","WindVyi","WindVzi","HorWndDir","VerWndDir", \
    "BldPitch2","IPDefl1","IPDefl2","TwstDefl1","TwstDefl2","TwstDefl3", "RootMxb2"\
    , "RootMyb2", "RootMzb2", "LSShftFys", "LSShftFzs", "LSSTipMys", "LSSTipMzs",\
    "YawBrTDxp", "YawBrTDyp", "YawBrMxn", "YawBrMyn", "YawBrMzn"]

def line_to_dict(labels, line):
    values = map(float, (line.split()))
    return {label: value for (label, value) in zip(labels, values)}

def fast_read():
    while 1: # loop forever
        f = open("Test13.out")
        i = 0
        for line in f.readlines():
        # there are 8 lines of header
            if i < 8:
                i += 1
            else:
                yield line_to_dict(labels, line)
        f.close()

def init_fast():
    for l in labels:
        create_stream(l)
    cond = lambda: True # this generator should always fire
    add_generator(fast_read(), cond)

