import os
import sys
import matplotlib.pyplot as plt
from bp_env import BPEnv
from sokoban import *
from q_learning import *

env = BPEnv()
env.set_bprogram_generator(init_bprogram)

pygame_settings["display"] = False

Q, results, episodes, mean_reward = qlearning(environment=env,
                                              num_episodes=10000,
                                              episode_timeout=300,
                                              alpha=0.1,
                                              gamma=0.99,
                                              testing=True,
                                              seed=1,
                                              glie=glie_10)
plt.plot(episodes, mean_reward)
plt.ylabel('mean reward')
plt.xlabel('episode')
plt.title(os.path.basename(sys.argv[0])[:-3])
plt.savefig(os.path.basename(sys.argv[0])[:-3] + ".pdf")
event_runs = []
for i in range(100):
    reward, event_run = run(env, Q, i, 100, True)
    if event_run not in event_runs:
        event_runs.append(event_run)
print(event_runs)
import pickle
pickle_out = open("Q_b.pickle", "wb")
pickle.dump(Q, pickle_out)
pickle_out.close()