import pygame, random, time
from pygame.locals import *
pygame.init()

#--variables--
clock = pygame.time.Clock()
w = int(input('Set screen size(500, 600, 700) prefered size is 500 :- '))
fps = w//10
h = w
win = pygame.display.set_mode((w,h))
pygame.display.set_caption('Abhinav made this Game')
x = w//2-(w//10/2)
y = h+10-(h//10/2)-h//10
s = w//10
speed = w//200 + 4
score = 0
checker = False
#----Block----
T = [pygame.time.get_ticks() for i in range(5)]
Bs = w//9
Bx = [random.randint(0, w - Bs) for _ in range(5)]
By = [-Bs for _ in range(5)]
S = [None for _ in range(5)]
C = [random.randint(1,15) for _ in range(5)]
#----Block----
#--variables--

def draw():
    global win, x, y,s, player, speed
    player = pygame.draw.rect(win,(255,0,0),(x,y,s,s))
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if x<= 0:
            pass
        else:
            x -= speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if x +Bs >= w:
            pass
        else:
            x += speed
    


def block(i):
    global S,T,Bx,By,w,win,Bs,C,speed,score, checker
    S[i-1] = pygame.time.get_ticks()
    if S[i-1]-T[i-1] >= C[i-1]*1000:
        pygame.draw.rect(win,(0,0,255),(Bx[i-1],By[i-1],Bs,Bs))
        pygame.display.update()
        By[i-1] += speed
        if By[i-1] > w + Bs:
            By[i-1] = -Bs
            Bx[i-1] = random.randint(0, w-Bs)
            score -= 1
        key = pygame.key.get_pressed()
        
        for jx in range(Bx[i-1],Bx[i-1] + Bs):
            for jy in range (By[i-1],By[i-1] + Bs):
                if player.collidepoint(jx,jy):
                    checker = True
        if checker:
            score += 2
            checker = False
while True:
    win.fill((255,255,255))
    draw()
    block(1)
    block(2)
    block(3)
    block(4)
    block(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f'Abhinav\'s Game Says,\'Your score was {score}\'')
            exit()
    _type_=pygame.font.Font('freesansbold.ttf',(w*4)//100)
    text=_type_.render(f'Score:- {score}',True,(255,0,0))
    textrect=text.get_rect()
    textrect.topleft = (0,0)
    win.blit(text,textrect)
    pygame.display.update()
    clock.tick(fps)