from sokoban import gym_env_generator


display = True
from bp_env import BPEnv
import random
from gym import spaces


env = gym_env_generator(episode_timeout=20)
observation = env.reset()
reward_sum = 0
while True:
    # env.render()
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    reward_sum += reward
    print(action, observation, reward, done, info)
    if done:
        break
print(reward_sum)
env.close()