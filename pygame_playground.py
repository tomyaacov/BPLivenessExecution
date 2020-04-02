# import pygame
# import time
#
#
# WIDTH = 1000
# HEIGHT = 1000
# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
#
# clock = pygame.time.Clock()
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             break
#
#     screen.fill((250, 250, 250))
#
#     for i in range(10):
#         pygame.draw.rect(screen, (50, 100, 0),
#                          pygame.Rect(5 + i * 100, 5 + i * 100, 5, 5))
#         pygame.draw.rect(screen, (0, 50, 255),
#                         pygame.Rect(11.25 + 0.7 * HEIGHT, 11.25 + 0.7 * WIDTH, 10, 10))
#         pygame.display.flip()
#         pygame.time.wait(1000)
#         clock.tick(1000)
#
#
#     break


import sys
import os
file_name =  os.path.basename(sys.argv[0])
print(file_name[:-3])