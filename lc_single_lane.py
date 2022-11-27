from bppy import *
from q_learning import *
import matplotlib.pyplot as plt
from bp_env import BPEnv

must_finish = "must_finish"
state = "state"

Approaching = lambda track, direction: BEvent("Approaching", {"track": track, "direction": direction})
Entering = lambda track, direction: BEvent("Entering", {"track": track, "direction": direction})
Leaving = lambda track, direction: BEvent("Leaving", {"track": track, "direction": direction})
Lower = BEvent("Lower")
Raise = BEvent("Raise")
Any_Approaching = EventSet(lambda e: e.name == "Approaching")

@b_thread
def r1(i, d):
    """trains keep approaching, entering, and then leaving
    in each track and in both directions."""
    while True:
        yield {request: Approaching(i, d), must_finish: True, state: 0}
        yield {request: Entering(i, d), must_finish: True, state: 1}
        yield {request: Leaving(i, d), state: 2}



def r2():
    """The barriers are lowered when a train is approaching
    and then raised as soon as possible."""
    while True:
        yield {waitFor: Any_Approaching, state: 0}
        yield {request: Lower, state: 1}
        yield {request: Raise, state: 2}

def r3(i, d):
    """A train may not enter while barriers are up."""
    while True:
        yield {waitFor: Lower, block: Entering(i, d), state: 0}
        yield {waitFor: Raise, state: 1}

def r4(i, d):
    """The barriers may not be raised while a train is in the intersection zone."""
    while True:
        yield {waitFor: Approaching(i, d), state: 0}
        yield {waitFor: Leaving(i, d), block: Raise, state: 1}

@b_thread
def r5(i, d):
    """A train may not enter while a train is passing from the opposite direction"""
    while True:
        yield {waitFor: Approaching(i, d), state: 0}
        yield {waitFor: Leaving(i, d), block: Entering(i, not d), state: 1}



def init_bprogram():
    n = 1
    bthreads_list = [r1(i, True) for i in range(n)] + [r3(i, True) for i in range(n)] + \
                    [r4(i, True) for i in range(n)] + [r5(i, True) for i in range(n)] + \
                    [r1(i, False) for i in range(n)] + [r3(i, False) for i in range(n)] + \
                    [r4(i, False) for i in range(n)] + [r5(i, False) for i in range(n)] + \
                    [r2()]
    return BProgram(bthreads=bthreads_list,
                    event_selection_strategy=SimpleEventSelectionStrategy(),
                    listener=PrintBProgramRunnerListener())

env = BPEnv()
env.set_bprogram_generator(init_bprogram)
Q, results, episodes, mean_reward = qlearning(env, 300000, 0.1, 0.99, True, 5, glie_10, 100)
plt.plot(episodes, mean_reward)
plt.ylabel('mean reward')
plt.xlabel('episode')
plt.title(os.path.basename(sys.argv[0])[:-3])
plt.savefig(os.path.basename(sys.argv[0])[:-3] + ".pdf")
Q_test(env, Q, 1000, 2, 50)







