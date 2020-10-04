import pygame
from pygame.locals import *
import time
import random as rand

#                                    Variables
#                                   Changables
w = 500
h = w
#                                   Changables
#                                     Colours
#                R    G    B

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
#                                     Colours

active = "none"
play_list = []
count = 0
btn_list = ['RED', 'BLUE', 'GREEN', 'YELLOW']

#                                    Variables
#                                  Startup_Codes
win = pygame.display.set_mode((w, h))
win.fill(WHITE)
pygame.display.update()


#                                  Startup_Codes
#                                 Functions_Classes
class Button:
    def __init__(self, nums):
        self.button_num = nums
        self.x, self.y = self.get_pos()
        self.rect = "none"
        self.show()

    def get_pos(self):
        if self.button_num == 1:
            return int(w // 12.5), int(w // 12.5)
        if self.button_num == 2:
            return int(w // 12.5), int(w // 1.9)
        if self.button_num == 3:
            return int(w // 1.9), int(w // 12.5)
        if self.button_num == 4:
            return int(w // 1.9), int(w // 1.9)

    def get_col(self, num):
        if num == 1:
            if self.glow(1):
                return BRIGHTRED
            else:
                return RED
        if num == 2:
            if self.glow(2):
                return BRIGHTBLUE
            else:
                return BLUE
        if num == 3:
            if self.glow(3):
                return BRIGHTGREEN
            else:
                return GREEN
        if num == 4:
            if self.glow(4):
                return BRIGHTYELLOW
            else:
                return YELLOW

    def show(self):
        self.rect = pygame.draw.rect(win, self.get_col(self.button_num), (self.x, self.y, w // 2.6, w // 2.6))
        pygame.display.update()

    def glow(self, num):
        global active
        if active == 'RED' and num == 1:
            active = "none"
            return True
        if active == 'BLUE' and num == 2:
            active = "none"
            return True
        if active == "GREEN" and num == 3:
            active = "none"
            return True
        if active == "YELLOW" and num == 4:
            active = "none"
            return True


def stop():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()


def get_list():
    global play_list, btn_list, count
    if count < 21:
        play_list.append(rand.choice(btn_list))
        count += 1
        print(play_list)
        show_pat()


def show_pat():
    global play_list, active, b, b2, b3, b4
    for i in range(len(play_list)):
        active = play_list[i]
        start = time.time()
        update()
        start1 = time.time()
        while time.time() - start1 < 0.5:
            stop()
        active = 'none'
        update()
        while time.time() - start < 1:
            stop()
    active = "none"
    update()
    print('go')
    p_input()


def update():
    global b, b2, b3, b4
    b = Button(1)
    b2 = Button(2)
    b3 = Button(3)
    b4 = Button(4)


def p_input():
    global play_list, active
    x, y = 0, 0
    start = time.time()
    ran = 0
    while (time.time() - start < 5) and (ran < len(play_list)):
        stop()
        if play_list[ran] == 'RED' and b.rect.collidepoint(x, y):
            active = "RED"
        if play_list[ran] == 'BLUE' and b2.rect.collidepoint(x, y):
            active = "BLUE"
        if play_list[ran] == 'GREEN' and b3.rect.collidepoint(x, y):
            active = "GREEN"
        if play_list[ran] == 'YELLOW' and b4.rect.collidepoint(x, y):
            active = "YELLOW"
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x, y)
                ran += 1
                start = time.time()
                print(ran)


#                                    Functions_Classes


b = Button(1)
b2 = Button(2)
b3 = Button(3)
b4 = Button(4)
while True:
    stop()
    get_list()
