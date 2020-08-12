import pygame
import random as r
import time
from pygame.locals import *

pygame.init()

w = 300
s = 20
x = r.randint(s, w - s)
y = r.randint(s, w - s)
speed = 3
speed_x = r.choice((-speed, speed))
speed_y = r.choice((-speed, speed))
win = pygame.display.set_mode((w, w))
clock = pygame.time.Clock()
fps = 120


def stop():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
        if event.type == QUIT:
            exit()


def get_r():
    return ((r.randint(0, 255), r.randint(0, 255), r.randint(0, 255)))


def check():
    global speed_y, speed_x, x, y

    # x on right

    if x >= w - s:
        if speed_x == speed:
            speed_x = -speed
            win.fill(get_r())
        else:
            speed_x = speed
            win.fill(get_r())

    # y on bottom

    elif y >= w - s:
        if speed_y == speed:
            speed_y = -speed
            win.fill(get_r())
        else:
            speed_y = speed
            win.fill(get_r())

    # x on right

    elif x <= s:
        if speed_x == speed:
            speed_x = -speed
            win, fill(())
        else:
            speed_x = speed
            win.fill(get_r())
    elif y <= s:
        if speed_y == speed:
            speed_y = -speed
            win.fill(get_r())
        else:
            speed_y = speed
            win.fill(get_r())


def follow():
    global x, y, speed_x, speed_y, fps
    for ii in pygame.event.get():
        if ii.type == MOUSEMOTION:
            rx, ry = ii.pos
            if s < rx < w - s and s < ry < w - s:
                x, y = ii.pos
                speed_x = 0
                speed_y = 0
                fps = 10000
        else:
            speed_x = r.choice((-speed, speed))
            speed_y = r.choice((-speed, speed))
            fps = 120


while True:
    stop()
    win.fill((255, 255, 255))
    pygame.draw.circle(win, (255, 0, 0), (x, y), s)
    pygame.display.update()
    check()
    follow()
    x += speed_x
    y += speed_y
    for i in pygame.event.get():
        if i.type == MOUSEMOTION:
            i.pos = (x, y)
            speed_y = 0
            speed_x = 0
    clock.tick(fps)
