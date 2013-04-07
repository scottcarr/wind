#Wind App Example

##Introduction

I took the [pseudo code wind app](https://docs.google.com/document/d/1xNizt1E0xUc9zcHf25v3SOXoEDd_YKIUt5Skyh8KCuQ/edit?usp=sharing) and turned it into something that can run.

It used simulated data as its input.  See [here](where_data.md) for how the data is generated.

Key points:
- I wrote this by hand, but eventually I'd like to automatically generate this from the spec
- Almost everything is functional.  The only stateful part is the queue
- It's only written in Python so I could hack it up quickly

##Architecture

### Sources and Sinks

Everything is either a source or a sink.  Sources are generator functions that
yield a datum that is then placed on the queue.  Sinks remove these data from
the queue.  I give each stream a name to keep track of them.

The queue is really a double ended queue.  The source pushes data onto one end
and the sink pops data off the other.

Every source or sink generator function has a *cond* (short for condition).  A
*cond* is just a function that returns true when the generator is ready to
run or false otherwise.  For example, if I sink needs 100 data points, but the
queue only has 42 data points it in, the sink's *cond* should return false.

To create a new source:
- call create_source with the name of the source (any string)
- define two functions
  1. cond - a function that returns true when you want the gen to be called (probably always)
  2. gen - a generator function that yields a dictionary of the form {source_name: value}

See data_source.py for the associated code.

To create a new sink:
- call create_source with the name of the source (any string)
- define two functions
  1. cond - a function that returns true when you want the f to be called (probably when there is enough data in the queue)
  2. f - a function that does something with the data

See data_sink.py for the associated code.

### The main loop

The main loop is just a round robin calling of the generator functions
for all the sources and sinks.  Something better could be implemented later.
