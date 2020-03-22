import pygame,time
pygame.init()
from pygame.locals import *
win = pygame.display.set_mode((600,600))
h=0
x,y =0,0
w=0
win.fill((255,255,255))


while True:
    if h != 600 and h <600:
        pygame.draw.rect(win,(0,0,0),(600/2-h/2,600/2-w/2,w,h))
        pygame.display.update()
        h+=1
        w+=1
    if h > 600 or h == 600:
        
        _type_=pygame.font.Font('freesansbold.ttf',32)
        text=_type_.render('START',True,(255,255,255))
        textrect=text.get_rect()
        textrect.center=(600/2,600/2)
        win.blit(text,textrect)
        pygame.display.update()
        start = 0
        for event in pygame.event.get():
                    if event.type== MOUSEBUTTONDOWN:
                        x,y = event.pos
        if textrect.collidepoint(x,y):
            win.fill((255,255,255))
            fin = pygame.draw.rect(win,(0,0,0),(600/2,-1,601,601),1)
        