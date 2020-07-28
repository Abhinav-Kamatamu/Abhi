import random as r
import pygame

pygame.init()

w = 500
h = 500
y = 0
x = r.randint(0, w)
win = pygame.display.set_mode((w, h))
win.fill((255, 255, 255))
pygame.display.update()
while True:
    ob = pygame.draw.circle(win, (0, 0, 0), (x, y), 4)
    y += 1
    if y > h:
        y = 0
        x = r.randint(0, w)
    pygame.display.update()
    win.fill((255, 255, 255))
