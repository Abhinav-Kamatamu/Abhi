import pygame
from pygame.locals import *

pygame.init()

width = 500
height = width

white = (255, 255, 255)
win = pygame.display.set_mode((width, height))

win.fill(white)
pygame.display.update()

s = 50
pygame.draw.rect(win, (255, 0, 0), (225, 225, s, s))
pygame.display.update()

while True:
    s += 1
    pygame.draw.rect(win, (255, 0, 0), (225, 225, s, s))
    pygame.display.update()
