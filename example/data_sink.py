all_sinks = []

def add_sink(f, cond):
    all_sinks.append((f,cond))

def data_sink_tick():
    for f, cond in all_sinks:
        if cond():
            f()
