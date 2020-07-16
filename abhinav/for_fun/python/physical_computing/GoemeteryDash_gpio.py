import pygame, time, math, random, sys, gpiozero
from pygame.locals import *

name = input('name  :-  ')
W, H = 640, 400
FPS = 40
get_ran = random.randint(0,150)
pygame.init()
clock = pygame.time.Clock()
speed = 9
si = 100
pos_x = 640
pos_y = 400 - si
r = random.randint(0,255)
g = random.randint(0,255)
b = random.randint(0,255)
col = (r,g,b)
forsi = True
first = True
no = []
led = gpiozero.LED(2)
check = False
co = 0
runing = True
main = True
led.on()

def get_p(name):
    for i in name:
        i = i.lower()
        if (i >= 'a' and i <= 'z') or i == ' ' :
            pass
        else:
            print(f'I think {name} is not a proper name')
            time.sleep(2)
            exit()
class Mario():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isJump = False
        self.jumpCount = 10

    def draw(self):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y, 40, 40))
    def clash(self):
        global my,runing,FPS,co,pos_x,name, forsi,pos_x, main, no,col,r,g,b,check,si,first
        hi = int(self.y)
        for x in range (self.x,self.x + 40):
            for y in range (hi,hi+ 40):
                if my.collidepoint(x,y):
                    time.sleep(1)
                    screen.fill([0,0,0])
                    pygame.display.update()
                    while runing:
                        pygame.display.set_caption('press r to restart    press x to exit')
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_r] or keys[pygame.K_SPACE]:
                            runing = False
                            led.off()
                            time.sleep(random.randint(1,6))
                            led.on()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                led.off()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                runing = False
                                led.off()
                                time.sleep(random.randint(1,6))
                                led.on()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                                    runing = False
                                    no.append(co)
                                    if first:
                                        if co == 0:
                                            forsi = True
                                            si = 100
                                    if co !=0:
                                        check = True
                                        first = False
                                    led.off()
                                    time.sleep(random.randint(1,6))
                                    led.on()
                                if event.key == pygame.K_x:
                                    for i in range (50):
                                        led.off()
                                    pygame.quit()
                                    runing = False
                                    main = False
                                    no.append(co)
                                    print(name, ', Your Highest Score Is',(max(no)))
                                    return(1)
                        clock.tick(FPS)
                    pygame.display.update()
                    co = 0
                    runing = True
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
    global check,pos_x,pos_y,col,my,screen, si, co, get_ran, r,g,b,col
    if check:
        si = random.randint(10,60)
        pos_x = random.randint(640,800)
        pos_y = 400 - si
        get_ran = random.randint(0,150)
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        col = (r,g,b)
        check = False
    my = pygame.draw.rect(screen,col,(pos_x,pos_y,si,si))
    if r >= 200 and g >= 200 and b >=200:
        your = pygame.draw.rect(screen,(128,128,128),(pos_x,pos_y,si,si),3)
    else:
        your = pygame.draw.rect(screen,(0,0,0),(pos_x,pos_y,si,si),3)
    pos_x -= speed
    if pos_x < 0-si:
        check = True
        num_2 = True
        co += 1

mario = Mario(200, 275)
get_p(name)
screen = pygame.display.set_mode((W,H))
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
    pygame.display.update()
    mario.clash()
led.off()