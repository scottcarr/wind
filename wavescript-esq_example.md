#A wavescript inspired example

##Introduction 

The main idea is if our application is a series of nested function calls:
- The compiler can do any optimizations which preserve the function semantics
- It doesn't matter where the function runs as long as the order is maintained.

Each function must:
- Accept as input one or more return values of its callee functions
- Output a new value that is a pure function of those inputs

##Stream processing in Python
Python isn't purely functional, but it can do stream processing using the 
*yield* key word.  *Yield* allows the programmer to build generator functions.
For example:

    def simple_generator():
        for i in range(10):
            yield i

    x = simple_generator()
    x.next() # is 0
    x.next() # is 1
    x.next() # is 2
    .
    .
    .
        
We can use this to model a stream of sensor readings:

    def simulated_sensor():
        f = open("sensor.txt")
        for line in f:
            yield f

    readings = simulated_sensor()
    readings.next() # returns the first "reading"
    readings.next() # returns the second "reading"
    .
    .
    .

With these generator functions we can build up a simulated stream processing
application.

##An example

The following function reads the sensor data file as above:

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

For confidence, I define a *namedtuple* (essentially a struct) for holding each
"reading."

    def unpack_line(lines):
        # split up the line and put it in a struct
        for line in lines:
            yield Datum(*map(float, (line.split())))

This looks a little complicated, but it's not.  I'm using the output of the FAST
simulation as my simulated sensor.  Each line is tab separated.  *line.split()*
returns a list of a strings partitioned by white space. *map(float, alist)* applies
the function *float* to each item of alist.  In this case each item
is text string like "1.2323" and float("1.2323") is just the float 1.2323.  The
asterisk (pronounced "splat") makes a list into the arguments of a function.  For
example:

    def printstuff(x,y,z):
        print x,y,z

    k = [1,2,3]
    printstuff(*k) # prints: 1, 2, 3

Now we could define a mini-stream processing app like:

    x = unpack_line(read_input())
    while 1:
        x.next()

Where each call of x.next() *yields* a *namedtuple* of type *Datum*.  The details
of the *Datum* tuple are not relevant at this point.

Note that the for loop in *unpack_lines* only reads as many lines as it needs
to calculate whatever it's returning with *yield*.  The complete list of readings
never exists in memory.

Now, lets do a calculation over the tuples.

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

This is more interesting because it doesn't just:
1. read 
2. calculate 
3. yield 
4. goto 1

It pools a chunk of 100 tuples and then calculates an average over the window. 
Again, it doesn't read in the whole list, but just 100 samples at a time.

Doing something with the averages is simple since we just readsin one average and yield
one result.

    def classify(sig):
        # run a classifier on the each average from the previous step
        for s in sig:
            if s > 11.5: # a completely made up classifier
                yield "OK. Average {0}.".format(s)
            else:
                yield "DANGER! Average {0}.".format(s)

Now we can build a complete stream processing simulation.

    theapp = classify(windowed_average(unpack_line(read_input())))
    while 1:
        try:
            print theapp.next()
        except StopIteration:
            print "done." # out of data
            break

##Key points

###The entire application is just a bunch of nested function calls.
What runs on the nodes and what runs on the basestation can be partitioned
at any function boundary.

###The complete list is never in memory
It "lazily" reads in only enough samples to get to the next *yield* statement.

##Future questions
-Can we express that application(s) we'd like to build in this manner
-What happens when the application is dynamic instead of statically calling
the same functions in the same order
