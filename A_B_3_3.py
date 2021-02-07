from bppy import *
from q_learning import *
import matplotlib.pyplot as plt
from bp_env import BPEnv


must_finish = "must_finish"
state = "state"


def add_a():
    for i in range(3):
        yield {request: BEvent("A"), state: i, must_finish: True}


def add_b():
    for i in range(3):
        yield {request: BEvent("B"), state: i, must_finish: True}


def control():
    while True:
        yield {waitFor: BEvent("A"), state: 0, must_finish: False}
        yield {waitFor: All(), block: BEvent("A"), state: 1, must_finish: False}


def init_bprogram():
    return BProgram(bthreads=[add_a(), add_b(), control()],
                    event_selection_strategy=SimpleEventSelectionStrategy(),
                    listener=PrintBProgramRunnerListener())


env = BPEnv()
env.set_bprogram_generator(init_bprogram)
Q, results, episodes, mean_reward = qlearning(env, 1000, 0.1, 0.99, True, 5, glie_10)
plt.plot(episodes, mean_reward)
plt.ylabel('mean reward')
plt.xlabel('episode')
plt.title(os.path.basename(sys.argv[0])[:-3])
plt.savefig(os.path.basename(sys.argv[0])[:-3] + ".pdf")
event_runs = []
for i in range(100):
    reward, event_run = run(env, Q, i, 100)
    if event_run not in event_runs:
        event_runs.append(event_run)
print(event_runs)
Q_test(env, Q, 1000, 2, 100)
