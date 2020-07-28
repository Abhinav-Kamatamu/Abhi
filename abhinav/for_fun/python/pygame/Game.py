import random as r
import pygame
from pygame.locals import *

pygame.init()

w = 500
h = 500
y = 0
fps = 90
clock = pygame.time.Clock()
x = r.randint(0, w)
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Abhinav\'s PROGRAM')
win.fill((255, 255, 255))
pygame.display.update()


def escape():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        exit()


while True:
    ob = pygame.draw.circle(win, (0, 0, 0), (x, y), 4)
    y += 1
    if y > h:
        y = 0
        x = r.randint(0, w)
    pygame.display.update()
    win.fill((255, 255, 255))
    escape()
    clock.tick(fps)
