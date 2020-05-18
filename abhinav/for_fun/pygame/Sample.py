import pygame
from pygame.locals import *
pygame.init()
#------------------Variables--------------------
w = 600
h = w
r = 4
clock = pygame.time.Clock()
fps = 120
#------------------Variables--------------------
win = pygame.display.set_mode((w,h))
while r <(300+300/3 + 300 * 0.14 )-5:
    pygame.draw.circle(win,(255,255,255),[int(w/2),int(h/2)],r)
    pygame.draw.circle(win,(255,0,0),[int(w/2),int(h/2)],r,4)
    pygame.display.update()
    r += 1
    clock.tick(fps)
