import pygame, time
import random as ra
from pygame.locals import *

pygame.init()

w = 500
h = 500
col = None
i_val = 0
r = 0
g = 0
begin = True

win = pygame.display.set_mode((w, h))
win.fill((255, 255, 185))
pygame.display.update()


def stop():
    global col
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_SPACE:
                print(255, 255, col)
                exit()


while True:
    stop()
    for j in range(10):
        if i_val >= 255:
            i_val = 1
        if r >= 255:
            r = 0
        if g >= 255:
            g = 0
        rando = ra.randint(0, 1)
        for i in range(1, 256):
            if j % 2 == 1:
                if i_val >= 255:
                    i_val = 0
                if r >= 255:
                    r = 0
                if g >= 255:
                    g = 0
                col = i_val
                if rando == 1:
                    r_c = 255 - r
                    g_c = g
                else:
                    r_c = r
                    g_c = g
                r += 1
                g += 1
                i_val += 1
                win.fill((r_c, g_c, col))  # Y to W
                time.sleep(0.01)
                stop()
                pygame.display.update()
                if i_val >= 255:
                    i_val = 0
                if r >= 255:
                    r = 0
                if g >= 255:
                    g = 0
            else:
                if i_val >= 255:
                    i_val = 0
                if r >= 255:
                    r = 0
                if g >= 255:
                    g = 0
                col = 255 - i_val
                if rando == 1:
                    r_c = r
                    g_c = 255 - g
                else:
                    r_c = 255 - r
                    g_c = g
                win.fill((r_c, g_c, col))  # W to Y
                stop()
                time.sleep(0.01)
                stop()
                pygame.display.update()
                i_val += 1
                r += 1
                g += 1
                if i_val >= 255:
                    i_val = 0
                if r >= 255:
                    r = 0
                if g >= 255:
                    g = 0
