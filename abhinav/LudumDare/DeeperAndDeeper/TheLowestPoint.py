import pygame
from pygame.locals import *

pygame.init()

w = 1920
h = 1080
win = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
fps = 60


class Level1:
    def __init__(self):
        self.l = pygame.image.load('L1.png')

    def display(self):
        win.blit(self.l, (0, 0))
        pygame.display.update()

    def getObsticalls(self):
        self.ob1 = pygame.Surface((509, 138))  # x = 0, y = 1080-138
        self.ob2 = pygame.Surface((1090 - 660, 100))  # x = 660 , y = 691
        self.ob3 = pygame.Surface((1920 - 1300, 479))  # x = 1300, y = 1080-479
        self.rect1 = self.ob1.get_rect()
        self.rect1.topleft = (0, 1080 - 138)
        self.rect2 = self.ob2.get_rect()
        self.rect2.topleft = (660, 691)
        self.rect3 = self.ob3.get_rect()
        self.rect3.topleft = (1300, 1080 - 479)
        return [self.rect3, self.rect1, self.rect2]


class Level2:
    def __init__(self):
        self.l = pygame.image.load('L2.png')

    def display(self):
        win.blit(self.l, (0, 0))
        pygame.display.update()

    def getObsticalls(self):
        self.ob1 = pygame.Surface((200, 339))  # x = 0, y = 1080-339
        self.ob2 = pygame.Surface((1080 - 500, 449 - 309))  # x = 500 , y = 1080-449
        self.rect1 = self.ob1.get_rect()
        self.rect1.topleft = (0, 1080 - 338)
        self.rect2 = self.ob2.get_rect()
        self.rect2.topleft = (500, 1080 - 449)
        return [self.rect1, self.rect2]


class Level3:
    def __init__(self):
        self.l = pygame.image.load('L3.png')

    def display(self):
        win.blit(self.l, (0, 0))
        pygame.display.update()

    def getObsticalls(self):
        self.ob1 = pygame.Surface((1000 - 380, 399 - 249))  # x = 380 , y = 1080-399
        self.rect1 = self.ob1.get_rect()
        self.rect1.topleft = (380, 1080 - 399)
        return [self.rect1]


class Level4:
    def __init__(self):
        self.l = pygame.image.load('L4.png')

    def display(self):
        win.blit(self.l, (0, 0))
        pygame.display.update()

    def getObsticalls(self):
        self.ob1 = pygame.Surface((150, 819))  # x = 0 , y = 1080-819
        self.ob2 = pygame.Surface((1920 - 150, 89))  # x = 150, y = 1080-89
        self.ob3 = pygame.Surface((1920 - 1650, 849 - 269))  # x = 1650, y = 1080-849

        self.rect1 = self.ob1.get_rect()
        self.rect1.topleft = (0, 1080 - 819)
        self.rect2 = self.ob2.get_rect()
        self.rect2.topleft = (150, 1080 - 89)
        self.rect3 = self.ob2.get_rect()
        self.rect3.topleft = (1650, 1080 - 849)
        return [self.rect1, self.rect2, self.rect3]


