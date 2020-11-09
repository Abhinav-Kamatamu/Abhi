import pygame
import time
import random
import sys

name = 'Abhinav'  # input('name  :-  ')
W, H = 640, 400
FPS = 40
get_ran = random.randint(0, 150)
pygame.init()
clock = pygame.time.Clock()
speed = 4
si = 100
pos_x = 640
n = 10
pos_y = 400 - si
r = random.randint(0, 255)
g = random.randint(0, 255)
b = random.randint(0, 255)
col = (r, g, b)
forsi = True
first = True
no = []
check = False
co = 0
runing = False
main = True


def get_p(name):
    for i in name:
        i = i.lower()
        if ('a' <= i <= 'z') or i == ' ':
            pass
        else:
            print('I think {} is not a proper name'.format(name))
            time.sleep(2)
            exit()


class Mario:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isJump = False
        self.jumpCount = 10

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 40, 40))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, 40, 40), 5)
        _type_ = pygame.font.Font('freesansbold.ttf', 15)
        text = _type_.render('YOU', True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.topleft = (self.x + 3, self.y - 20)
        screen.blit(text, textrect)

    def clash(self):
        global my, runing, FPS, co, pos_x, name, forsi, pos_x, main, no, col, r, g, b, check, si, first
        hi = int(self.y)
        for x in range(self.x, self.x + 40):
            for y in range(hi, hi + 40):
                if my.collidepoint(x, y):
                    time.sleep(1)
                    screen.fill([0, 0, 0])
                    pygame.display.update()
                    while runing:
                        pygame.display.set_caption('press r to restart    press x to exit')
                        screen.fill((0, 0, 0))
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_r] or keys[pygame.K_SPACE]:
                            runing = False
                            speed = 6
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                runing = False
                                speed = 6
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                                    runing = False
                                    speed = 6
                                    no.append(co)
                                    if first:
                                        if co == 0:
                                            forsi = True
                                            si = 100
                                    if co != 0:
                                        check = True
                                        first = False
                                if event.key == pygame.K_x:
                                    pygame.quit()
                                    runing = False
                                    main = False
                                    no.append(co)
                                    print(name, ', Your Highest Score Is', (max(no)))
                                    print(speed)
                                    exit()

                        pygame.display.update()
                        clock.tick(FPS)
                    pygame.display.update()
                    co = 0
                    speed = 6
                    speed = 6
                    runing = True
                    pos_x = 640
                    return (co)

    def jump(self):
        if self.isJump:
            if self.jumpCount >= -15:
                neg = -1
                if self.jumpCount > 0:
                    neg = 1
                self.y -= self.jumpCount ** 2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 15


def ranobj():
    global check, pos_x, pos_y, col, my, screen, si, co, get_ran, r, g, b, col
    if check:
        si = random.randint(10, 60)
        pos_x = random.randint(640, 1000)
        pos_y = 400 - si
        get_ran = random.randint(0, 150)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        col = (r, g, b)
        check = False
    my = pygame.draw.rect(screen, col, (pos_x, pos_y, si, si))
    if r >= 200 and g >= 200 and b >= 200:
        your = pygame.draw.rect(screen, (128, 128, 128), (pos_x, pos_y, si, si), 3)
    else:
        your = pygame.draw.rect(screen, (0, 0, 0), (pos_x, pos_y, si, si), 3)
    pos_x -= speed
    if pos_x < 0 - si:
        check = True
        num_2 = True
        co += 1


mario = Mario(200, 275)
get_p(name)
screen = pygame.display.set_mode((W, H))


def init():
    global screen
    screen.fill((0, 0, 0))
    redraw()
    pygame.display.update()
    time.sleep(2)
    fade = pygame.Surface((640, 400))
    fade.fill((255, 255, 255))
    for alpha in range(0, 50):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)
        pygame.display.update()


def redraw():
    screen.fill((0, 0, 0))
    image = pygame.image.load('GeoDash.png')
    screen.blit(image, (0, 0))


name = name.capitalize()
pygame.display.set_caption('{}, Your Score  Is  :-  {}'.format(name, co))
init()
while main:
    name = name.capitalize()
    pygame.display.set_caption('{}, Your Score  Is  :-  {}'.format(name, co))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            no.append(co)
            print(name, ', Your Highest Score Is', (max(no)))
        if event.type == pygame.MOUSEBUTTONDOWN:
            mario.isJump = True
            if forsi:
                si = 5
                pos_y = 400 - si
                forsi = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mario.isJump = True
                if forsi:
                    si = 5
                    pos_y = 400 - si
                    forsi = False
            if event.key == pygame.K_w:
                mario.isJump = True
                if forsi:
                    si = 5
                    pos_y = 400 - si
                    forsi = False
            if event.key == pygame.K_UP:
                mario.isJump = True
                if forsi:
                    si = 5
                    pos_y = 400 - si
                    forsi = False

    clock.tick(FPS)
    pressed_keys = pygame.key.get_pressed()
    ranobj()
    mario.draw()
    mario.jump()
    if co == n:
        if speed == 11 or speed > 11:
            pass
        else:
            speed += 1
            n += 10
    if co < 50 or (co < 150 and co > 100) or co > 150:
        screen.fill((255, 255, 255))
    else:
        screen.fill((random.randint(5, 255), random.randint(5, 255), random.randint(5, 155)))
    mario.draw()
    mario.clash()
    ranobj()
    pygame.display.update()
