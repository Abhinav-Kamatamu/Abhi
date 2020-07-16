import pygame
from pygame.locals import *
#-----variables-----#
h = 600
w = h
win = pygame.display.set_mode((w,h))
x,y = w/2 , h/2
r = 1
col = 0
pa = 0
#-----variables-----#
def draw(x,y):
    global px,py
    inx = int(x)
    iny = int(y)
    if col == 1:
        pygame.draw.rect(win,(0,0,255),(inx,iny,r,r))
        if pa == 'mo':
            pygame.draw.line(win,(0,0,255),(px,py),(x,y),r*2)
    if col == 2:
        pygame.draw.rect(win,(255,0,0),(inx,iny,r,r))
        if pa == 'mo':
            pygame.draw.line(win,(255,0,0),(px,py),(x,y),r*2)
    if col == 0:
        pygame.draw.rect(win,(255,255,255),(inx,iny,r,r))
        if pa == 'mo':
            pygame.draw.line(win,(255,255,255),(px,py),(x,y),r*2)
    if col == 3:
        pygame.draw.rect(win,(0,255,0),(inx,iny,r,r))
        if pa == 'mo':
            pygame.draw.line(win,(0,255,0),(px,py),(x,y),r*2)
    pygame.display.update()
    
while True:
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            px,py=x,y
            x,y = event.pos
            pa = 'mo'
        if event.type== QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_1:
                col = 1
            if event.key == K_2:
                col = 2
            if event.key == K_c:
                win.fill((0,0,0))
            if event.key == K_0:
                col = 0
            if event.key == K_3:
                col = 3
            if event.key == K_w:
                x = x+1
                pa = 0
            if event.key == K_a:
                y=y-1
                pa = 0
            if event.key == K_s:
                x=x-1
                pa = 0
            if event.key == K_d:
                y =y+ 1
                pa = 0
    draw(x,y)