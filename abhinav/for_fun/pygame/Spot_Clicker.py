import pygame
from pygame.locals import *
#-------Init--------
pygame.init()
#-------Init--------

#-----Variables-----
w = 600
h = w
fps = 30
win = pygame.display.set_mode((w,h))
pygame.display.set_caption('Clicker')
x = int(0.1*w)
y = int(0.9*h)
cx = int(0.125*w)
cy = int(0.925*h)
r = int(1/30*w)
l = int(0.8*w)
b = int(0.05*h)
run = True
mx,my = 0,0
points = 0
clock = pygame.time.Clock()
#-----Variables-----

#-----Functions-----
def pointing():
    global mx,my
    pass
def click(x,y):
    global points
    play.collidepoint(x,y)
    points = pointing()
def in_loops():
    global run,mx,my
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = event.pos
            click(mx,my)
#-----Functions-----
while run:
    win.fill((255,255,255))
    pygame.draw.rect(win,(255,0,0),(x,y,l,b))
    pygame.draw.circle(win,(0,0,0),(cx,cy),r,4)
    pygame.display.update()
    in_loops()
    clock.tick(fps)

