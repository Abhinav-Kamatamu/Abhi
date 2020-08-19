import pygame
import random
import time
from pygame.locals import *

pygame.init()

colours = {'red': (204, 0, 0), 'green': (0, 204, 0), 
           'blue': (0, 0, 204), 'd_red': (255, 51, 51), 
           'd_green': (51, 255, 51), 'd_blue': (51, 51, 255),
           'yellow': (204, 204, 0), 'd_yellow': (255, 255, 51)}
w = 800
h = w
empty = []
colt = 'normal'
n = 0
click = False


def get(x):
    global colt
    if x == 'red':
        colt = 'red'
    if x == 'green':
        colt = 'green'
    if x == 'blue':
        colt = 'blue'
    if x == 'yellow':
        colt = 'yellow'
        return (colt)


def listr():
    global empty
    col = ['red', 'green', 'blue', 'yellow']
    for i in range(21):
        x = random.choice(col)
        empty.append(x)
    return empty


def co(x):
    return (colours.get(x))


win = pygame.display.set_mode((w, h))


class board():
    def draw(self):
        global red, green, blue, yellow
        if colt == 'normal':
            red = pygame.draw.rect(win, co('red'), ((0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            green = pygame.draw.rect(win, co('green'), (((w - 0.35 * w) - 0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            blue = pygame.draw.rect(win, co('blue'), ((0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))
            yellow = pygame.draw.rect(win, co('yellow'),
                                      (((w - 0.35 * w) - 0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))

        if colt == 'red':
            red = pygame.draw.rect(win, co('d_red'), ((0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            green = pygame.draw.rect(win, co('green'), (((w - 0.35 * w) - 0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            blue = pygame.draw.rect(win, co('blue'), ((0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))
            yellow = pygame.draw.rect(win, co('yellow'),
                                      (((w - 0.35 * w) - 0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))
            o_red = pygame.draw.rect(win, (0, 0, 0), ((0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)), int(0.35 * w * 0.03))

        if colt == 'blue':
            red = pygame.draw.rect(win, co('red'), ((0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            green = pygame.draw.rect(win, co('green'), (((w - 0.35 * w) - 0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            blue = pygame.draw.rect(win, co('d_blue'), ((0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))
            yellow = pygame.draw.rect(win, co('yellow'),
                                      (((w - 0.35 * w) - 0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))
            o_blue = pygame.draw.rect(win, (0, 0, 0), ((0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)),
                                      int(0.35 * w * 0.03))

        if colt == 'green':
            red = pygame.draw.rect(win, co('red'), ((0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            green = pygame.draw.rect(win, co('d_green'), (((w - 0.35 * w) - 0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            blue = pygame.draw.rect(win, co('blue'), ((0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))
            yellow = pygame.draw.rect(win, co('yellow'),
                                      (((w - 0.35 * w) - 0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))
            o_green = pygame.draw.rect(win, (0, 0, 0), (((w - 0.35 * w) - 0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)),
                                       int(0.35 * w * 0.03))

        if colt == 'yellow':
            red = pygame.draw.rect(win, co('red'), ((0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            green = pygame.draw.rect(win, co('green'), (((w - 0.35 * w) - 0.1 * w, 0.1 * h), (0.35 * w, 0.35 * h)))
            blue = pygame.draw.rect(win, co('blue'), ((0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))
            yellow = pygame.draw.rect(win, co('d_yellow'),
                                      (((w - 0.35 * w) - 0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)))
            d_yellow = pygame.draw.rect(win, (0, 0, 0),
                                        (((w - 0.35 * w) - 0.1 * w, (h - 0.35 * h) - 0.1 * h), (0.35 * w, 0.35 * h)),
                                        int(0.35 * w * 0.03))


bo = board()
win.fill((255, 255, 255))
coltl = []
bo.draw()
pygame.display.update()
x, y = (0, 0)
time.sleep(1)
ext = 0

while True:
    bo.draw()

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    for i in range(20):
        a = random.choice(['red', 'green', 'blue', 'yellow'])
        coltl.append(a)
        print(coltl)
        for i in coltl:
            exe = 0
            x, y = 0, 0
            colt = i
            win.fill((255, 255, 255))
            bo.draw()
            pygame.display.update()
            time.sleep(1)
            win.fill((255, 255, 255))
            colt = 'normal'
            bo.draw()
            pygame.display.update()
            time.sleep(1)
            while ext == 0:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        x, y = event.pos
                        click = True
                        if click:
                            if (red.collidepoint(x, y) and i == 'red') \
                                    or (green.collidepoint(x, y) and i == 'green') \
                                    or (blue.collidepoint(x, y) and i == 'blue') \
                                    or (yellow.collidepoint(x, y) and i == 'yellow'):
                                pass

                            if (red.collidepoint(x, y) and i != 'red') \
                                    or (green.collidepoint(x, y) and i != 'green') \
                                    or (blue.collidepoint(x, y) and i != 'blue') \
                                    or (yellow.collidepoint(x, y) and i != 'yellow'):
                                exit()

                click = False
                ext = 1
            ext = 0

    pygame.display.update()
