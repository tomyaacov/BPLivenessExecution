import gym
import os
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN
from stable_baselines.bench import Monitor
from lane_bridge import *



# Create log dir
log_dir = "/tmp/gym/"
os.makedirs(log_dir, exist_ok=True)

env = gym_env_generator(episode_timeout=30)
#env = gym.make('CartPole-v1')
env = Monitor(env, log_dir)
policy_kwargs = dict(layers=[5])
model = DQN("MlpPolicy", 
            env, 
            verbose=1, 
            exploration_fraction=0.9,
            exploration_final_eps=0,
            learning_rate=0.001,
            learning_starts=100,
            policy_kwargs = policy_kwargs)
model.learn(total_timesteps=150000)
model.save("deepq_lane_bridge")

del model # remove to demonstrate saving and loading

model = DQN.load("deepq_lane_bridge")

# pygame_settings["display"] = True
# pygame.init()  # Prepare the PyGame module for use

# obs = env.reset()
# done = False
# rewards_sum = 0
# while not done:
#     action, _states = model.predict(obs)
#     obs, rewards, done, info = env.step(action)
#     rewards_sum += rewards
#     #env.render()
# print(rewards_sum)
# pygame.quit()

total_rewards = 0
for i in range(1000):
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
    print(reward_sum)
    total_rewards += reward_sum
print(1+(total_rewards/1000))
env.close()
pygame.quit()