from bppy import *
from q_learning import *
import matplotlib.pyplot as plt


must_finish = "must_finish"
state = "state"


def add_a():
    for i in range(10):
        yield {request: BEvent("A"), state: i, must_finish: True}


def add_b():
    for i in range(10):
        yield {request: BEvent("B"), state: i, must_finish: True}


def control():
    while True:
        yield {waitFor: BEvent("A"), state: 0, must_finish: False}
        yield {waitFor: BEvent("B"), block: BEvent("A"), state: 1, must_finish: False}


b_program = BProgram(bthreads=[add_a, add_b, control],
                     event_selection_strategy=SimpleEventSelectionStrategy(),
                     listener=PrintBProgramRunnerListener())
Q, results, episodes, mean_reward = qlearning(b_program, 100000, 0.1, 1.0, True, 5, glie_10)
plt.plot(episodes, mean_reward)
plt.ylabel('mean reward')
plt.xlabel('episode')
plt.title(os.path.basename(sys.argv[0])[:-3])
plt.savefig(os.path.basename(sys.argv[0])[:-3] + ".pdf")
event_runs = []
for i in range(100):
    reward, event_run = run(b_program, Q, i)
    if event_run not in event_runs:
        event_runs.append(event_run)
print(event_runs)
print(Q_test(b_program, Q, 1000, 2))
print(Q_test(b_program, {}, 1000, 2))
