import pygame,random
from time import sleep
from pygame.locals import *
#----------
pygame.init()
FPS = 1
FPSclock = pygame.time.Clock()
#----------
mouseClick = False
#----variables----
win=pygame.display.set_mode((700,700))
win.fill((255,255,255))
bal=pygame.image.load('bal.png')
ball=pygame.image.load('ball.jpeg')
bal=pygame.transform.scale(bal,(50,100))
ball=pygame.transform.scale(ball,(50,100))
pygame.display.update()
mousex = 0
mousey = 0
ranumx,ranumy = 0,0
balpop= False
no_on_screen=0
p_x=0
p_y=0
my = pygame.draw.rect(win,(255,0,0),(-100,-100,1,1))
class Balloon():
    def draw(img):
        global bal
        global balrect
        global no_on_screen
        global ranumy
        global ranumx
        global my
        ranumx=random.randint(0,650)
        ranumy=random.randint(0,600)
        my=pygame.draw.rect(win,(0,0,0),(ranumx,ranumy,50,100))
        pygame.display.update()
        no_on_screen+=1
        ranumy+=5

        
    def pop():
        global mousex
        global mousey
        global mouseClick
        global my
        global no_on_screen
        if mouseClick == True:
            if my.collidepoint(mousex,mousey):
                curentballx=my.left
                curentbally=my.top
                win.fill((255,255,255))
                font=pygame.font.Font('freesansbold.ttf',32)
                text=font.render("pop",True,(255,0,0))
                text=text.get_rect()
                win.blit(text,(curentballx,curentbally))
                pygame.display.update()
                

b1=Balloon()
b2=Balloon()

while True:
    b1.pop
    b2.pop
    b1.draw()
    b2.draw()
    if my.collidepoint(mousex,mousey):
        b1.draw()
        b2.draw()
    balrect=bal.get_rect()
    win.fill((255,255,255))
    for i in pygame.event.get():
        if i.type == QUIT:
            pygame.quit()
            exit()
        if i.type==MOUSEBUTTONDOWN:
            mousex,mousey=i.pos
            mouseClick = True
    mousex=int(mousex)
    mousey=int(mousey)
    my.left=ranumx
    my.top=ranumy
    balrect=bal.get_rect()
    if mouseClick == True:
        if balrect.collidepoint(mousex,mousey):
            win.fill((255,255,255))
            win.blit(ball,(ranumx,ranumy))
            pygame.display.update()
            sleep(3)
            pygame.quit()
            exit()

    FPSclock.tick(FPS)