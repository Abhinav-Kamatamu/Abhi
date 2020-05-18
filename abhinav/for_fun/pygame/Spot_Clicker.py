import pygame
from pygame.locals import *
#-------Init--------
pygame.init()
#-------Init--------
#-----Variables-----
w = 600
h = 600
win = pygame.display.set_mode((w,h))
pygame.display.set_caption('HI Game')
x = int(0.1*w)
y = int(0.9*h)
cx = int(0.125*w)
cy = int(0.925*h)
r = 20
l = int(0.8*w)
b = int(0.05*h)
#-----Variables-----
while True:
    win.fill((255,255,255))
    pygame.draw.rect(win,(255,0,0),(x,y,l,b))
    pygame.draw.circle(win,(0,0,0),(cx,cy),r,1)
    pygame.display.update()

