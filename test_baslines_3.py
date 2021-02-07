from stable_baselines.common.env_checker import check_env
from lane_bridge import *
env = gym_env_generator(100)
check_env(env, warn=True, skip_render_check=True)