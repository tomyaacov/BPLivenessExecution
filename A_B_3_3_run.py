from bppy import *
from q_learning import *
import matplotlib.pyplot as plt
from bp_env import BPEnv


must_finish = "must_finish"
state = "state"


def add_a():
    for i in range(3):
        yield {request: BEvent("A")}


def add_b():
    for i in range(3):
        yield {request: BEvent("B")}


def control():
    while True:
        yield {waitFor: BEvent("A")}
        yield {waitFor: BEvent("B"), block: BEvent("A")}



bprogram = BProgram(bthreads=[add_a(), add_b(), control()],
                              event_selection_strategy=SimpleEventSelectionStrategy(),
                              listener=PrintBProgramRunnerListener())
bprogram.run()


