import pickle
import pygame
from sokoban import *
from q_learning import *

env = BPEnv()
env.set_bprogram_generator(init_bprogram)

pickle_in = open("models/Q_f_1.pickle", "rb")
Q = pickle.load(pickle_in)
pickle_in.close()

pygame_settings["display"] = True
map_settings["map"] = [
    "XXXXXXXX",
    "X   XXXX",
    "X   X  X",
    "XX     X",
    "XX XXXtX",
    "X bXXXXX",
    "Xa XXXXX",
    "XXXXXXXX",
]
pygame.init()  # Prepare the PyGame module for use
reward, event_run = run(env, Q, 2, 300, optimal=False)
pygame.quit()

# Q_f_1
# map = [
#     "XXXXXXXX",
#     "X   XXXX",
#     "X   X  X",
#     "XX     X",
#     "XX XXXtX",
#     "X bXXXXX",
#     "Xa XXXXX",
#     "XXXXXXXX",
# ]
# Q_f_2
# map = [
#     "XXXXXXXX",
#     "X     aX",
#     "Xt  b  X",
#     "X  tb  X",
#     "XXX X  X",
#     "XXXXXXXX",
#     "XXXXXXXX",
#     "XXXXXXXX",
# ]
# Q_f_3
# map = [
    # "XXXXXXXX",
    # "X XXX aX",
    # "X t X  X",
    # "X btb  X",
    # "X  b  tX",
    # "XX     X",
    # "XX     X",
    # "XXXXXXXX",
# ]