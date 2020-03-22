import pygame,sys
from time import sleep
pygame.init()
from pygame.locals import *
j = 0
w=1280
h=700
x=20
y=20
posx=x
posy=y
vel=1
black=(0,0,0)
fps = 60
clock = pygame.time.Clock()
DISPLAYSURF=pygame.display.set_mode((w,h))
DISPLAYSURF.fill(black)
while True:
    lx=[]
    ly=[]
    lx.append(x)
    if j == 0:
        my = pygame.draw.rect(DISPLAYSURF,(255,255,255),(posx,posy,x,y))
    else:
        my = pygame.draw.rect(DISPLAYSURF,(black),(posx,posy,x,y))
        
    pygame.time.delay(100)
    for i in pygame.event.get():
        if i.type== QUIT:
            _type_=pygame.font.Font('freesansbold.ttf',32)
            text=_type_.render('This program was writen by Abhinav with the help of Gopal Krishna',True,(255,255,255))
            textrect=text.get_rect()
            textrect.center=(w/2,h/2)
            DISPLAYSURF.fill(black)
            DISPLAYSURF.blit(text,textrect)
            pygame.display.update()
            sleep(2)
            pygame.quit()
            sys.exit()
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT] :
        posx-=vel
        if posx == 0:
            posx = w
    if keys[pygame.K_RIGHT] :
        posx+=vel
        if posx == w-x:
            posx = -x
    if keys[pygame.K_UP]:
        posy-=vel
        if posy == 0:
            posy = h
    if keys[pygame.K_DOWN]:
        posy+=vel
        if posy == h-y:
            posy = -y
    if keys[pygame.K_u]:
        j = 1
        pygame.display.update()
    if keys[pygame.K_d]:
        j = 0
    if keys[pygame.K_c]:
        posx=x
        posy=y
        j=0
        DISPLAYSURF.fill(black)
        pygame.display.update()
    pygame.display.update()
    clock.tick(fps)