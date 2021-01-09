import pygame
from pygame.locals import *

win = pygame.display.set_mode((600, 600))

x = 30
y = 30

while True:
    win.fill((255, 255, 255))
    pygame.draw.rect(win, (255, 255, 0), [x, y, 30, 30])
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        exit()
    pygame.display.update()