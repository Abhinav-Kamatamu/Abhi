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
points = 0
clock = pygame.time.Clock()
#-----Variables-----

#-----Functions-----
def pointing(check = False):
    global cx
    if check:
        return 100
    if (w/2 >cx and cx >w/3) or( w/2<cx and cx<w/3):
        return(50)
    if (w/3 >cx and cx >w/4) or( w/3<cx and cx<w/4):
        return 10
    else:
        return 0
def click():
    global points, cx, y
    if play.collidepoint(cx,y):
        points+= pointing(True)
    else:
        points += pointing()
def in_loops():
    global run,mx,my
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click()
    show(points)
def show(points):
   pass 
#-----Functions-----
while run:
    win.fill((255,255,255))
    pygame.draw.rect(win,(255,0,0),(x,y,l,b))
    pygame.draw.line(win,(0,255,0),(w/2,y),(w/2,y+b),4)
    play = pygame.draw.circle(win,(0,0,0),(cx,cy),r,4)
    pygame.display.update()
    in_loops()
    clock.tick(fps)

