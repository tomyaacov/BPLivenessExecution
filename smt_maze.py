import sys
import pygame
import time
sys.path.extend(['/Users/tomyaacov/Desktop/university/thesis/BPpy'])
from model.bprogram import BProgram
from model.event_selection.smt_event_selection_strategy import SMTEventSelectionStrategy
from utils.z3helper import *
from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener


HEIGHT = 500
WIDTH = 500

# move_west_south = Bool('move_west_south')
# x = RealVector('x')
# y = RealVector('y')
#
#
# def walls():
#     yield {'block': Or(x < 0, x > WIDTH, y < 0, y > HEIGHT), 'wait-for': false}
#
#


done = False
pygame.init()
frame_edge_width = 10
screen = pygame.display.set_mode((WIDTH + frame_edge_width * 2, HEIGHT + frame_edge_width * 2))
clock = pygame.time.Clock()
for i in range(200):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (250, 250, 250), pygame.Rect(frame_edge_width, frame_edge_width, WIDTH, HEIGHT))
    x = i
    y = i
    pygame.draw.circle(screen, (255, 100, 0), (x + frame_edge_width, y + frame_edge_width), 5)
    pygame.display.flip()
    clock.tick(60)

# import pygame
#
# pygame.init()
# screen = pygame.display.set_mode((400, 300))
# done = False
# is_blue = True
# x = 30
# y = 30
#
# while not done:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#             is_blue = not is_blue
#
#     pressed = pygame.key.get_pressed()
#     if pressed[pygame.K_UP]: y -= 3
#     if pressed[pygame.K_DOWN]: y += 3
#     if pressed[pygame.K_LEFT]: x -= 3
#     if pressed[pygame.K_RIGHT]: x += 3
#
#     if is_blue:
#         color = (0, 128, 255)
#     else:
#         color = (255, 100, 0)
#     pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
#
#     pygame.display.flip()