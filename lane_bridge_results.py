import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean
import pandas as pd
import os
FOLDER_NAME = "/Users/tomyaacov/Downloads/13_2_9_40"

experiments = {
    "1_CAR": {"DQN": "dqn1", "DDQN": "ddqn1", "PER": "per1"},
    "2_CAR": {"DQN": "dqn2", "DDQN": "ddqn2", "PER": "per2"},
    "3_CAR": {"DQN": "dqn3", "DDQN": "ddqn3", "PER": "per3"},
    "4_CAR": {"DQN": "dqn4", "DDQN": "ddqn4", "PER": "per4"}
}

def get_rewards(file):
    rewards = []
    with open(file) as f:
        for l in f.readlines()[2:]:
            rewards.append(float(l.split(",")[0]))
    final = []
    for i in range(1000, len(rewards), 1):
        final.append(mean(rewards[i-1000:i]))
    return final

for k1,v1 in experiments.items():
    for k2,v2 in v1.items():
        df = pd.read_csv(os.path.join(FOLDER_NAME, v2, "monitor.csv"))
        plt.plot(get_rewards(os.path.join(FOLDER_NAME, v2, "monitor.csv")), label=k2)
    plt.ylabel('mean reward')
    plt.xlabel('episode')
    plt.legend()
    plt.title(k1)
    plt.savefig(k1 + ".pdf")
    plt.close()