class Player:
    def __init__(self):
        self.x = 20
        self.y = 1080 - 188
        self.s = 50
        self.level = L1
        self.v = 12
        self.start = True
        self.win = False
        self.m = 1
        self.isjump = False
        self.speed = 10
        self.otherv = 1

    def levelBackground(self):
        if self.level == L1:
            L1.display()
        if self.level == L2:
            L2.display()
        if self.level == L3:
            L3.display()
        if self.level == L4:
            L4.display()

    def draw(self):
        self.levelBackground()
        self.player = pygame.draw.rect(win, (255, 0, 0), [self.x, self.y, self.s, self.s])
        pygame.display.update()

    def move(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.x += self.speed
        if keys[K_LEFT]:
            self.x -= self.speed
        if keys[K_SPACE]:
            self.isjump = True
        self.hitObsticle()

        if self.level == L1:
            if self.y >= 1080:
                self.y = 1080 - 188
                self.x = 50
            if 660 < self.x < 760 and self.y > 1080 - 691:
                self.y = 691 - self.s
            if 1300 < self.x < 1920 and self.y < 1080 - 479:
                self.y = 1080 - 479 - self.s
            if self.x > 1920:
                self.level = L2
                self.x = 50
                self.y = 1080 - 339 - self.s

        if self.level == L2:
            if 0 < self.x < 200 and self.y > 1080 - 339:
                self.y = 1080 - 339 - self.s
            if self.y > 1080:
                self.y = 0
                self.level = L3

        if self.level == L3:
            if 380 < self.x < 1000 and self.y > 1080 - 399:
                self.y = 1080 - 399 - self.s
            if self.y > 1080:
                self.y = 0
                self.level = L4

        if self.level == L4:
            if 0 < self.x < 150 and self.y > 1080 - 819:
                self.y = 1080 - 819 - self.s
            if 1650 < self.x < 1920 and 1080 - 849 + 269 > self.y > 1080 - 849:
                self.y = 1080 - 849 - self.s
            if 150 < self.x < 1920 and self.y > 1080 - 89:
                self.y = 1080 - 89 - self.s
            if self.x + self.s > 1920 and self.y == 1080 - 89 - self.s:
                self.win = True
                self.screens()
            if self.x < 30:
                self.x = 30
            if self.x <= 161 and self.y == 1080 - 89 - self.s:
                self.x = 162

    def screens(self):
        start = pygame.image.load('Start.png')
        end = pygame.image.load('End.png')
        if self.start == True:
            for alpha in range(100):
                start.set_alpha(alpha)
                win.blit(start, (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                alpha += 1
            pygame.time.delay(400)
            self.levelBackground()
            start.set_alpha(255)
            win.blit(start, (0, 0))
            pygame.display.update()
            self.start = False

        if self.win:
            for alpha in range(255):
                end.set_alpha(alpha)
                win.blit(end, (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                alpha += 1
            quit()

    def hitObsticle(self):
        if self.level == L1:
            self.nos = L1.getObsticalls()
            if self.nos[0].collidepoint(self.x + (self.s // 2), self.y + self.s) or self.nos[1].collidepoint(
                    self.x + (self.s // 2), self.y + self.s) or self.nos[2].collidepoint(self.x + (self.s // 2),
                                                                                         self.y + self.s):
                return True
            else:
                if not self.isjump:
                    self.y -= (1 / 2 * -1) * self.otherv ** 2
                    self.otherv = self.otherv - 1
        if self.level == L2:
            self.nos = L2.getObsticalls()
            if self.nos[0].collidepoint(self.x + (self.s // 2), self.y + self.s) or self.nos[1].collidepoint(
                    self.x + (self.s // 2), self.y + self.s):
                return True
            else:
                if not self.isjump:
                    self.y -= (1 / 2 * -1) * self.otherv ** 2
                    self.otherv = self.otherv - 1
        if self.level == L3:
            self.nos = L3.getObsticalls()
            if self.nos[0].collidepoint(self.x + (self.s // 2), self.y + self.s):
                return True
            else:
                if not self.isjump:
                    self.y -= (1 / 2 * -1) * self.otherv ** 2
                    self.otherv = self.otherv - 1
        if self.level == L4:
            self.nos = L4.getObsticalls()
            if self.nos[0].collidepoint(self.x + (self.s // 2), self.y + self.s):
                return True
            else:
                if not self.isjump:
                    self.y -= (1 / 2 * -1) * self.otherv ** 2
                    self.otherv = self.otherv - 1

    def jump(self):
        if self.isjump:
            self.y -= (1 / 2 * self.m) * self.v ** 2
            self.v = self.v - 1

            if self.hitObsticle():
                self.isjump = False
                self.v = 12
                self.m = 1
            if self.v < 0:
                self.m = -1


L1 = Level1()
L2 = Level2()
L3 = Level3()
L4 = Level4()
square = Player()
square.screens()
while True:
    clock.tick(fps)
    square.move()
    square.draw()
    square.jump()
