import pygame, time
from pygame.locals import *

pygame.init()

w = 500
h = 500
col = None
i_val = 0
begin = True

win = pygame.display.set_mode((w, h))
win.fill((255, 255, 185))
pygame.display.update()


def stop():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()


while True:
    stop()
    for j in range(10):
        if i_val >= 255:
            i_val = 1
        for i in range(1, 256):
            if j%2 ==1:
                if i_val >= 255:
                    i_val = 0
                col = i_val
                i_val += 1
                win.fill((255, 255, col))    #  Y to W
                time.sleep(0.01)
                stop()
                pygame.display.update()
                if i_val >= 255:
                    i_val = 0
            else:
                if i_val >= 255:
                    i_val = 0
                col = 255 - i_val
                win.fill((255, 255, col)) # W to Y
                time.sleep(0.01)
                stop()
                pygame.display.update()
                i_val += 1
                if i_val >= 255:
                    i_val = 0