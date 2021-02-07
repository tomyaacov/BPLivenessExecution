import gym
import os
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import HER, DQN
from stable_baselines.her import GoalSelectionStrategy, HERGoalEnvWrapper
from stable_baselines.bench import Monitor
from sokoban import *



# Create log dir
log_dir = "/tmp/gym/"
os.makedirs(log_dir, exist_ok=True)

env = gym_goal_env_generator(episode_timeout=100)
#env = gym.make('CartPole-v1')
env = Monitor(env, log_dir)
model_class = DQN  # works also with SAC, DDPG and TD3
goal_selection_strategy = 'future' # equivalent to GoalSelectionStrategy.FUTURE
# model = DQN(MlpPolicy, 
#             env, 
#             verbose=1, 
#             exploration_fraction=0.7,
#             learning_rate=0.1)


model = HER('MlpPolicy', 
    env, 
    model_class, 
    n_sampled_goal=4, 
    goal_selection_strategy=goal_selection_strategy,
    verbose=1)
model.learn(total_timesteps=100000)
model.save("deepq_sokoban")
del model # remove to demonstrate saving and loading

model = DQN.load("deepq_sokoban")

pygame_settings["display"] = True
pygame.init()  # Prepare the PyGame module for use

obs = env.reset()
done = False
while not done:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    #env.render()

pygame.quit()
