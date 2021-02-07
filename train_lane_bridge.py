import os
import sys
import matplotlib.pyplot as plt
from lane_bridge import *
from q_learning import *

env = BPEnv()
env.set_bprogram_generator(init_bprogram)

pygame_settings["display"] = False

Q, results, episodes, mean_reward = qlearning(environment=env,
                                              num_episodes=100000,
                                              episode_timeout=20,
                                              alpha=0.1,
                                              gamma=1,#0.99,
                                              testing=True,
                                              seed=1,
                                              glie=glie_10)
plt.plot(episodes, mean_reward)
plt.ylabel('mean reward')
plt.xlabel('episode')
plt.title(os.path.basename(sys.argv[0])[:-3])
plt.savefig(os.path.basename(sys.argv[0])[:-3] + ".pdf")

# event_runs = []
# reward_sum = 0
# for i in range(1000):
#     reward, event_run = run(env, Q, i, 100, True)
#     reward_sum += reward
# # print(Q)
# # print(event_runs)
# print(1+(reward_sum/1000))
# total_rewards = 0

print(Q)

import pickle
pickle_out = open("Q_lane_bridge.pickle", "wb")
pickle.dump(Q, pickle_out)
pickle_out.close()