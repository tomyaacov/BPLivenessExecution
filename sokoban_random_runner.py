from sokoban import *

pygame_settings["display"] = True
env = gym_goal_env_generator(episode_timeout=10)
observation = env.reset()
reward_sum = 0
while True:
    # env.render()
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    reward_sum += reward
    #print(action, observation, reward, done, info)
    print(reward, env.compute_reward(observation["achieved_goal"], observation["desired_goal"], None))
    if done:
        break
print(reward_sum)
env.close()

