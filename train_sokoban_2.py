import os
import sys
import matplotlib.pyplot as plt
from bp_env import BPEnv
from sokoban import *
from q_learning import *
from sokoban_maps import maps2
import time
import sys
map_key = int(sys.argv[1])
map_value = maps2[map_key]
for j in range(20):
    start = time.time()
    env = BPEnv()
    env.set_bprogram_generator(init_bprogram)
    
    pygame_settings["display"] = False
    map_settings["map"] = map_value
    
    Q, results, episodes, mean_reward = qlearning(environment=env,
                                                  num_episodes=int(sys.argv[2]),
                                                  episode_timeout=100,
                                                  alpha=0.1,
                                                  gamma=0.99,
                                                  testing=True,
                                                  seed=1,
                                                  glie=glie_10)
    end = time.time()
    #plt.plot(episodes, mean_reward)
    #plt.ylabel('mean reward')
    #plt.xlabel('episode')
    #plt.title(os.path.basename(sys.argv[0])[:-3])
    #plt.savefig(os.path.basename(sys.argv[0])[:-3] + ".pdf")
    event_runs = []
    rewards_sum = 0
    for i in range(100):
        reward, event_run = run(env, Q, i, 100, True)
        if event_run not in event_runs:
            event_runs.append(event_run)
        rewards_sum += reward
        
    print(j, rewards_sum / 100, end - start)
