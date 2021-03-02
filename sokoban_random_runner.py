from sokoban import *

pygame_settings["display"] = True
map_settings["map"] = [
    "XXXXXXXX",
    "X XXX aX",
    "X t X  X",
    "X btb  X",
    "X  b  tX",
    "XX     X",
    "XX     X",
    "XXXXXXXX",
]
bpr = init_bprogram()
bpr.run()
# env = gym_env_generator(episode_timeout=30)
# observation = env.reset()
# reward_sum = 0
# while True:
#     # env.render()
#     action = env.action_space.sample()
#     observation, reward, done, info = env.step(action)
#     reward_sum += reward
#     print(action, observation, reward, done, info)
#     #print(reward, env.compute_reward(observation["achieved_goal"], observation["desired_goal"], None))
#     if done:
#         break
# print(reward_sum)
# env.close()

