import pickle
import pygame
from sokoban import *
from q_learning import *

env = BPEnv()
env.set_bprogram_generator(init_bprogram)

pickle_in = open("Q_b.pickle", "rb")
Q = pickle.load(pickle_in)
pickle_in.close()

pygame_settings["display"] = True
pygame.init()  # Prepare the PyGame module for use
reward, event_run = run(env, Q, 2, 100, True)
pygame.quit()