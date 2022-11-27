from bppy import *
from dfs_bprogram import DFSBProgram
from value_iteration import q_value_iteration
from q_learning import Q_test
from bp_env import BPEnv


must_finish = "must_finish"
state = "state"


def add_a():
    for i in range(3):
        yield {request: BEvent("A"), state: i, must_finish: i!=0}


def add_b():
    for i in range(3):
        yield {request: BEvent("B"), state: i, must_finish: i!=0}



def control():
    while True:
        yield {waitFor: BEvent("A"), state: 0, must_finish: False}
        yield {waitFor: BEvent("B"), block: BEvent("A"), state: 1, must_finish: False}


def init_bprogram():
    return BProgram(bthreads=[add_a(), add_b(), control()],
                    event_selection_strategy=SimpleEventSelectionStrategy(),
                    listener=PrintBProgramRunnerListener())


if __name__ == "__main__":
    dfs = DFSBProgram(init_bprogram)
    init, states = dfs.run()
    DFSBProgram.save_graph(init, states, "graph.dot")
    Q = q_value_iteration(states, 1, 0.01)
    print("Q values:")
    for s in Q:
        print(s)
        for a in Q[s]:
            print(a.name, ":", Q[s][a], end=", ")
        print("")
    env = BPEnv()
    env.set_bprogram_generator(init_bprogram)
    Q_test(env, Q, 100, 4, 100, optimal=True)