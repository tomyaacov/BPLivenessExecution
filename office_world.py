from bppy import *
import pygame
import time
from bp_env import BPEnv
from gym import spaces

must_finish = "must_finish"
state = "state"

pygame_settings = {
    "display": True
}

@b_thread
def player(i, j):
    while True:
        e = yield {request: [BEvent("Up", {"i": i-1, "j": j}),
                             BEvent("Down", {"i": i+1, "j": j}),
                             BEvent("Left", {"i": i, "j": j-1}),
                             BEvent("Right", {"i": i, "j": j+1})]}
        i, j = e.data["i"], e.data["j"]

    
@b_thread
def wall(i, j):
    yield {block: EventSet(lambda e: e.data == {"i": i, "j": j})}


@b_thread
def decoration(i, j):
    yield {block: EventSet(lambda e: e.data == {"i": i, "j": j})}


@b_thread
def take_coffee(i, j):
    while True:
        e = yield {waitFor: All(), must_finish: True}
        if i == e.data.get("i", -1) and j == e.data.get("j", -1):
            yield {request: BEvent("TAKE_COFFEE"), block: AllExcept(BEvent("TAKE_COFFEE")), must_finish: False}
            break


@b_thread
def bring_coffee_to_office(i, j):
    while True:
        yield {waitFor: BEvent("TAKE_COFFEE"), must_finish: True}
        e = yield {waitFor: All(), must_finish: True}
        if i == e.data.get("i", -1) and j == e.data.get("j", -1):
            e = yield {waitFor: All(), must_finish: False}
            break


@b_thread
def map_printer(map):
    stepped_on = None
    i, j = find(map, "A")[0]
    if pygame_settings["display"]:

        main_surface = pygame.display.set_mode((32 * len(map[0]), 32 * len(map)))
        count = 0
        while True:
            # Look for an event from keyboard, mouse, joystick, etc.
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break
            # Completely redraw the surface, starting with background
            main_surface.fill((255, 255, 255))
            for x in range(len(map)):
                for y in range(len(map[x])):
                    # Copy our image to the surface, at this (x,y) posn
                    main_surface.blit(map_dict[map[x][y]], (y * 32, x * 32))
            # Now that everything is drawn, put it on display!
            pygame.display.flip()
            time.sleep(1)
            #print(count)
            count += 1
            e = yield {waitFor: All()}
            i_new, j_new = e.data.get("i", i), e.data.get("j", j)
            if stepped_on is None:
                map[i] = map[i][:j] + " " + map[i][j+1:]
            else:
                map[i] = map[i][:j] + stepped_on + map[i][j+1:]
            if map[i_new][j_new] == " ":
                stepped_on = None
            else:
                stepped_on = map[i_new][j_new]
            map[i_new] = map[i_new][:j_new] + "A" + map[i_new][j_new+1:]
            i, j = i_new, j_new

    else:
        yield {waitFor: All()}


map_dict = {
    " ": pygame.transform.scale(pygame.image.load("office_world_pygame/floor.png"), (32,32)),
    "X": pygame.transform.scale(pygame.image.load("office_world_pygame/wall.png"), (32,32)),
    "n": pygame.transform.scale(pygame.image.load("office_world_pygame/decoration.png"), (32,32)),
    "A": pygame.transform.scale(pygame.image.load("office_world_pygame/player.png"), (32,32)),
    "o": pygame.transform.scale(pygame.image.load("office_world_pygame/office.png"), (32,32)),
    "m": pygame.transform.scale(pygame.image.load("office_world_pygame/mail.png"), (32,32)),
    "c": pygame.transform.scale(pygame.image.load("office_world_pygame/coffee.png"), (32,32))
}

def find(map, ch):
    return [(i, j) for i, row in enumerate(map) for j, c in enumerate(row) if c == ch]


if __name__ == "__main__":

    def init_bprogram():
        map = [
            "XXXXXXXXXXXXXXXXX",
            "X   X   X   X   X",
            "X     n   n     X",
            "X   Xc  X   X   X",
            "XX XXX XXX XXX XX",
            "X   X   X   X   X",
            "X n   o   m   n X",
            "X   X   X   X   X",
            "XX XXXXXXXXXXX XX",
            "X   X   X  cX   X",
            "X  A  n   n     X",
            "X   X   X   X   X",
            "XXXXXXXXXXXXXXXXX"
        ]
        map = [
            "XXXXXXXXXX",
            "X o      X",
            "X      n X",
            "X n    c X",
            "X    n   X",
            "XA       X",
            "XXXXXXXXXX"
        ]
        walls_list = find(map, "X")
        decoration_list = find(map, "n")
        player_locations = find(map, "A")
        coffee_locations = find(map, "c")
        player_location = player_locations[0]

        bthreads_list = [player(*player_location), map_printer(map)] + \
                        [wall(*l) for l in walls_list] + \
                        [decoration(*l) for l in decoration_list] + \
                        [take_coffee(*l) for l in coffee_locations]
        return BProgram(bthreads=bthreads_list, event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())

    bprog = init_bprogram()
    bprog.run()
