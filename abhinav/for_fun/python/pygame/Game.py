import random as r
import pygame
from pygame.locals import *

pygame.init()

# ----------------------------------------------Variables

# ---------------------------------------------General Variables
w = 500
h = 500
fps = 60
clock = pygame.time.Clock()
speed = 4
# ---------------------------------------------General Variables

# ---------------------------------------------Player's variables
player_w = 25 // 2 * 3
player_h = player_w
player_x = w // 2 - player_w // 2
player_y = h // 8
player_col = (255, 0, 0)
player = None
# ---------------------------------------------Player's variables

# ---------------------------------------------Variables
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Abhinav\'s PROGRAM')
win.fill((255, 255, 255))
pygame.display.update()


def escape():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        exit()


def player_block():
    global win, player, player_x, player_y, player_w, player_h
    player = pygame.draw.rect(win, player_col, (player_x, player_y, player_w, player_h))
    keys = pygame.key.get_pressed()
    if player_x <= w - player_w:
        if keys[K_RIGHT] or keys[K_a]:
            player_x += speed
    if player_x >= 0:
        if keys[K_LEFT] or keys[K_d]:
            player_x -= speed


def obstcal():
    global line_col
    pygame.draw.line(win, line_col, (r.randint(0,w/2)))


while True:
    win.fill((255, 255, 255))
    player_block()
    escape()
    pygame.display.update()
    clock.tick(fps)
