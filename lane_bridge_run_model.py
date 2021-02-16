import gym
import os
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN
from stable_baselines.bench import Monitor
from lane_bridge import *

def evaluate_model(model):
    total_rewards = 0
    for i in range(5):
        observation = env.reset()
        reward_sum = 0
        counter = 0
        while True:
            # env.render()
            action, _states = model.predict(observation)
            observation, reward, done, info = env.step(action)
            reward_sum += reward
            counter += 1
            #print(action, observation, reward, done, info)
            if done:
                break
        total_rewards += reward_sum
    print(1+(total_rewards/5))

b_program_settings["n_blue_cars"] = 3
env = gym_env_generator(episode_timeout=100)
pygame_settings["display"] = True
model = DQN.load("ddqn3")
evaluate_model(model)