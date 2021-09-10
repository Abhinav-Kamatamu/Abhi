import random

import pygame
import time
from pygame.locals import *

pygame.init()

w = 500
h = 500
win = pygame.display.set_mode((w, h))
BALLOON = pygame.image.load('balloon.png')
POP = pygame.image.load('pop.png')
sound = pygame.mixer.Sound('Pop.wav')
clock = pygame.time.Clock()
fps = 60
balloon_list = []


class Balloon:
    def __init__(self):
        self.x = random.randint(0, w - 100)
        self.y = random.randint(h, h + 300)
        self.pressed = False
        self.pop = False
        self.speed = 1
        self.start_time = random.randint(0, 10000)
        self.pop_time = None
        self.deactivate = False

    def poping(self):
        if not self.pop and self.pressed:
            player.score += 1
        if self.pressed:
            self.pop = True
            self.pressed = False
            self.pop_time = time.time()

    def draw(self):
        if not self.pop:
            win.blit(BALLOON, (self.x, self.y))
        else:
            win.blit(POP, (self.x, self.y))

    def move(self):
        if not self.pop and not self.deactivate:
            self.y -= self.speed
        else:
            pass
        if self.y <= -100:
            self.y = h
            # self.x = random.randint(0, w - 100)
            self.x = 0

    def shot(self):
        if not self.deactivate:
            for ix in range(self.x + 33, self.x + 66):
                for iy in range(self.y + 100 - 68, self.y + 100 - 32):
                    if player.bullet.collidepoint(ix, iy):
                        self.pressed = True

    def startRound(self):
        try:
            if self.deactivate and time.time() - player.roundtime >= 2:
                self.deactivate = False
                self.pop = False
                self.y = random.randint(h, h + 300)
                for i in balloon_list:
                    i.deactivate = False
                    i.pop = False
                    i.y = random.randint(h, h + 300)
                player.roundtime = None
                for i in range(10):
                    balloon_list.append(Balloon())
                balloon_list.append(Balloon())
        except:
            pass


class Player:
    def __init__(self):
        self.x = w // 2
        self.score = 0
        self.y = 10
        self.shoot = False
        self.speed = 5
        self.s = w // 10
        self.bulx = -30
        self.roundtime = None
        self.buly = -30
        self.bulb = 5
        self.roundlimit = []
        self.ascore = 0
        self.round = 1
        self.bull = 10
        self.character = None
        self.bullet = pygame.draw.rect(win, (255, 0, 0), [self.bulx, self.buly, self.bulb, self.bull])
        self.bulmove = False
        self.bulspeed = 10

    def move(self):
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.x -= self.speed
        if keys[K_RIGHT]:
            self.x += self.speed
        self.shooter()

        if self.shoot and not self.bulmove:
            self.bulx = self.x + self.s // 2 - self.bulb // 2
            self.buly = self.y + self.s
            self.shoot = False
            self.bulmove = True

        if self.bulmove:
            self.buly += self.bulspeed
            if self.buly > h:
                self.bulmove = False
                self.shoot = False
                self.buly = -30

    def draw(self):
        self.character = pygame.draw.rect(win, (0, 0, 0), [self.x, self.y, self.s, self.s])
        self.bullet = pygame.draw.rect(win, (255, 0, 0), [self.bulx, self.buly, self.bulb, self.bull])
        _type_ = pygame.font.Font('freesansbold.ttf', 20)
        text = _type_.render('Score:- {}'.format(self.score), True, (255, 0, 0))
        textrect = text.get_rect()
        textrect.topleft = (0, 0)
        win.blit(text, textrect)

    def shooter(self):
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.shoot = True

    def rounds(self):
        for i in balloon_list:
            if not i.deactivate and not i.pop:
                self.roundlimit.append(None)
        print(len(self.roundlimit))
        if self.ascore >= len(self.roundlimit):
            self.round += 1
            self.x = w // 2
            self.roundtime = time.time()
            self.ascore += self.score
            self.score = 0
        self.roundlimit = []
        print(self.ascore)


for i in range(w // 50):
    balloon_list.append(Balloon())
start = time.time()
print(len(balloon_list))
player = Player()
while True:
    win.fill((255, 255, 255))
    for i in balloon_list:
        i.draw()
        i.move()
        i.shot()
        i.poping()
        i.startRound()
        if i.pop_time is not None:
            if time.time() - i.pop_time > 2:
                i.deactivate = True
                i.pop_time = None
                i.y = h
    player.draw()
    player.move()
    player.rounds()
    pygame.display.update()
    clock.tick(fps)
