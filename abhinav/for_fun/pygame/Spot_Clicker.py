import pygame
from pygame.locals import *
#-------Init--------
pygame.init()
#-------Init--------

#-----Variables-----
w = 600
h = 600
fps = 30
win = pygame.display.set_mode((w,h))
pygame.display.set_caption('Clicker')
x = int(0.1*w)
y = int(0.9*h)
cx = int(0.125*w)
cy = int(0.925*h)
r = 20
l = int(0.8*w)
b = int(0.05*h)
run = True
clock = pygame.time.Clock()
#-----Variables-----

#-----Functions-----
def click(x,y):
    play.collidepoint(x,y)
def in_loops():
    global run
    for event in pygame.events.get():
        if evet.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = event.pos()
#-----Functions-----
while run:
    win.fill((255,255,255))
    pygame.draw.rect(win,(255,0,0),(x,y,l,b))
    pygame.draw.circle(win,(0,0,0),(cx,cy),r,1)
    pygame.display.update()
    clock.tick(fps)

