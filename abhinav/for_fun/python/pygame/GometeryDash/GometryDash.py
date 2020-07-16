import pygame, time, math, random, sys
from pygame.locals import *

name = input('name  :-  ')
W, H = 640, 400
HW, HH = W / 2, H / 2
AREA = W * H
FPS = 45
bg_x = 0
get_ran = random.randint(0,150)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W,H))
speed = 7
si = 100
pos_x = 640
no = []
nam = []
nam.append(name)
pos_y = 400 - si
r = random.randint(0,255)
g = random.randint(0,255)
b = random.randint(0,255)
col = (r,g,b)
forsi = True
check = False
co = 0
runing = True
main = True

def get():
    global no, nam
    for i in range (len(nam)):
        if max(no) == no[i]:
            return(nam[i])

class Mario():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isJump = False
        self.jumpCount = 10

    def draw(self):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y, 40, 40))
    def clash(self):
        global my,runing,FPS,co,pos_x,name, forsi,pos_x, main
        hi = int(self.y)
        for x in range (self.x,self.x + 40):
            for y in range (hi,hi+ 40):
                if my.collidepoint(x,y):
                    pygame.display.update()
                    time.sleep(1)
                    while runing:
                        pygame.display.set_caption('press r to restart    press x to exit')
                        screen.fill((0,0,0))
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_r]:
                            runing = False
                        if keys[pygame.K_x]:
                            pygame.quit()
                            exit()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                runing = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:
                                    runing = False
                                    pos_x = W + W//2
                                    
                                    no.append(co)
                                    print(nam[-1],no[-1])
                                    name = input('name  :-  ')
                                    nam.append(name)
                                    time.sleep(2)
                                if event.key == pygame.K_x:
                                    no.append(co)
                                    print(nam[-1],no[-1])
                                    print(get(),'is at max by',(max(no)))
                                    main = False
                        pygame.display.update()
                        clock.tick(FPS)
                    screen.fill([255,255,255])
                    pygame.display.update()
                    co = 0
                    runing = True
                    check = True
                    pos_x = 640
                    return(co)
                                            

    def jump(self):
        if self.isJump:
            if self.jumpCount >= -15:
                neg = -1
                if self.jumpCount > 0:
                    neg = 1
                self.y -= self.jumpCount**2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 15

def ranobj():
    global check,pos_x,pos_y,col,my,screen, si, co, get_ran
    if check:
        si = random.randint(10,60)
        pos_x = 640
        pos_y = 400 - si
        get_ran = random.randint(0,150)
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        col = (r,g,b)
        check = False
    my = pygame.draw.rect(screen,col,(pos_x,pos_y,si,si))
    pos_x -= speed
    if pos_x < get_ran:
        check = True
        num_2 = True
        co += 1
    if pos_x < 60 and pos_x > 40:
        mario.isJump = True
mario = Mario(200, 275)

while main:
    name = name.capitalize()
    pygame.display.set_caption(f'{name}, Your Score  Is  :-  {co}')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mario.isJump = True
            if forsi:
                    si = 5
                    pos_y = 400- si
                    forsi = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mario.isJump = True
                if forsi:
                    si = 5
                    pos_y = 400- si
                    forsi = False
            if event.key == pygame.K_w:
                mario.isJump = True
                if forsi:
                    si = 5
                    pos_y = 400- si
                    forsi = False
            if event.key == pygame.K_UP:
                mario.isJump = True
                if forsi:
                    si = 5
                    pos_y = 400- si
                    forsi = False
    
    clock.tick(FPS)
    pressed_keys = pygame.key.get_pressed()
    ranobj()
    mario.draw()
    mario.jump()
    if co < 50 or (co < 150 and co>100) or co > 150:
        screen.fill((255,255,255))
    else:
        screen.fill((random.randint(5,255), random.randint(5,255),random.randint(5,155)))
    mario.draw()
    ranobj()
    mario.clash()
    pygame.display.update()

