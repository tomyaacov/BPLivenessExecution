from bppy import *
import pygame
import time
import random
from bp_env import BPEnv
from gym import spaces
import numpy as np

must_finish = "must_finish"
state = "state"
pygame_settings = {
    "display": False
}

b_program_settings = {
    "n_blue_cars": 1
}

blue_cars_locations = [2.5, 4, 5]
red_cars_locations = [0]

def advance_red_car(i, e):
    if e.name == "Move":
        red_cars_locations[i] = (red_cars_locations[i]+1)%5

def any_blue_on_bridge():
    return any([2 <= x <= 3 for x in blue_cars_locations])

def any_red_on_bridge():
    return any([2 <= x <= 3 for x in red_cars_locations])

def advance_blue_cars():
    global blue_cars_locations
    if any_red_on_bridge():
        for i in range(len(blue_cars_locations)):
            if blue_cars_locations[i] <= 2 or blue_cars_locations[i] >= 3:
                suggested = blue_cars_locations[i] - 0.5
                if abs(suggested - blue_cars_locations[i-1]) >= 0.5:
                    blue_cars_locations[i] = suggested
    else:
        blue_cars_locations = [x-0.5 for x in blue_cars_locations]
    for i in range(len(blue_cars_locations)):
        if blue_cars_locations[i] <= 0:
            blue_cars_locations[i] = 5 + blue_cars_locations[i]

def attempting_to_cross(i):
    return red_cars_locations[i] == 1 or red_cars_locations[i] == 2

def red_passed():
    return red_cars_locations[i] = 4

@b_thread
def red_car():
    e = yield {request: [BEvent("Wait"), BEvent("Move")]}
    advance_red_car(e)

@b_thread
def red_pass_bridge_infinitly_often():
    while True:
        while not red_passed():
            yield {waitFor: All(), must_finish: True}
        yield {waitFor: All()}

@b_thread
def blue_cars():
    while True:
        blue_state = "_".join([str(x) for x in blue_cars_locations])
        yield {waitFor: All(), state: blue_state}
        advance_blue_cars()

@b_thread
def blue_car(i):
    sample_blue_car_location(i)
    while True:
        yield {waitFor: All()}
        advance_blue_car(i)

@b_thread
def control_red_crossing():
    while True:
        if any_blue_on_bridge() and attempting_to_cross():
            yield {block: BEvent("Move"), waitFor: All()}
        else:
            yield {waitFor: All()}


@b_thread
def road_printer():
    if pygame_settings["display"]:
        scale = 100
        main_surface = pygame.display.set_mode((scale * 6, scale * 2))
        background_image = pygame.transform.scale(pygame.image.load("lane_bridge_pygame/road.jpeg"), (scale * 6, scale * 2))
        red_image = pygame.transform.scale(pygame.image.load("lane_bridge_pygame/red.png"), (50,30))
        blue_image = pygame.transform.scale(pygame.image.load("lane_bridge_pygame/blue.png"), (50,30))
        blue_height = 1.4
        bridge_height = 1
        red_height = 0.6
        count = 0
        while True:
            # Look for an event from keyboard, mouse, joystick, etc.
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break
            # Completely redraw the surface, starting with background
            main_surface.blit(background_image, [0, 0])
            for i in blue_cars_locations:
                if 2 <= i <= 3:
                    main_surface.blit(blue_image, ((i+0.3) * scale, bridge_height * scale))
                else:
                    main_surface.blit(blue_image, ((i+0.3)  * scale, blue_height * scale))
            for i in red_cars_locations:
                if 2 <= i <= 3:
                    main_surface.blit(red_image, ((i+0.3)  * scale, bridge_height * scale))
                else:
                    main_surface.blit(red_image, ((i+0.3)  * scale, red_height * scale))
           # Now that everything is drawn, put it on display!
            pygame.display.flip()
            time.sleep(0.5)
            count += 1
            e = yield {waitFor: All()}
    else:
        yield {waitFor: All()}


def get_random_locations(n):
    final = []
    l_bound = 0.5
    r_bound = 5 - (0.5)*n
    while len(final) < n:
        p = round(random.uniform(l_bound, r_bound),1)
        final.append(p)
        l_bound = p + 0.5
        r_bound = r_bound + 0.5
    return final
        

def shuffle_locations(n):
    global blue_cars_locations, red_cars_locations
    red_cars_locations = [random.choice([0])]
    #blue_cars_locations = random.sample([0.5,1,1.5,2,2.5,3,3.5,4,4.5,5], n)
    blue_cars_locations = get_random_locations(n)
    #red_cars_locations = [1]
    #blue_cars_locations = [3.5]
    #print(blue_cars_locations)
    #blue_cars_locations.sort()

def init_bprogram():
    n = b_program_settings["n_blue_cars"]
    shuffle_locations(n)
    bthreads_list = [red_car(0), red_pass_bridge_infinitly_often(0), control_red_crossing(0), road_printer(), blue_cars()]
    return BProgram(bthreads=bthreads_list, event_selection_strategy=SimpleEventSelectionStrategy())

def gym_env_generator(episode_timeout):
    _ = init_bprogram()
    env = BPEnv()
    env.set_bprogram_generator(init_bprogram)
    action_mapper = {0: "Wait", 1: "Move"}
    env.action_mapper = action_mapper
    env.action_space = spaces.Discrete(action_mapper.__len__())
    input_shape = (b_program_settings["n_blue_cars"]+2,)
    env.observation_space = spaces.Box(low=0, high=5, shape=input_shape, dtype=np.float32)
    env.episode_timeout = episode_timeout
    return env

# pygame_settings["display"] = True
# bprogram = init_bprogram()
# bprogram.run()
