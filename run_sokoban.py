import pickle
import pygame
from sokoban import *
from q_learning import *
from sokoban_maps import maps
import sys

map_key = int(sys.argv[1])
map_value = maps[map_key]

env = BPEnv()
env.set_bprogram_generator(init_bprogram)

pickle_in = open("models/Q_f_" + sys.argv[1] + ".pickle", "rb")
Q = pickle.load(pickle_in)
pickle_in.close()


pygame_settings["display"] = True
map_settings["map"] = map_value
pygame.init()  # Prepare the PyGame module for use
reward, event_run = run(env, Q, 2, 300, optimal=False)
pygame.quit()

