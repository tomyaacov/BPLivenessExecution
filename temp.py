import gym
import os
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy, FeedForwardPolicy
from stable_baselines import DQN
from stable_baselines.bench import Monitor
from lane_bridge import *

e = {
        "name": "dqn1",
        "n": 1,
        "double_q": False,
        "prioritized_replay": False,
        "total_timesteps": 10**5,
        "layers": [5]
    }

log_dir = "/tmp/"+ e["name"] +"/"
os.makedirs(log_dir, exist_ok=True)
b_program_settings["n_blue_cars"] = e["n"]
env = gym_env_generator(episode_timeout=30)
env = Monitor(env, log_dir)
policy_kwargs = dict(layers=e["layers"])
model = DQN("MlpPolicy", 
            env, 
            verbose=1, 
            exploration_fraction=0.9,
            exploration_final_eps=0,
            learning_rate=0.001,
            learning_starts=100,
            policy_kwargs = policy_kwargs,
            double_q = e["double_q"],
            prioritized_replay = e["prioritized_replay"])

                        
env = gym_env_generator(episode_timeout=100)
observation = env.reset()
print(observation)
observation = np.array(observation)
vectorized_env = model._is_vectorized_observation(observation, model.observation_space)
observation = observation.reshape((-1,) + model.observation_space.shape)
with model.sess.as_default():
    actions, a, b = model.step_model.step(observation, deterministic=True)
print(actions)
print(a)
print(b)
if not vectorized_env:
    actions = actions[0]
print(actions)