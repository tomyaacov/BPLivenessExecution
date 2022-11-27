from bppy import *

Approaching = lambda i: BEvent("Approaching", {"i":i})
Entering = lambda i: BEvent("Entering", {"i":i})
Leaving = lambda i: BEvent("Leaving", {"i":i})
Lower = BEvent("Lower")
Raise = BEvent("Raise")
Any_Approaching = EventSet(lambda e: e.name == "Approaching")

def r1(i): # train approaching, entering, and then leaving
    while True:
        yield {request: Approaching(i)}
        yield {request: Entering(i)}
        yield {request: Leaving(i)}

def r2(): # The barriers are lowered when a train is approaching and then raised as soon as possible.
    while True:
        yield {waitFor: Any_Approaching}
        yield {request: Lower}
        yield {request: Raise}

def r3(i): # A train may not enter while barriers are up.
    while True:
        yield {waitFor: Lower, block: Entering(i)}
        yield {waitFor: Raise}

def r4(i): # The barriers may not be raised while a train is in the intersection zone.
    while True:
        yield {waitFor: Approaching(i)}
        yield {waitFor: Leaving(i), block: Raise}

n = 2
bthreads_list = [r1(i) for i in range(n)] + [r3(i) for i in range(n)] + [r4(i) for i in range(n)] + [r2()]
bprog = BProgram(bthreads=bthreads_list, event_selection_strategy=SimpleEventSelectionStrategy(), listener=PrintBProgramRunnerListener())
bprog.run()