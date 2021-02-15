from lane_bridge import *

#pygame_settings["display"] = True
#pygame.init()  
b_program_settings["n_blue_cars"] = 4
env = gym_env_generator(episode_timeout=30)

total_rewards = 0
for i in range(10000):
    observation = env.reset()
    reward_sum = 0
    counter = 0
    while True:
        # env.render()
        observation, reward, done, info = env.step(env.replace_if_disabled(random.choice([0,1])))
        reward_sum += reward
        counter += 1
        #print(action, observation, reward, done, info)
        if done:
            break
    total_rewards += reward_sum
print(1+(total_rewards/10000))
env.close()
#pygame.quit()
#0.67790.54620.424
