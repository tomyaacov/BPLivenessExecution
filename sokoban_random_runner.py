from sokoban import *
from sokoban_maps import maps
import sys

map_key = int(sys.argv[1])
map_value = maps[map_key]

pygame_settings["display"] = True
map_settings["map"] = map_value
bpr = init_bprogram()
bpr.run()


