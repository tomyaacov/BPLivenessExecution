from lane_bridge import *

# pygame_settings["display"] = True
# env = gym_env_generator(episode_timeout=10)
# observation = env.reset()
# print(observation)
# reward_sum = 0
# while True:
#     # env.render()
#     action = env.action_space.sample()
#     # observation, reward, done, info = env.step(action)
#     observation, reward, done, info = env.step(1)
#     reward_sum += reward
#     print(action, observation, reward, done, info)
#     if done:
#         break
# print(reward_sum)
# env.close()


if __name__ == "__main__":
    #pygame_settings["display"] = True
    pygame.init()  
    env = gym_env_generator(episode_timeout=15)
    total_rewards = 0
    for i in range(1):
        observation = env.reset()
        print(observation)
        reward_sum = 0
        counter = 0
        while True:
            # env.render()
            observation, reward, done, info = env.step(env.replace_if_disabled(1))
            # if reward == 1:
            #     done = True
            reward_sum += reward
            counter += 1
            print(1, observation, reward, done, info)
            if done:
                break
        print(reward_sum)
        total_rewards += reward_sum
    print(1+(total_rewards/1000))
    env.close()
    pygame.quit()

